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

## Agent 1: User Profiler Agent
# This agent analyzes user onboarding data, extracts insights from additional_info,
# and creates an enriched profile with key carbon reduction levers and narrative summary

def create_profiler_agent():
    """Creates the User Profiler Agent for data analysis and profile enrichment"""
    
    return Agent(
        role="Senior User Profiler and Sustainability Data Analyst",
        goal="Analyze user onboarding data, extract insights from additional text, and create an enriched "
             "user profile with structured categories, key carbon reduction levers, and a narrative summary. "
             "Focus on identifying the most impactful areas for carbon footprint reduction.",
        backstory="You are a behavioral sustainability expert with advanced pattern recognition skills. "
                 "You excel at analyzing user lifestyle data to create comprehensive profiles that highlight "
                 "key carbon reduction opportunities. Your specialty is restructuring complex user data into "
                 "clear categories (demographics, lifestyle habits, consumption patterns, psychographic insights) "
                 "and identifying the 4-6 most impactful levers for carbon reduction. You also extract meaningful "
                 "insights from user's additional comments and create compelling narrative summaries that capture "
                 "their lifestyle, motivations, and personal context in 70-90 words.",
        verbose=False,
        allow_delegation=False,
        llm="openai/gpt-4.1-nano-2025-04-14",
        tools=[],
        max_iter=1,
        max_execution_time=120,
    )


## ====================================
##      Agent 2 - The Analyst
## ====================================
# This agent is responsible for calculating emissions and fetching benchmark data.


# Instantiate tools
calculate_emissions_tool = CalculateEmissionsTool()
fetch_benchmark_data_tool = FetchBenchmarkDataTool()


def create_analyst_agent():
    """Creates the Sustainability Analyst Agent"""
    
    return Agent(
        role="Senior Quantitative Insight Specialist",
        
        goal="Analyze enriched user profiles to calculate precise carbon footprints, validate key reduction levers, " \
        "and generate personalized insights that connect emissions data with user psychology. " \
        "Focus on actionable recommendations aligned with user motivations and barriers.",
        
        backstory="You are an expert carbon analyst who specializes in translating complex emissions data into " \
        "personalized, actionable insights. You excel at validating reduction opportunities and creating " \
        "psychologically-informed recommendations that resonate with individual users' motivations and overcome their barriers.",
       
        verbose=False,  # Disable verbose to avoid showing thinking
        allow_delegation=False,
        
        llm="openai/gpt-4.1-nano-2025-04-14",
        tools=[],  # Remove tools that might cause thinking loops
        max_iter=1,  # Force single iteration
        max_execution_time=120,  # Increased timeout for complex analysis
    )


## Agent 3:
# Weekly Action Planner Agent

def create_planner_agent():
    """Creates the Weekly Action Planner Agent"""
    
    return Agent(
        role="Personal Sustainability Challenge Planner & Action Coach",
        goal="Review enriched user profiles and carbon analysis to generate 6 hyper personalized, "
             "achievable sustainability challenges (3 easy + 2 medium + 1 hard). Generate additional daily tasks "
             "when users complete 2 easy + 2 medium challenges to maintain momentum and build sustainable habits.",
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