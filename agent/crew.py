# crew.py
from crewai import Crew, Process
from .agents import create_profiler_agent, create_analyst_agent, create_planner_agent
from .tasks import create_profiling_task, create_analyst_task, create_benchmarking_task, create_weekly_planning_task, create_update_planning_task, create_feedback_aware_planning_task
import json
import re





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
    planning_task = create_weekly_planning_task(planner_agent, user_data)
    
    # Form the crew with sequential process
    crew = Crew(
        agents=[analyst_agent, planner_agent],
        tasks=[analyst_task, benchmarking_task, planning_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    return crew


# Agent 3 - Planner Agent Workflow
# =========================================================

def extract_and_validate_json(raw_output, validator_func):
    """
    Extract JSON from raw output and validate using Pydantic models.
    Handles multiple JSON extraction strategies with improved error handling.
    """
    try:
        print(f"🔍 Attempting to validate output type: {type(raw_output)}")

        if isinstance(raw_output, dict):
            try:
                validated_output = validator_func(raw_output)
                print("✅ Successfully validated dictionary input")
                return validated_output
            except Exception as e:
                print(f"❌ Dictionary validation failed: {str(e)}")
                raise ValueError(f"Dictionary validation failed: {str(e)}")

        raw_str = str(raw_output).strip()
        print(f"🔍 Attempting to extract JSON from string (length: {len(raw_str)})")

        try:
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
    """Validate that challenges have exactly the right difficulty distribution (4 challenges: 2 easy + 1 medium + 1 hard)"""
    if len(challenges) != 4:
        raise ValueError(f"Must have exactly 4 challenges, got {len(challenges)}")

    difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
    for challenge in challenges:
        difficulty = challenge.get('difficulty', '').lower()
        if difficulty in difficulty_counts:
            difficulty_counts[difficulty] += 1
        else:
            raise ValueError(f"Invalid difficulty level: {difficulty}")

    if difficulty_counts["easy"] != 2:
        raise ValueError(f"Must have exactly 2 easy challenges, got {difficulty_counts['easy']}")
    if difficulty_counts["medium"] != 1:
        raise ValueError(f"Must have exactly 1 medium challenge, got {difficulty_counts['medium']}")
    if difficulty_counts["hard"] != 1:
        raise ValueError(f"Must have exactly 1 hard challenge, got {difficulty_counts['hard']}")

    return True

def run_planner_workflow(user_id: str, test_data=None):
    """
    Executes the basic planner workflow (Agent 3) for initial challenge generation.
    
    Args:
        user_id (str): User's UUID
        test_data: Optional test data for development
    
    Returns:
        str: Raw text output from Agent 3
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import get_complete_user_data_with_score
        
        print(f"🔄 Starting planner workflow for user {user_id}")
        
        # Get complete user data (combined profile + carbon analysis)
        if test_data:
            user_complete_data = test_data  # Use test data if provided
            print("📋 Using provided test data")
        else:
            user_complete_data = get_complete_user_data_with_score(user_id)
            print("📋 Fetched complete user data with scores from database")
        
        if not user_complete_data:
            raise ValueError("No complete user data found. Agent 1 and 2 must be completed first.")
        
        # Create planner agent
        planner_agent = create_planner_agent()
        
        # Create planning task
        planning_task = create_weekly_planning_task(planner_agent, user_complete_data)
        
        # Form the crew and execute
        print("🚀 Executing planner workflow")
        crew = Crew(
            agents=[planner_agent],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=True,
            memory=False
        )
        
        raw_results = crew.kickoff()

        # Get the text output
        raw_output = None
        if hasattr(raw_results, 'raw'):
            raw_output = raw_results.raw
        elif hasattr(raw_results, 'tasks_output') and raw_results.tasks_output:
            task_output = raw_results.tasks_output[0]
            if hasattr(task_output, 'raw'):
                raw_output = task_output.raw
        else:
            raw_output = str(raw_results)        
        
        return raw_output
        
    except Exception as e:
        print(f"❌ Error in planner workflow: {str(e)}")
        raise e





def run_feedback_aware_planning_workflow(user_id: str, raw_feedback: str = None, test_data=None):
    """
    Executes the feedback-aware planning workflow using the Two-Tiered Memory System.

    Args:
        user_id (str): User's UUID
        raw_feedback (str): Optional new feedback from user
        test_data: Optional test data for development

    Returns:
        dict: Planning results with feedback adaptation and validated JSON
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import (
            get_complete_user_data_with_score,
            get_user_feedback_history, save_feedback_and_process
        )
        from .tasks import create_feedback_aware_planning_task

        # Step 1: Process new feedback if provided (skip for test data)
        if raw_feedback and not test_data:
            print(f"🔄 Processing new feedback for user {user_id}")
            feedback_success = save_feedback_and_process(user_id, raw_feedback)
            if not feedback_success:
                print("⚠️ Warning: Failed to save feedback, continuing with existing data")

        # Step 2: Get complete user data (combined profile + carbon analysis)
        if test_data:
            user_complete_data = test_data  # Use test data if provided
            print("📋 Using provided test data")
        else:
            print("📋 Fetching complete user data with scores")
            user_complete_data = get_complete_user_data_with_score(user_id)

        if not user_complete_data:
            raise ValueError("No complete user data found. Agent 1 and 2 must be completed first.")
        
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
            user_complete_data,  # Using complete data instead of separate profile and carbon analysis
            # {},  # benchmark_results placeholder (not needed with complete data)
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
        
        # Get the text output
        raw_output = None
        if hasattr(raw_results, 'raw'):
            raw_output = raw_results.raw
        elif hasattr(raw_results, 'tasks_output') and raw_results.tasks_output:
            task_output = raw_results.tasks_output[0]
            if hasattr(task_output, 'raw'):
                raw_output = task_output.raw
        else:
            raw_output = str(raw_results)
        
        print("="*80)
        print(f"📋 Raw text output:\n{raw_output}")
        print("="*80)
        
        # Convert text to JSON using feedback-aware parser
        from .utils import parse_agent3_text_output
        plan_data = parse_agent3_text_output(raw_output, task_type="feedback_aware")
        
        print("✅ Successfully converted text to JSON")
        print(f"🎯 Generated {len(plan_data.get('challenges', []))} challenges")
        
        # Return raw text output for consistency with dashboard expectations
        return raw_output
            
    except Exception as e:
        print(f"❌ Error in feedback-aware planning workflow: {str(e)}")
        raise e






# REMOVED: Daily task generation workflow no longer needed
# (Using only weekly planning with easy/medium/hard challenges)




def run_update_planning_workflow(user_id: str, user_update_text: str, test_data=None):
    """
    Executes the update planning workflow when user provides feedback from dashboard.

    Args:
        user_id (str): User's UUID
        user_update_text (str): User's update/feedback text
        test_data: Optional test data for development

    Returns:
        dict: Updated planning results with validated JSON
    """
    try:
        # Import here to avoid circular imports
        from data_model.database import get_complete_user_data_with_score
        from .tasks import create_update_planning_task

        print(f"🔄 Starting update planning workflow for user {user_id}")

        # Get complete user data (combined profile + carbon analysis)
        if test_data:
            user_complete_data = test_data  # Use test data if provided
            print("📋 Using provided test data")
        else:
            user_complete_data = get_complete_user_data_with_score(user_id)

        if not user_complete_data:
            raise ValueError("No complete user data found. Agent 1 and 2 must be completed first.")
        
        # Create planner agent
        planner_agent = create_planner_agent()
        
        # Create update planning task
        update_task = create_update_planning_task(
            planner_agent, 
            user_complete_data,  # Using complete data instead of separate profile and carbon analysis
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
        
        # Get the text output
        raw_output = None
        if hasattr(raw_results, 'raw'):
            raw_output = raw_results.raw
        elif hasattr(raw_results, 'tasks_output') and raw_results.tasks_output:
            task_output = raw_results.tasks_output[0]
            if hasattr(task_output, 'raw'):
                raw_output = task_output.raw
        else:
            raw_output = str(raw_results)
        
        print("="*80)
        print(f"📋 Raw text output:\n{raw_output}")
        print("="*80)
        
        # Convert text to JSON using update planning parser
        from .utils import parse_agent3_text_output
        update_plan_data = parse_agent3_text_output(raw_output, task_type="update_planning", user_update_text=user_update_text)
        
        print("✅ Successfully converted text to JSON")
        print(f"🎯 Generated {len(update_plan_data.get('challenges', []))} challenges")
        
        # Return raw text output for consistency with dashboard expectations
        return raw_output
        
    except Exception as e:
        print(f"❌ Error in update planning workflow: {str(e)}")
        raise e