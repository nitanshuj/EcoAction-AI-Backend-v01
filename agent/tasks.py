# tasks.py
from crewai import Task
from .models import (
    ProfilerAgentOutput, 
    AnalystAgentOutput
)
import json
import os

from .utils import parse_text_to_json, load_challenges_metadata


## ========================================================================
##                           Agent 1 (Profiler) Task
## ========================================================================
def create_profiling_task(agent, user_data):
    """Creates the user profiling task to analyze data and generate enriched profile"""
    
    return Task(
        description=(
            "Analyze user's onboarding data, extract insights from additional_info text, and create an enriched "
            "user profile with key carbon reduction levers and a narrative summary.\n\n"
            
            "USER ONBOARDING DATA:\n"
            f"{user_data}\n\n"
            
            "TASK STEPS:\n"
            "1. RESTRUCTURE DATA: Organize user data into clear categories (demographics, lifestyle_habits, consumption_patterns, psychographic_insights)\n"
            "2. EXTRACT INSIGHTS: Process additional_info field to understand user's personal context and goals\n"
            "3. IDENTIFY KEY LEVERS: Find 4-6 specific, actionable areas with highest carbon reduction potential for this user\n"
            "4. CREATE NARRATIVE: Write 70-90 word narrative summarizing user's lifestyle, motivations, and context\n\n"
            
            "KEY LEVERS should be specific and actionable, such as:\n"
            "- 'Reduce car usage by 30%'\n"
            "- 'Switch to renewable energy'\n"
            "- 'Reduce meat consumption'\n"
            "- 'Improve home insulation'\n"
            "- 'Reduce food waste'\n"
            "- 'Use public transport more'\n\n"
            
            "NARRATIVE should include:\n"
            "- Living situation and location context\n"
            "- Transportation and commuting patterns\n"
            "- Diet and consumption habits\n"
            "- Personal motivations and barriers\n"
            "- Key lifestyle characteristics\n"
        ),
        expected_output=(
            "A valid JSON object with the complete restructured user profile:\n"
            "{\n"
            '  "demographics": {\n'
            '    "location": "City, Country",\n'
            '    "climate": "Climate type",\n'
            '    "household_size": number,\n'
            '    "home_type": "Type",\n'
            '    "ownership": "Own/Rent"\n'
            '  },\n'
            '  "lifestyle_habits": {\n'
            '    "diet": {\n'
            '      "type": "Diet type",\n'
            '      "meat_frequency": "Frequency",\n'
            '      "food_waste": "Level"\n'
            '    },\n'
            '    "transportation": {\n'
            '      "primary_mode": "Main transport",\n'
            '      "car_type": "Vehicle type",\n'
            '      "commute_details": "Distance/frequency"\n'
            '    },\n'
            '    "energy_usage": {\n'
            '      "heating_source": "Heating type",\n'
            '      "ac_usage": "AC frequency",\n'
            '      "energy_conservation_habits": "Conservation level"\n'
            '    }\n'
            '  },\n'
            '  "consumption_patterns": {\n'
            '    "shopping_frequency": "Frequency",\n'
            '    "plastic_usage": "Usage level",\n'
            '    "recycling_habit": "Recycling level"\n'
            '  },\n'
            '  "psychographic_insights": {\n'
            '    "motivations": ["Primary motivations"],\n'
            '    "barriers": ["Main challenges"],\n'
            '    "goals": ["Improvement areas"]\n'
            '  },\n'
            '  "key_levers": [\n'
            '    "Specific actionable lever 1",\n'
            '    "Specific actionable lever 2",\n'
            '    "Specific actionable lever 3",\n'
            '    "Specific actionable lever 4"\n'
            '  ],\n'
            '  "narrative_text": "70-90 word narrative summarizing user\'s lifestyle, location, habits, motivations, and personal context from additional_info."\n'
            "}\n"
            "CRITICAL: Return ONLY the JSON object. No text before or after. Start with { and end with }."
        ),
        agent=agent,
        async_execution=False,
        output_json=ProfilerAgentOutput,
    )

# # =========================================================
# #             Agent 2 - Analyst Agent Task
# # =========================================================
# # Task 1
# # -----------------------------
def create_analyst_task(agent, enriched_profile_data):
    """Creates the comprehensive carbon analysis task for Analyst Agent using enriched profile"""
    
    return Task(
        description=(
            "Analyze the enriched user profile to calculate carbon footprint, validate key levers, "
            "and generate personalized insights. Be concise and focus on the most impactful findings.\n\n"
            
            "ENRICHED PROFILE:\n"
            f"{enriched_profile_data}\n\n"
            
            "ANALYSIS TASKS:\n"
            "1. Calculate annual carbon footprint by category using emission factors\n"
            "2. Validate top 3 key levers from profile with potential reduction in kg CO2\n"
            "3. Create 2-3 personalized insights connecting emissions to user's motivations/barriers\n"
            "4. Generate sustainability score (0-10) and regional comparison\n\n"
            
            "EMISSION FACTORS:\n"
            "Transport: Gas car 0.4kg/mile, Hybrid 0.2kg/mile, Electric 0.15kg/mile\n"
            "Diet: Beef 27kg/kg, Chicken 7kg/kg, Vegetables 2kg/kg\n"
            "Energy: Natural gas 5.3kg/therm, Electricity 0.7kg/kWh\n"
            "Digital: AI query 4g, Streaming 36g/hour\n\n"
            
            "IMPORTANT: For 'top_impact_categories', use user-friendly names:\n"
            "- 'Transportation' (not 'transportation_kg')\n"
            "- 'Diet' (not 'diet_kg')\n"
            "- 'Home Energy' (not 'home_energy_kg')\n"
            "- 'Shopping' (not 'shopping_kg')\n"
            "- 'Digital Footprint' (not 'digital_footprint_kg')\n"
            "- 'Other' (not 'other_kg')\n\n"
            
            "PSYCHOGRAPHIC INTEGRATION (keep insights precise):\n"
            "- Connect high emissions with user motivations (e.g., 'saving money' + energy use)\n"
            "- Address barriers with specific actions (e.g., 'not knowing what to do' + simple steps)\n"
            "- Link goals to emission reductions (e.g., 'reduce footprint' + quantified impact)\n\n"
            
            "FOCUS ON BREVITY: Keep insights actionable but concise."
        ),
        expected_output=(
            "Concise JSON object with carbon analysis:\n"
            "{\n"
            '  "total_carbon_footprint_kg": number,\n'
            '  "total_carbon_footprint_tonnes": number,\n'
            '  "category_breakdown": {\n'
            '    "transportation_kg": number,\n'
            '    "diet_kg": number,\n'
            '    "home_energy_kg": number,\n'
            '    "shopping_kg": number,\n'
            '    "digital_footprint_kg": number,\n'
            '    "other_kg": number\n'
            '  },\n'
            '  "top_impact_categories": ["Transportation", "Home Energy", "Diet"],\n'
            '  "sustainability_score": number,\n'
            '  "score_category": "category",\n'
            '  "regional_comparison": {\n'
            '    "user_location": "location",\n'
            '    "local_average_kg": number,\n'
            '    "comparison_status": "above/below/equal",\n'
            '    "percentage_difference": number\n'
            '  },\n'
            '  "key_lever_validations": [\n'
            '    {\n'
            '      "lever": "lever text",\n'
            '      "validated": boolean,\n'
            '      "impact_category": "category",\n'
            '      "potential_reduction_kg": number,\n'
            '      "validation_reason": "brief reason"\n'
            '    }\n'
            '  ],\n'
            '  "psychographic_insights": [\n'
            '    {\n'
            '      "insight_text": "Precise insight connecting emissions to user psychology",\n'
            '      "related_motivation": "specific motivation from profile",\n'
            '      "addresses_barrier": "specific barrier from profile",\n'
            '      "actionable_next_step": "concrete, measurable action"\n'
            '    }\n'
            '  ],\n'
            '  "fun_comparison_facts": ["fact1", "fact2"],\n'
            '  "priority_reduction_areas": ["area1", "area2"],\n'
            '  "calculation_method": "brief method",\n'
            '  "data_confidence": "high/medium/low"\n'
            "}\n"
            "CRITICAL: Return ONLY valid JSON. Keep psychographic insights precise and actionable."
        ),
        agent=agent,
        async_execution=False,
        output_json=AnalystAgentOutput,
    )
    
# # Task 2
# # -----------------------------
def create_benchmarking_task(agent, user_data, carbon_results):
    """Creates the benchmarking, scoring, and insights task for Analyst Agent"""
    
    return Task(
        description=(
            "Generate sustainability scores, fun comparison facts, and actionable insights based on carbon footprint analysis. "
            "IMPORTANT: You must respond with ONLY a valid JSON object. No text before or after.\n\n"
            
            "USER PROFILE DATA:\n"
            f"{user_data}\n\n"
            
            "CARBON CALCULATION RESULTS:\n"
            f"{carbon_results}\n\n"
            
            "TASK 3 - GENERATE FUN FACTS: Create 2-3 engaging comparison facts using these benchmarks:\n"
            "Regional Averages (kg CO2/year/person):\n"
            "- US: 14,000 | Europe: 10,700 | India: 2,000 | Asia: 4,700 | China: 8,900\n"
            "- Africa: 1,000 | Global Average: 7,000 | Sustainable Target: 2,000\n"
            "Use your knowledge for other countries/regions not listed.\n\n"
            
            "TASK 4 - CREATE SUSTAINABILITY SCORE: Develop 0-10 scale where:\n"
            "- 0-3: High Impact (>12,000 kg CO2/year)\n"
            "- 4-6: Above Average (6,000-12,000 kg CO2/year)\n"
            "- 7-8: Below Average (3,000-6,000 kg CO2/year)\n"
            "- 9-10: Highly Sustainable (<3,000 kg CO2/year)\n\n"
            
            "TASK 5 - DELIVER INSIGHTS: Package findings into clear, actionable insights.\n"
            "Focus on priority reduction areas and personalized recommendations.\n\n"
            
            "YOUR RESPONSE: Pure JSON starting with { and ending with }"
        ),
        expected_output=(
            "A valid JSON object with exactly these fields:\n"
            "{\n"
            '  "sustainability_score": number (0-10 scale),\n'
            '  "score_category": "string (Highly Sustainable/Below Average/Above Average/High Impact)",\n'
            '  "fun_comparison_facts": [\n'
            '    "fact 1 comparing to regional/national average",\n'
            '    "fact 2 with relatable comparison (cars, trees, etc)",\n'
            '    "fact 3 with location-specific insight"\n'
            '  ],\n'
            '  "regional_comparison": {\n'
            '    "user_location": "from user data",\n'
            '    "local_average_kg": number,\n'
            '    "comparison_status": "above/below/equal to average"\n'
            '  },\n'
            '  "priority_reduction_areas": ["top 2-3 categories for improvement"],\n'
            '  "reduction_potential_kg": number,\n'
            '  "key_insights": [\n'
            '    "personalized insight 1",\n'
            '    "personalized insight 2",\n'
            '    "actionable recommendation"\n'
            '  ]\n'
            "}\n"
            "CRITICAL: Return ONLY valid JSON. No text before or after."
        ),
        agent=agent,
        async_execution=False,
        output_json=AnalystAgentOutput,
    )


# # =========================================================
# #             Agent 3 - Planner Agents Tasks
# # =========================================================

from .utils import load_challenges_metadata

# # Task 1
# # -----------------------------
def create_weekly_planning_task(agent, user_complete_data):
    """
    Creates the weekly action planning task for Planner Agent
    
    Args:
        agent: The planner agent
        user_complete_data: Complete user data including profile and carbon analysis
    """
    
    # Load available challenges from metadata
    challenges_data = load_challenges_metadata()
    
    return Task(
        description=(
            "Create EXACTLY 4 personalized sustainability challenges for this user.\n\n"
            
            f"USER DATA:\n{str(user_complete_data)[:400]}\n\n"
            
            "CHALLENGE EXAMPLES:\n"
            f"Easy: {[c['description'][:40] + '...' for c in challenges_data['easy'][:2]]}\n"
            f"Medium: {[c['description'][:40] + '...' for c in challenges_data['medium'][:1]]}\n"
            f"Hard: {[c['description'][:40] + '...' for c in challenges_data['hard'][:1]]}\n\n"
            
            "CRITICAL REQUIREMENTS:\n"
            "• Generate EXACTLY 4 challenges - NO MORE, NO LESS\n"
            "• Structure: 2 Easy + 1 Medium + 1 Hard\n"
            "• Select/adapt from examples OR create new ones\n"
            "• Keep descriptions under 50 words each\n"
            "• Focus on user's highest impact areas\n"
            "• COMPLETE ALL 4 CHALLENGES - DO NOT STOP EARLY\n"
        ),

        expected_output=(
            "WEEK FOCUS: [Brief theme]\n"
            "PRIORITY AREA: [Top impact area]\n\n"
            
            "CHALLENGES:\n"
            "1. EASY - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [diet/transport/energy/waste/consumption]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "2. EASY - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "3. MEDIUM - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "4. HARD - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "TOTAL SAVINGS: [X.X kg CO2]\n"
            "MOTIVATION MESSAGE: [Encouraging message]\n\n"
            "IMPORTANT: Complete ALL 4 challenges before finishing."
        ),
        agent=agent,
        async_execution=False,
    )


# # Task 2
# # -----------------------------
def create_feedback_aware_planning_task(agent, user_complete_data, feedback_history=None):
    """Creates the feedback-aware weekly planning task for Planner Agent"""
    
    # Load available challenges from metadata
    challenges_data = load_challenges_metadata()
    
    # Prepare feedback context
    feedback_context = ""
    if feedback_history and len(feedback_history) > 0:
        latest_feedback = feedback_history[0]['summary']
        feedback_context = f"\n\nUSER FEEDBACK:\n{latest_feedback[:200]}\n"
    
    return Task(
        description=(
            "Create EXACTLY 4 personalized challenges based on user feedback.\n\n"
            
            f"USER DATA:\n{str(user_complete_data)[:400]}\n\n"
            f"{feedback_context}"
            
            "EXAMPLES:\n"
            f"Easy: {[c['description'][:40] + '...' for c in challenges_data['easy'][:2]]}\n"
            f"Medium: {[c['description'][:40] + '...' for c in challenges_data['medium'][:1]]}\n"
            f"Hard: {[c['description'][:40] + '...' for c in challenges_data['hard'][:1]]}\n\n"
            
            "CRITICAL REQUIREMENTS:\n"
            "• Generate EXACTLY 4 challenges - NO MORE, NO LESS\n"
            "• Structure: 2 Easy + 1 Medium + 1 Hard\n"
            "• Adapt based on user feedback\n"
            "• Keep descriptions under 50 words each\n"
            "• COMPLETE ALL 4 CHALLENGES - DO NOT STOP EARLY\n"
        ),
        expected_output=(
            "WEEK FOCUS: [Theme adapted to feedback]\n"
            "PRIORITY AREA: [Area from feedback and analysis]\n\n"
            
            "CHALLENGES:\n"
            "1. EASY - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [diet/transport/energy/waste/consumption]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "2. EASY - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "3. MEDIUM - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "4. HARD - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "TOTAL SAVINGS: [X.X kg CO2]\n"
            "MOTIVATION MESSAGE: [Encouraging message]\n\n"
            "IMPORTANT: Complete ALL 4 challenges before finishing."
        ),
        agent=agent,
        async_execution=False,
    )

# # Task 3 - REMOVED: Daily task generation no longer needed
# # (Using only weekly planning with easy/medium/hard challenges)

# # Task 4
# # -----------------------------
def create_update_planning_task(agent, user_complete_data, user_update_text):
    """Creates an adaptive planning task based on user's latest update from dashboard"""
    
    # Load available challenges from metadata
    challenges_data = load_challenges_metadata()
    
    return Task(
        description=(
            "Create EXACTLY 4 new challenges based on user feedback.\n\n"
            
            f"USER UPDATE:\n{user_update_text[:200]}\n\n"
            
            f"USER DATA:\n{str(user_complete_data)[:400]}\n\n"
            
            "EXAMPLES:\n"
            f"Easy: {[c['description'][:35] + '...' for c in challenges_data['easy'][:2]]}\n"
            f"Medium: {[c['description'][:35] + '...' for c in challenges_data['medium'][:1]]}\n"
            f"Hard: {[c['description'][:35] + '...' for c in challenges_data['hard'][:1]]}\n\n"
            
            "CRITICAL REQUIREMENTS:\n"
            "• Generate EXACTLY 4 challenges - NO MORE, NO LESS\n"
            "• Structure: 2 Easy + 1 Medium + 1 Hard\n"
            "• Adapt based on their feedback\n"
            "• Keep descriptions under 50 words each\n"
            "• COMPLETE ALL 4 CHALLENGES - DO NOT STOP EARLY\n"
        ),
        expected_output=(
            "UPDATE ANALYSIS: [Summary of user feedback]\n"
            "WEEK FOCUS: [Adapted theme based on feedback]\n"
            "PRIORITY AREA: [Top area based on update]\n\n"
            
            "CHALLENGES:\n"
            "1. EASY - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [diet/transport/energy/waste/consumption]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "2. EASY - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "3. MEDIUM - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "4. HARD - [Title]\n"
            "   Description: [Action in 1 sentence]\n"
            "   Category: [category]\n"
            "   CO2 Savings: [X.X kg]\n"
            "   Time: [X minutes/hours]\n"
            "   Motivation: [Brief benefit]\n\n"
            
            "TOTAL SAVINGS: [X.X kg CO2]\n"
            "MOTIVATION MESSAGE: [Encouraging message]\n"
            "PLANNING NOTES: [Insights for future]\n\n"
            "IMPORTANT: Complete ALL 4 challenges before finishing."
        ),
        agent=agent,
        async_execution=False,
    )