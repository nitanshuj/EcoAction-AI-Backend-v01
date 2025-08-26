# agent/models.py
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

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

def validate_enriched_user_data(json_data: dict) -> EnrichedUserData:
    """Validate the complete enriched user data using Pydantic"""
    try:
        return EnrichedUserData.model_validate(json_data)
    except Exception as e:
        raise ValueError(f"Invalid enriched user data format: {str(e)}")
