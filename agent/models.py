# agent/models.py
"""
This module defines Pydantic data models for EcoAction AI agents. It structures user profile data, carbon footprint analysis, and legacy Q&A formats, enabling robust validation and serialization for agent communication and downstream analytics.
Classes:
    Demographics: Captures user's basic demographic and household information.
    DietInfo: Represents dietary habits and food waste patterns.
    TransportationInfo: Details primary transportation modes and commute patterns.
    EnergyUsage: Describes home energy sources and conservation habits.
    LifestyleHabits: Aggregates diet, transportation, and energy usage data.
    ConsumptionPatterns: Summarizes shopping, plastic use, and recycling behaviors.
    PsychographicInsights: Lists motivations, barriers, and goals for sustainability.
    ProfilerAgentOutput: Output schema for Agent 1 (Profiler), including narrative and actionable levers.
    CategoryBreakdown: Annual carbon emissions by category.
    RegionalComparison: Compares user emissions to local/regional averages.
    KeyLeverValidation: Validates impact of suggested carbon reduction levers.
    PsychographicInsight: Personalized insight based on user psychology.
    AnalystAgentOutput: Output schema for Agent 2 (Analyst), including scores, breakdowns, and insights.
    FollowUpQuestion: Legacy model for follow-up questions.
    QuestionAnswer: Legacy model for Q&A responses.
    EnrichedUserData: Aggregates all user data, including analysis and Q&A.
Functions:
    validate_profiler_output(json_data: dict) -> ProfilerAgentOutput:
        Validates and parses profiler agent output using Pydantic models.
    validate_analyst_output(json_data: dict) -> AnalystAgentOutput:
        Validates and parses analyst agent output using Pydantic models.
    validate_enriched_user_data(json_data: dict) -> EnrichedUserData:
        Validates and parses complete enriched user data using Pydantic models.
"""
#
# This file is responsible for 
#
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

import json, re,ast
from typing import Union
from .utils import parse_text_to_json, load_challenges_metadata

# New simplified models for the restructured output
class Demographics(BaseModel):
    location: str = Field(..., description="City, Country")
    climate: str = Field(..., description="Climate type")
    household_size: int = Field(..., description="Number of people in household")
    home_type: str = Field(..., description="Type of home")
    ownership: str = Field(..., description="Own or Rent")

class DietInfo(BaseModel):
    type: str = Field(..., description="Diet type")
    meat_frequency: str = Field(..., description="Meat consumption frequency")
    food_waste: str = Field(..., description="Food waste level")

class TransportationInfo(BaseModel):
    primary_mode: str = Field(..., description="Main transportation mode")
    car_type: str = Field(..., description="Type of vehicle")
    commute_details: str = Field(..., description="Commute distance/frequency details")

class EnergyUsage(BaseModel):
    heating_source: str = Field(..., description="Primary heating source")
    ac_usage: str = Field(..., description="Air conditioning usage frequency")
    energy_conservation_habits: str = Field(..., description="Energy conservation level")

class LifestyleHabits(BaseModel):
    diet: DietInfo = Field(..., description="Diet-related information")
    transportation: TransportationInfo = Field(..., description="Transportation information")
    energy_usage: EnergyUsage = Field(..., description="Energy usage patterns")

class ConsumptionPatterns(BaseModel):
    shopping_frequency: str = Field(..., description="Shopping frequency")
    plastic_usage: str = Field(..., description="Single-use plastic usage level")
    recycling_habit: str = Field(..., description="Recycling habits")

class PsychographicInsights(BaseModel):
    motivations: List[str] = Field(..., description="Primary motivations for sustainability")
    barriers: List[str] = Field(..., description="Main challenges/barriers")
    goals: List[str] = Field(..., description="Improvement goals")

class ProfilerAgentOutput(BaseModel):
    demographics: Demographics = Field(..., description="Demographic information")
    lifestyle_habits: LifestyleHabits = Field(..., description="Lifestyle and habit information")
    consumption_patterns: ConsumptionPatterns = Field(..., description="Consumption and shopping patterns")
    psychographic_insights: PsychographicInsights = Field(..., description="Motivations, barriers, and goals")
    key_levers: List[str] = Field(..., description="4-6 specific actionable carbon reduction levers")
    narrative_text: str = Field(..., description="70-90 word narrative summary")

# Agent 2 (Analyst) Output Models
class CategoryBreakdown(BaseModel):
    transportation_kg: float = Field(..., description="Annual transportation emissions in kg CO2")
    diet_kg: float = Field(..., description="Annual diet emissions in kg CO2")
    home_energy_kg: float = Field(..., description="Annual home energy emissions in kg CO2")
    shopping_kg: float = Field(..., description="Annual shopping/consumption emissions in kg CO2")
    digital_footprint_kg: float = Field(..., description="Annual digital emissions in kg CO2")
    other_kg: float = Field(..., description="Other annual emissions in kg CO2")

class RegionalComparison(BaseModel):
    user_location: str = Field(..., description="User's location from profile")
    local_average_kg: float = Field(..., description="Local/regional average annual emissions")
    comparison_status: str = Field(..., description="above/below/equal to average")
    percentage_difference: float = Field(..., description="Percentage above or below average")

class KeyLeverValidation(BaseModel):
    lever: str = Field(..., description="The key lever identified by Agent 1")
    validated: bool = Field(..., description="Whether this lever is confirmed as high-impact")
    impact_category: str = Field(..., description="Which emission category this lever affects")
    potential_reduction_kg: float = Field(..., description="Estimated annual kg CO2 reduction potential")
    validation_reason: str = Field(..., description="Explanation of why this lever is/isn't high-impact")

class PsychographicInsight(BaseModel):
    insight_text: str = Field(..., description="Personalized insight incorporating user's motivations/barriers")
    related_motivation: str = Field(..., description="Which user motivation this insight relates to")
    addresses_barrier: str = Field(..., description="Which user barrier this insight addresses")
    actionable_next_step: str = Field(..., description="Specific next step aligned with user psychology")

class AnalystAgentOutput(BaseModel):
    total_carbon_footprint_kg: float = Field(..., description="Total annual carbon footprint in kg CO2")
    total_carbon_footprint_tonnes: float = Field(..., description="Total annual carbon footprint in tonnes CO2")
    category_breakdown: CategoryBreakdown = Field(..., description="Detailed breakdown by emission category")
    top_impact_categories: List[str] = Field(..., description="Top 2-3 highest impact categories")
    sustainability_score: float = Field(..., description="Overall sustainability score (0-10 scale)")
    score_category: str = Field(..., description="Score category: Highly Sustainable/Below Average/Above Average/High Impact")
    regional_comparison: RegionalComparison = Field(..., description="Comparison with regional/national averages")
    key_lever_validations: List[KeyLeverValidation] = Field(..., description="Validation of Agent 1's key levers")
    psychographic_insights: List[PsychographicInsight] = Field(..., description="Personalized insights based on user psychology")
    fun_comparison_facts: List[str] = Field(..., description="Engaging comparison facts")
    priority_reduction_areas: List[str] = Field(..., description="Top priority areas for emission reduction")
    calculation_method: str = Field(..., description="Brief description of calculation methodology")
    data_confidence: str = Field(..., description="Confidence level: high/medium/low")

# Legacy models for backward compatibility (if needed)
class FollowUpQuestion(BaseModel):
    id: str = Field(..., description="Unique identifier for the question")
    question: str = Field(..., description="The actual question text")
    category: str = Field(..., description="Category: transportation/energy/diet/consumption/digital")
    importance: str = Field(..., description="Importance level: high/medium")
    expected_answer_type: str = Field(..., description="Expected answer type: number/frequency/amount/description")

class QuestionAnswer(BaseModel):
    question_id: str = Field(..., description="ID of the question")
    question: str = Field(..., description="The question text")
    answer: str = Field(..., description="User's answer")
    skipped: bool = Field(default=False, description="Whether user skipped this question")

class EnrichedUserData(BaseModel):
    user_id: str = Field(..., description="User's unique identifier")
    original_onboarding_data: Dict[str, Any] = Field(..., description="Original form data")
    profiler_analysis: ProfilerAgentOutput = Field(..., description="Agent 1 analysis results")
    qa_responses: List[QuestionAnswer] = Field(default=[], description="Q&A session responses")
    profile_complete: bool = Field(default=False, description="Whether profiling is complete")
    
    class Config:
        extra = "allow"  # Allow additional fields for flexibility

def validate_profiler_output(json_data: dict) -> ProfilerAgentOutput:
    """Validate the profiler agent output using Pydantic"""
    try:
        return ProfilerAgentOutput.model_validate(json_data)
    except Exception as e:
        raise ValueError(f"Invalid profiler output format: {str(e)}")

def validate_analyst_output(json_data: dict) -> AnalystAgentOutput:
    """Validate the analyst agent output using Pydantic"""
    try:
        return AnalystAgentOutput.model_validate(json_data)
    except Exception as e:
        raise ValueError(f"Invalid analyst output format: {str(e)}")

# Agent 3 (Planner) Output Models
class Challenge(BaseModel):
    id: str = Field(..., description="Unique identifier for the challenge")
    title: str = Field(..., description="Catchy, actionable title")
    description: str = Field(..., description="Specific action description")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, or hard")
    category: str = Field(..., description="Category: diet/transport/energy/waste/consumption")
    steps: List[str] = Field(..., description="Step-by-step instructions")
    co2_savings_kg: float = Field(..., description="Estimated CO2 savings in kg")
    time_required: str = Field(..., description="Time commitment required")
    deadline: str = Field(..., description="When to complete by")
    success_metrics: str = Field(..., description="How to measure completion")
    motivation: str = Field(..., description="Why this matters for the user")
    completed: bool = Field(default=False, description="Completion status")
    
    class Config:
        extra = "forbid"  # Strict validation
        validate_assignment = True

class PlannerAgentOutput(BaseModel):
    week_focus: str = Field(..., description="Main theme for the week")
    priority_area: str = Field(..., description="Top priority emission category")
    challenges: List[Challenge] = Field(..., description="Exactly 6 challenges (3 easy + 2 medium + 1 hard)")
    total_potential_savings: float = Field(..., description="Total potential CO2 savings in kg")
    motivation_message: str = Field(..., description="Encouraging message tailored to user's goals")
    
    class Config:
        extra = "forbid"  # Strict validation
        validate_assignment = True
    
    @classmethod
    def validate_challenge_structure(cls, challenges_data):
        """Validate challenge count and difficulty distribution"""
        if not isinstance(challenges_data, list):
            raise ValueError("Challenges must be a list")
        
        if len(challenges_data) != 6:
            raise ValueError(f"Must have exactly 6 challenges, got {len(challenges_data)}")
        
        difficulty_counts = {"easy": 0, "medium": 0, "hard": 0}
        
        for i, challenge in enumerate(challenges_data):
            if not isinstance(challenge, dict):
                raise ValueError(f"Challenge {i+1} must be a dictionary")
            
            difficulty = challenge.get('difficulty', '').lower().strip()
            if difficulty not in difficulty_counts:
                raise ValueError(f"Challenge {i+1} has invalid difficulty '{difficulty}'. Must be 'easy', 'medium', or 'hard'")
            
            difficulty_counts[difficulty] += 1
        
        if difficulty_counts["easy"] != 3:
            raise ValueError(f"Must have exactly 3 easy challenges, got {difficulty_counts['easy']}")
        if difficulty_counts["medium"] != 2:
            raise ValueError(f"Must have exactly 2 medium challenges, got {difficulty_counts['medium']}")
        if difficulty_counts["hard"] != 1:
            raise ValueError(f"Must have exactly 1 hard challenge, got {difficulty_counts['hard']}")
        
        return challenges_data

class FeedbackAwarePlannerOutput(BaseModel):
    week_focus: str = Field(..., description="Adapted theme for this week based on user feedback")
    priority_area: str = Field(..., description="Top priority emission category")
    challenges: List[Challenge] = Field(..., description="Exactly 6 challenges adapted to feedback")
    total_potential_savings: float = Field(..., description="Total potential CO2 savings in kg")
    motivation_message: str = Field(..., description="Personalized encouragement addressing feedback")
    feedback_adaptation_notes: str = Field(..., description="How the plan was adapted based on feedback")
    
    class Config:
        extra = "forbid"  # Strict validation
        validate_assignment = True

class DailyTask(BaseModel):
    id: str = Field(..., description="Unique identifier for the daily task")
    title: str = Field(..., description="Short daily action title (max 80 chars)")
    action: str = Field(..., description="Simple daily action to take (max 80 chars)")
    why: str = Field(..., description="Why this daily habit matters (max 80 chars)")
    steps: List[str] = Field(..., description="Quick steps to complete")
    co2_savings: float = Field(..., description="Daily CO2 savings in kg")
    difficulty: str = Field(default="easy", description="Difficulty level")
    task_type: str = Field(default="daily", description="Task type")
    frequency: str = Field(default="daily", description="Frequency of task")
    completed: bool = Field(default=False, description="Completion status")
    
    class Config:
        extra = "forbid"  # Strict validation
        validate_assignment = True

class DailyTasksOutput(BaseModel):
    congratulations_message: str = Field(..., description="Celebration message for completing tasks")
    daily_focus: str = Field(..., description="Theme for these daily habits")
    new_daily_tasks: List[DailyTask] = Field(..., description="Exactly 3 new daily tasks")
    motivation: str = Field(..., description="Encouragement for daily habit building")
    
    class Config:
        extra = "forbid"  # Strict validation
        validate_assignment = True
    
    @classmethod
    def validate_task_structure(cls, tasks_data):
        """Validate that there are exactly 3 daily tasks"""
        if not isinstance(tasks_data, list):
            raise ValueError("Tasks must be a list")
        
        if len(tasks_data) != 3:
            raise ValueError(f"Must have exactly 3 daily tasks, got {len(tasks_data)}")
        
        return tasks_data

class UpdatePlannerOutput(BaseModel):
    update_analysis: str = Field(..., description="Summary of what user shared and implications")
    planning_adjustments: str = Field(..., description="How the plan was modified based on their update")
    week_focus: str = Field(..., description="Adapted theme for this week based on user feedback")
    challenges: List[Challenge] = Field(..., description="Exactly 6 updated challenges")
    total_potential_savings: float = Field(..., description="Total potential CO2 savings in kg")
    motivation_message: str = Field(..., description="Personalized encouragement addressing their update")
    future_planning_notes: str = Field(..., description="Insights to remember for next planning")
    
    class Config:
        extra = "forbid"  # Strict validation
        validate_assignment = True



def clean_json_string(raw_json: str) -> str:
    """Clean JSON string by removing common formatting issues"""
    # Remove markdown code blocks
    raw_json = re.sub(r'```json\s*', '', raw_json)
    raw_json = re.sub(r'```\s*', '', raw_json)
    
    # Remove trailing commas before closing brackets
    raw_json = re.sub(r',\s*}', '}', raw_json)
    raw_json = re.sub(r',\s*]', ']', raw_json)
    
    return raw_json.strip()

def extract_json_from_text(text: str) -> dict:
    """
    Bulletproof function to extract a JSON object from a string.
    It handles JSON, Python dict strings, and markdown code blocks.
    """
    # 1. Aggressively find a JSON-like object using regex.
    # This pattern looks for the outermost curly braces.
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if not match:
        raise ValueError(f"No JSON object found in text. Preview: {text[:200]}...")

    json_str = match.group(0)

    # 2. Try to parse it as standard JSON.
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # 3. If standard parsing fails, it might be a Python dict string.
        # Safely evaluate it as a Python literal.
        try:
            py_dict = ast.literal_eval(json_str)
            # Convert the Python dict to a JSON-compliant dict before returning
            return json.loads(json.dumps(py_dict))
        except (ValueError, SyntaxError, MemoryError) as e:
            # If all parsing attempts fail, raise the final error.
            raise ValueError(f"Failed to parse JSON or Python dict from text. Preview: {json_str[:200]}...") from e

# ------------------------------------------------------------------------------------------            

def validate_profiler_output(json_data: Union[dict, str]) -> ProfilerAgentOutput:
    """Validate the profiler agent output using Pydantic"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        return ProfilerAgentOutput.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid profiler output format: {str(e)}")

def validate_analyst_output(json_data: Union[dict, str]) -> AnalystAgentOutput:
    """Validate the analyst agent output using Pydantic"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        return AnalystAgentOutput.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid analyst output format: {str(e)}")

def validate_planner_output(json_data: Union[dict, str]) -> PlannerAgentOutput:
    """Validate the planner agent output using Pydantic with enhanced validation"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        # Pre-validate challenge structure
        if 'challenges' in data:
            PlannerAgentOutput.validate_challenge_structure(data['challenges'])
        
        return PlannerAgentOutput.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid planner output format: {str(e)}")

def validate_feedback_aware_output(json_data: Union[dict, str]) -> FeedbackAwarePlannerOutput:
    """Validate the feedback-aware planner output using Pydantic"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        # Pre-validate challenge structure
        if 'challenges' in data:
            PlannerAgentOutput.validate_challenge_structure(data['challenges'])
        
        return FeedbackAwarePlannerOutput.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid feedback-aware planner output format: {str(e)}")

def validate_daily_tasks_output(json_data: Union[dict, str]) -> DailyTasksOutput:
    """Validate the daily tasks output using Pydantic"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        # Pre-validate task structure
        if 'new_daily_tasks' in data:
            DailyTasksOutput.validate_task_structure(data['new_daily_tasks'])
        
        return DailyTasksOutput.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid daily tasks output format: {str(e)}")

def validate_update_planner_output(json_data: Union[dict, str]) -> UpdatePlannerOutput:
    """Validate the update planner output using Pydantic"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        # Pre-validate challenge structure
        if 'challenges' in data:
            PlannerAgentOutput.validate_challenge_structure(data['challenges'])
        
        return UpdatePlannerOutput.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid update planner output format: {str(e)}")

def validate_enriched_user_data(json_data: Union[dict, str]) -> EnrichedUserData:
    """Validate the complete enriched user data using Pydantic"""
    try:
        # If it's already a dictionary, use it directly
        if isinstance(json_data, dict):
            data = json_data
        else:
            # Only extract from text if it's a string
            data = extract_json_from_text(json_data)
        
        return EnrichedUserData.model_validate(data)
    except Exception as e:
        raise ValueError(f"Invalid enriched user data format: {str(e)}")
