# crew.py
from crewai import Crew, Process
from .agents import create_profiler_agent, create_analyst_agent, create_planner_agent
from .tasks import create_profiling_task, create_analyst_task, create_benchmarking_task, create_weekly_planning_task, create_update_planning_task, create_daily_tasks_generation_task, create_feedback_aware_planning_task
from .models import validate_planner_output, validate_feedback_aware_output, validate_daily_tasks_output, validate_update_planner_output
import json
import re


def extract_and_validate_json(raw_output, validator_func):
    """
    Extract JSON from raw output and validate using Pydantic models.
    Handles multiple JSON extraction strategies with improved error handling.
    """
    try:
        print(f"🔍 Attempting to validate output type: {type(raw_output)}")
        
        # Strategy 1: Check if it's already a dictionary (most common case)
        if isinstance(raw_output, dict):
            try:
                validated_output = validator_func(raw_output)
                print("✅ Successfully validated dictionary input")
                return validated_output
            except Exception as e:
                print(f"❌ Dictionary validation failed: {str(e)}")
                raise ValueError(f"Dictionary validation failed: {str(e)}")
        
        # Strategy 2: If it's a string or other type, convert to string and validate
        raw_str = str(raw_output).strip()
        print(f"🔍 Attempting to extract JSON from string (length: {len(raw_str)})")
        
        try:
            # Use the improved validation function which handles both dict and string inputs
            validated_output = validator_func(raw_str)
            print("✅ Successfully validated extracted JSON")
            return validated_output
            
        except Exception as e:
            print(f"❌ JSON extraction and validation failed: {str(e)}")
            print(f"📄 Raw output preview: {raw_str[:500]}...")
            raise ValueError(f"JSON validation failed: {str(e)}")
        
    except Exception as e:
        print(f"❌ Critical error in extract_and_validate_json: {str(e)}")
        raise ValueError(f"Failed to extract and validate JSON: {str(e)}")


def validate_challenge_structure(challenges):
    """Validate that challenges have exactly the right difficulty distribution (legacy function)"""
    if len(challenges) != 6:
        raise ValueError(f"Must have exactly 6 challenges, got {len(challenges)}")
    
    difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
    for challenge in challenges:
        difficulty = challenge.get('difficulty', '').lower()
        if difficulty in difficulty_counts:
            difficulty_counts[difficulty] += 1
        else:
            raise ValueError(f"Invalid difficulty level: {difficulty}")
    
    if difficulty_counts["easy"] != 3:
        raise ValueError(f"Must have exactly 3 easy challenges, got {difficulty_counts['easy']}")
    if difficulty_counts["medium"] != 2:
        raise ValueError(f"Must have exactly 2 medium challenges, got {difficulty_counts['medium']}")
    if difficulty_counts["hard"] != 1:
        raise ValueError(f"Must have exactly 1 hard challenge, got {difficulty_counts['hard']}")
    
    return True


# Agent 1 - Profiler Agent Workflow
# =========================================================
def run_profiler_workflow(user_data):
    """Executes the profiler agent workflow (Agent 1)"""
    
    # Create profiler agent
    profiler_agent = create_profiler_agent()    
    # Create profiling task
    profiling_task = create_profiling_task(profiler_agent, user_data)    
    # Form the crew with single profiler agent
    crew = Crew(
        agents=[profiler_agent],
        tasks=[profiling_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )    
    # Execute and return results
    results = crew.kickoff()    
    return results



# Agent 2 - Analyst Agent Workflow
# =========================================================
def run_analyst_workflow(user_id):
    """Executes the analyst workflow using enriched profile from Agent 1"""
    
    # Import here to avoid circular imports
    from data_model.database import get_profiler_results
    
    # Get enriched profile from Agent 1 results
    enriched_profile = get_profiler_results(user_id)
    
    if not enriched_profile:
        raise ValueError("No enriched profile found. Agent 1 must be completed first.")
    
    # Create analyst agent
    analyst_agent = create_analyst_agent()
    
    # Create analyst task with enriched profile as input
    analyst_task = create_analyst_task(analyst_agent, enriched_profile)
    
    # Form the crew with single analyst agent
    crew = Crew(
        agents=[analyst_agent],
        tasks=[analyst_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    # Execute and return results
    results = crew.kickoff()
    return results

def create_analyst_crew(user_data):
    """Creates and runs the analyst crew (legacy - for backwards compatibility)"""
    
    # Create agents
    analyst_agent = create_analyst_agent()
    planner_agent = create_planner_agent()
    
    # Create tasks - using new analyst task
    analyst_task = create_analyst_task(analyst_agent, user_data)
    benchmarking_task = create_benchmarking_task(analyst_agent, user_data, analyst_task)
    planning_task = create_weekly_planning_task(planner_agent, user_data, analyst_task, benchmarking_task)
    
    # Form the crew with sequential process
    crew = Crew(
        agents=[analyst_agent, planner_agent],
        tasks=[analyst_task, benchmarking_task, planning_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    return crew





def create_update_planner_crew(user_data, carbon_results, benchmark_results, user_update_text):
    """Creates a crew for handling user updates and adaptive planning"""
    pass

def run_update_planning_workflow(user_data, carbon_results, benchmark_results, user_update_text):
    """Executes the update planning workflow when user provides feedback from dashboard"""
    pass

def run_feedback_aware_planning_workflow(user_id: str, raw_feedback: str = None):
    """
    Executes the feedback-aware planning workflow using the Two-Tiered Memory System.
    
    Args:
        user_id (str): User's UUID
        raw_feedback (str): Optional new feedback from user
    
    Returns:
        dict: Planning results with feedback adaptation and validated JSON
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import (
            get_profiler_results, get_agent_results, 
            get_user_feedback_history, save_feedback_and_process
        )
        from .tasks import create_feedback_aware_planning_task
        
        # Step 1: Process new feedback if provided
        if raw_feedback:
            print(f"🔄 Processing new feedback for user {user_id}")
            feedback_success = save_feedback_and_process(user_id, raw_feedback)
            if not feedback_success:
                print("⚠️ Warning: Failed to save feedback, continuing with existing data")
        
        # Step 2: Get Tier 1 Memory (stable user data)
        print("📋 Fetching Tier 1 Memory (stable profile data)")
        user_profile = get_profiler_results(user_id)  # Agent 1 results
        carbon_analysis = get_agent_results(user_id)  # Agent 2 results
        
        if not user_profile:
            raise ValueError("No user profile found. Agent 1 must be completed first.")
        if not carbon_analysis:
            raise ValueError("No carbon analysis found. Agent 2 must be completed first.")
        
        # Step 3: Get Tier 2 Memory (dynamic feedback history)
        print("🧠 Fetching Tier 2 Memory (feedback history)")
        feedback_history = get_user_feedback_history(user_id, limit=3)
        
        if feedback_history:
            print(f"✅ Found {len(feedback_history)} feedback entries")
            print(f"📝 Latest feedback: {feedback_history[0]['summary']}")
        else:
            print("ℹ️ No feedback history found - using standard planning")
        
        # Step 4: Create feedback-aware planner agent
        planner_agent = create_planner_agent()
        
        # Step 5: Create feedback-aware planning task
        planning_task = create_feedback_aware_planning_task(
            planner_agent, 
            user_profile, 
            carbon_analysis, 
            {},  # benchmark_results placeholder
            feedback_history
        )
        
        # Step 6: Form the crew and execute
        print("🚀 Executing feedback-aware planning workflow")
        crew = Crew(
            agents=[planner_agent],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        raw_results = crew.kickoff()
        
        # Validate and parse JSON output
        print("🔍 Validating feedback-aware JSON output with Pydantic")
        try:
            validated_results = extract_and_validate_json(raw_results, validate_feedback_aware_output)
            print("✅ Successfully validated feedback-aware planning output")
            return validated_results.model_dump()
            
        except Exception as validation_error:
            print(f"❌ Validation failed for feedback-aware planning: {str(validation_error)}")
            print(f"� Raw results preview: {str(raw_results)[:300]}...")
            raise ValueError(f"Failed to validate feedback-aware planning output: {str(validation_error)}")
            
        except Exception as validation_error:
            print(f"❌ Feedback-aware JSON validation failed: {str(validation_error)}")
            print(f"🔍 Raw output: {str(raw_results)[:500]}...")
            raise validation_error
        
    except Exception as e:
        print(f"❌ Error in feedback-aware planning workflow: {str(e)}")
        raise e


def run_planner_workflow(user_id: str):
    """
    Executes the basic planner workflow (Agent 3) for initial challenge generation.
    
    Args:
        user_id (str): User's UUID
    
    Returns:
        dict: Planning results with validated JSON
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import get_profiler_results, get_agent_results
        from .tasks import create_weekly_planning_task
        
        print(f"🔄 Starting planner workflow for user {user_id}")
        
        # Get user data
        user_profile = get_profiler_results(user_id)  # Agent 1 results
        carbon_analysis = get_agent_results(user_id)  # Agent 2 results
        
        if not user_profile:
            raise ValueError("No user profile found. Agent 1 must be completed first.")
        if not carbon_analysis:
            raise ValueError("No carbon analysis found. Agent 2 must be completed first.")
        
        # Create planner agent
        planner_agent = create_planner_agent()
        
        # Create planning task
        planning_task = create_weekly_planning_task(
            planner_agent, 
            user_profile, 
            carbon_analysis, 
            {}  # benchmark_results placeholder
        )
        
        # Form the crew and execute
        print("🚀 Executing planner workflow")
        crew = Crew(
            agents=[planner_agent],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        raw_results = crew.kickoff()
        
        # Validate and parse JSON output
        print("🔍 Validating JSON output with Pydantic")
        try:
            validated_results = extract_and_validate_json(raw_results, validate_planner_output)
            print("✅ Successfully validated planner output")
            return validated_results.model_dump()
            
        except Exception as validation_error:
            print(f"❌ Validation failed for planner: {str(validation_error)}")
            print(f"� Raw results preview: {str(raw_results)[:300]}...")
            raise ValueError(f"Failed to validate planner output: {str(validation_error)}")
            
        except Exception as validation_error:
            print(f"❌ JSON validation failed: {str(validation_error)}")
            print(f"🔍 Raw output: {str(raw_results)[:500]}...")
            raise validation_error
        
    except Exception as e:
        print(f"❌ Error in planner workflow: {str(e)}")
        raise e

def create_daily_tasks_crew(user_data, carbon_results, benchmark_results, completed_tasks):
    """Creates a crew for generating daily tasks when user completes 3 out of 5 tasks"""
    pass

def run_daily_tasks_generation_workflow(user_id: str, completed_tasks: list):
    """
    Executes the daily tasks generation workflow when user completes 3 out of 5 challenges.
    
    Args:
        user_id (str): User's UUID
        completed_tasks (list): List of completed tasks
    
    Returns:
        dict: New daily tasks results with validated JSON
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import get_profiler_results, get_agent_results
        from .tasks import create_daily_tasks_generation_task
        
        print(f"🔄 Starting daily tasks generation for user {user_id}")
        
        # Get user data
        user_profile = get_profiler_results(user_id)
        carbon_analysis = get_agent_results(user_id)
        
        if not user_profile:
            raise ValueError("No user profile found. Agent 1 must be completed first.")
        if not carbon_analysis:
            raise ValueError("No carbon analysis found. Agent 2 must be completed first.")
        
        # Create planner agent
        planner_agent = create_planner_agent()
        
        # Create daily tasks generation task
        daily_tasks_task = create_daily_tasks_generation_task(
            planner_agent, 
            user_profile, 
            carbon_analysis, 
            {},  # benchmark_results placeholder
            completed_tasks
        )
        
        # Form the crew and execute
        print("🚀 Executing daily tasks generation workflow")
        crew = Crew(
            agents=[planner_agent],
            tasks=[daily_tasks_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        raw_results = crew.kickoff()
        
        # Validate and parse JSON output
        print("🔍 Validating daily tasks JSON output with Pydantic")
        try:
            validated_results = extract_and_validate_json(raw_results, validate_daily_tasks_output)
            print("✅ Successfully validated daily tasks output")
            return validated_results.model_dump()
            
        except Exception as validation_error:
            print(f"❌ Validation failed for daily tasks: {str(validation_error)}")
            print(f"� Raw results preview: {str(raw_results)[:300]}...")
            raise ValueError(f"Failed to validate daily tasks output: {str(validation_error)}")
        
    except Exception as e:
        print(f"❌ Error in daily tasks generation workflow: {str(e)}")
        raise e


def run_update_planning_workflow(user_id: str, user_update_text: str):
    """
    Executes the update planning workflow when user provides feedback from dashboard.
    
    Args:
        user_id (str): User's UUID
        user_update_text (str): User's update/feedback text
    
    Returns:
        dict: Updated planning results with validated JSON
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import get_profiler_results, get_agent_results
        from .tasks import create_update_planning_task
        
        print(f"🔄 Starting update planning workflow for user {user_id}")
        
        # Get user data
        user_profile = get_profiler_results(user_id)
        carbon_analysis = get_agent_results(user_id)
        
        if not user_profile:
            raise ValueError("No user profile found. Agent 1 must be completed first.")
        if not carbon_analysis:
            raise ValueError("No carbon analysis found. Agent 2 must be completed first.")
        
        # Create planner agent
        planner_agent = create_planner_agent()
        
        # Create update planning task
        update_task = create_update_planning_task(
            planner_agent, 
            user_profile, 
            carbon_analysis, 
            {},  # benchmark_results placeholder
            user_update_text
        )
        
        # Form the crew and execute
        print("🚀 Executing update planning workflow")
        crew = Crew(
            agents=[planner_agent],
            tasks=[update_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        raw_results = crew.kickoff()
        
        # Validate and parse JSON output
        print("🔍 Validating update planning JSON output with Pydantic")
        try:
            validated_results = extract_and_validate_json(raw_results, validate_update_planner_output)
            print("✅ Successfully validated update planning output")
            return validated_results.model_dump()
            
        except Exception as validation_error:
            print(f"❌ Validation failed for update planning: {str(validation_error)}")
            print(f"� Raw results preview: {str(raw_results)[:300]}...")
            raise ValueError(f"Failed to validate update planning output: {str(validation_error)}")
        
    except Exception as e:
        print(f"❌ Error in update planning workflow: {str(e)}")
        raise e