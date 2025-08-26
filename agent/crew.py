# crew.py
from crewai import Crew, Process
from .agents import create_profiler_agent, create_analyst_agent, create_planner_agent
from .tasks import create_profiling_task, create_analyst_task, create_benchmarking_task, create_weekly_planning_task, create_update_planning_task, create_daily_tasks_generation_task
import json


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
    
    # Create planner agent
    planner_agent = create_planner_agent()
    
    # Create update planning task
    update_task = create_update_planning_task(planner_agent, user_data, carbon_results, benchmark_results, user_update_text)
    
    # Form the crew with single planner agent
    crew = Crew(
        agents=[planner_agent],
        tasks=[update_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    return crew

def run_update_planning_workflow(user_data, carbon_results, benchmark_results, user_update_text):
    """Executes the update planning workflow when user provides feedback from dashboard"""
    
    crew = create_update_planner_crew(user_data, carbon_results, benchmark_results, user_update_text)
    results = crew.kickoff()
    
    return results

def create_daily_tasks_crew(user_data, carbon_results, benchmark_results, completed_tasks):
    """Creates a crew for generating daily tasks when user completes 3 out of 5 tasks"""
    
    # Create planner agent
    planner_agent = create_planner_agent()
    
    # Create daily tasks generation task
    daily_task = create_daily_tasks_generation_task(planner_agent, user_data, carbon_results, benchmark_results, completed_tasks)
    
    # Form the crew with single planner agent
    crew = Crew(
        agents=[planner_agent],
        tasks=[daily_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    return crew

def run_daily_tasks_generation_workflow(user_data, carbon_results, benchmark_results, completed_tasks):
    """Executes the daily tasks generation workflow when user completes 3 out of 5 challenges"""
    
    crew = create_daily_tasks_crew(user_data, carbon_results, benchmark_results, completed_tasks)
    results = crew.kickoff()
    
    return results