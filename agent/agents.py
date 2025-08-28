#
#
#
import os, json, dotenv
from crewai import Agent, LLM
from .tools import CalculateEmissionsTool, FetchBenchmarkDataTool
import google.generativeai as genai

# Load environment variables from .env file
dotenv.load_dotenv()

# Set environment variables for AIMLAPI (for Agents 1 & 2)
os.environ["OPENAI_API_BASE"] = "https://api.aimlapi.com/v1"
os.environ["OPENAI_API_KEY"] = os.getenv("AI_ML_API_KEY")

# Set environment variables for Gemini API (for Agent 3)
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# LLM Configuration for each agent
# Some agent options
# - "openai/gpt-4.1-nano-2025-04-14"
# - "gpt-4o-mini"
# - "openai/gpt-4.1-mini-2025-04-14"
# - "openai/gpt-5-nano-2025-08-07" - not working now
# - "openai/gpt-5-mini-2025-08-07"
# - ""


# # Google LLM Modes (Configuration)
# # --------------------------------
# def configure_gemini_llm(model="gemini-2.0-flash"):
#     return LLM(
#         model=model,
#         provider="google",
#         api_key=os.getenv("GOOGLE_API_KEY")
#     )
# llm_gemini_2_0_flash = configure_gemini_llm("gemini-2.0-flash") 
# llm_gemini_2_0_flash_lite = configure_gemini_llm("gemini-2.0-flash-lite")

# llm_gemini_2_0_flash_lite = genai.GenerativeModel("gemini-2.0-flash-lite")
# llm_gemini_2_0_flash = genai.GenerativeModel("gemini-2.0-flash")

# Open AI LLM Models
llm_gpt_4_1_nano = "openai/gpt-4.1-nano-2025-04-14"
llm_gpt_4_1_mini = "openai/gpt-4.1-mini-2025-04-14"
llm_gpt_5_nano = "openai/gpt-5-nano-2025-08-07"
llm_gpt_5_mini = "openai/gpt-5-mini-2025-08-07"

llm_agent_1_profiler = llm_gpt_4_1_nano
llm_agent_2_analyst = llm_gpt_4_1_nano
llm_agent_3_planner = llm_gpt_4_1_nano  # Using the more powerful mini model for Agent 3

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
        llm=llm_agent_1_profiler,
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
        
        goal="Analyze enriched user profiles to calculate precise carbon footprints, " \
        "validate key reduction levers, " \
        "and generate personalized insights that connect emissions data with user psychology. " \
        "",
        
        backstory="You are an expert carbon analyst who specializes in translating complex emissions data into " \
        "personalized, actionable insights. You excel at validating reduction opportunities and creating " \
        "psychologically-informed recommendations that resonate with individual users' motivations and overcome their barriers.",
       
        verbose=True,  # Disable verbose to avoid showing thinking
        allow_delegation=False,
        
        # llm=llm_agent_2_analyst,
        llm = LLM(
                model="openai/gpt-4.1-nano-2025-04-14",
                provider="openai",
                api_key=os.getenv("AI_ML_API_KEY"),
                base_url="https://api.aimlapi.com/v1",
                max_tokens=4064  # or higher
            ),
        tools=[],  # Remove tools that might cause thinking loops
        max_iter=2,  # Force single iteration
        max_execution_time=200,  # Increased timeout for complex analysis
    )


## Agent 3:
# Weekly Action Planner Agent

def create_planner_agent():
    """Creates the Weekly Action Planner Agent"""
    
    return Agent(
        role="Personal Sustainability Challenge Planner & Action Coach",
        goal="Review enriched user profiles (with carbon analysis, personal details) to generate 4 hyper personalized, achievable sustainability challenges "
             "The 4 challenges divided - 2 easy challenges + 1 medium challenge + 1 hard challenge. " \
             "Use premade challenge metadata as inspiration or selection, and generate new challenges when needed.",
        backstory="You are an expert personal sustainability coach who specializes in creating structured, "
                 "achievable action plans with both immediate daily habits and longer-term goals. "
                 "You excel at analyzing user data from profiling and carbon analysis to craft specific, time-bound challenges "
                 "that build momentum. You have access to a comprehensive database of proven sustainability challenges "
                 "that you can select from, adapt, or use as inspiration. You understand how to balance daily habit-building with longer-term "
                 "sustainability projects, and you reward user progress with additional challenges to keep them "
                 "engaged. Your specialty is making sustainability feel manageable and rewarding for each "
                 "individual user, while ensuring actions are trackable and lead to measurable environmental impact.",
        verbose=True,  # Enable verbose output
        allow_delegation=False,
        llm=llm_agent_3_planner,  # GPT 4.1 Mini - more powerful for complex tasks
        tools=[],
        max_iter=5,  # Increased from 3 to 5 to allow more retries
        max_execution_time=300,  # Increased from 180 to 300 seconds (5 minutes)
        step_callback=lambda step: print(f"🔄 Agent step: {step.action}") if hasattr(step, 'action') else None
    )