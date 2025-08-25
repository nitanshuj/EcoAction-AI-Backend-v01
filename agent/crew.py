# crew.py
from crewai import Crew, Process
from .agents import create_profiler_agent, create_analyst_agent, create_planner_agent
from .tasks import create_profiling_task, create_calculation_task, create_benchmarking_task, create_weekly_planning_task, create_update_planning_task, create_daily_tasks_generation_task

def create_complete_crew(user_data):
    """Creates and runs the complete 3-agent crew with sequential tasks"""
    
    # Create agents
    profiler_agent = create_profiler_agent()
    analyst_agent = create_analyst_agent()
    planner_agent = create_planner_agent()
    
    # Create tasks - sequential workflow
    profiling_task = create_profiling_task(profiler_agent, user_data)
    calculation_task = create_calculation_task(analyst_agent, user_data)
    benchmarking_task = create_benchmarking_task(analyst_agent, user_data, calculation_task)
    planning_task = create_weekly_planning_task(planner_agent, user_data, calculation_task, benchmarking_task)
    
    # Form the crew with sequential process
    crew = Crew(
        agents=[profiler_agent, analyst_agent, planner_agent],
        tasks=[profiling_task, calculation_task, benchmarking_task, planning_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    return crew

def create_analyst_crew(user_data):
    """Creates and runs the analyst crew (legacy - for backwards compatibility)"""
    
    # Create agents
    analyst_agent = create_analyst_agent()
    planner_agent = create_planner_agent()
    
    # Create tasks
    calculation_task = create_calculation_task(analyst_agent, user_data)
    benchmarking_task = create_benchmarking_task(analyst_agent, user_data, calculation_task)
    planning_task = create_weekly_planning_task(planner_agent, user_data, calculation_task, benchmarking_task)
    
    # Form the crew with sequential process
    crew = Crew(
        agents=[analyst_agent, planner_agent],
        tasks=[calculation_task, benchmarking_task, planning_task],
        process=Process.sequential,
        verbose=False,
        memory=False
    )
    
    return crew

def run_complete_workflow(user_data):
    """Executes the complete 3-agent workflow including profiler"""
    
    crew = create_complete_crew(user_data)
    results = crew.kickoff()
    
    return results

def run_analyst_workflow(user_data):
    """Executes the complete analyst workflow"""
    
    crew = create_analyst_crew(user_data)
    results = crew.kickoff()
    
    return results

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