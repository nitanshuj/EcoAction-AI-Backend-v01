#
#
#
import os
import json
import dotenv
from crewai import Agent
from .utils import CalculateEmissionsTool, FetchBenchmarkDataTool

# Load environment variables from .env file
dotenv.load_dotenv()

# Set environment variables for AIMLAPI
os.environ["OPENAI_API_BASE"] = "https://api.aimlapi.com/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("AI_ML_API_KEY")

## Agent 1: 
# 

def create_profiler_agent():
    """Creates the User Profiler Agent for data analysis and enrichment"""
    
    return Agent(
        role="Senior User Profiler and Dynamic Sustainability Data Analyst",
        goal="Conduct deep, personalized analysis of user lifestyle patterns to identify unique carbon impact areas. "
             "Generate contextually relevant, varied questions that adapt to each user's specific situation. "
             "Create engaging, non-repetitive conversations that uncover actionable sustainability insights.",
        backstory="You are a behavioral sustainability expert with advanced pattern recognition skills. "
                 "You excel at reading between the lines of user responses to understand their true lifestyle patterns. "
                 "Your specialty is crafting personalized, context-aware questions that feel natural and relevant to each user. "
                 "You never ask generic questions - every question is tailored to the specific user's situation and designed to "
                 "uncover the most impactful areas for carbon reduction. You understand that engaged users provide better data, "
                 "so you make every interaction feel personalized and meaningful. You're also skilled at varying your approach "
                 "to keep conversations fresh and avoid repetitive patterns.",
        verbose=False,
        allow_delegation=False,
        llm="openai/gpt-4.1-nano-2025-04-14",
        tools=[],  # Can add conversation management tools later
        max_iter=1,
        max_execution_time=60,
    )


## Agent 2:
# lib/agents/analyst_agent/agent.py

# Instantiate tools
calculate_emissions_tool = CalculateEmissionsTool()
fetch_benchmark_data_tool = FetchBenchmarkDataTool()


def create_analyst_agent():
    """Creates the Sustainability Analyst Agent"""
    
    return Agent(
        role="Senior Sustainability Analyst and Carbon Footprint Calculator",
        goal="Calculate precise carbon footprints, categorize impact areas, generate sustainability scores (0-10), " \
        "create fun comparison facts against regional/national benchmarks, and deliver actionable insights " \
        "for carbon reduction. Focus on top 2-3 impact categories and clear, data-driven recommendations.",
        backstory="You are an expert data scientist specializing in carbon footprint calculations, environmental benchmarking, " \
        "and sustainability scoring. You excel at breaking down complex emissions data into understandable categories, " \
        "creating engaging comparisons with regional averages, and developing practical sustainability scores. " \
        "Your analysis helps users understand their environmental impact through fun facts and clear priority areas for improvement.",
        verbose=False,  # Disable verbose to avoid showing thinking
        allow_delegation=False,
        llm="openai/gpt-4.1-nano-2025-04-14",
        tools=[],  # Remove tools that might cause thinking loops
        max_iter=1,  # Force single iteration
        max_execution_time=60,  # Shorter timeout
    )


## Agent 3:
# Weekly Action Planner Agent

def create_planner_agent():
    """Creates the Weekly Action Planner Agent"""
    
    return Agent(
        role="Personal Sustainability Planner and Action Coach",
        goal="Review enriched user profiles and carbon analysis to generate 5 highly personalized, "
             "achievable sustainability challenges (3 daily + 2 long-term). Generate additional daily tasks "
             "when users complete 3 out of 5 challenges to maintain momentum and build sustainable habits.",
        backstory="You are an expert personal sustainability coach who specializes in creating structured, "
                 "achievable action plans with both immediate daily habits and longer-term goals. You excel at "
                 "analyzing user data from profiling and carbon analysis to craft specific, time-bound challenges "
                 "that build momentum. You understand how to balance daily habit-building with longer-term "
                 "sustainability projects, and you reward user progress with additional challenges to keep them "
                 "engaged. Your specialty is making sustainability feel manageable and rewarding for each "
                 "individual user, while ensuring actions are trackable and lead to measurable environmental impact.",
        verbose=False,
        allow_delegation=False,
        llm="openai/gpt-4.1-nano-2025-04-14",
        tools=[],
        max_iter=1,
        max_execution_time=120,  # Increased from 60 to 120 seconds
    )