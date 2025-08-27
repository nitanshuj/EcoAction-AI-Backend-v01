# tasks.py
from crewai import Task
from .models import (
    ProfilerAgentOutput, 
    AnalystAgentOutput, 
    PlannerAgentOutput, 
    FeedbackAwarePlannerOutput, 
    DailyTasksOutput, 
    UpdatePlannerOutput
)


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

# # Task 1
# # -----------------------------
def create_weekly_planning_task(agent, user_data, carbon_results, benchmark_results):
    """Creates the weekly action planning task for Planner Agent"""
    
    return Task(
        description=(
            "Create EXACTLY 6 personalized sustainability challenges based on user profile and carbon analysis.\n\n"
            
            "CRITICAL REQUIREMENTS:\n"
            "- MUST create exactly 6 challenges (never more, never less)\n"
            "- MUST include 3 easy + 2 medium + 1 hard challenge\n"
            "- NEVER delete incomplete challenges unless user specifically requests it\n"
            "- Each challenge must be unique and actionable\n\n"
            
            f"USER PROFILE:\n{str(user_data)}\n\n"
            f"CARBON ANALYSIS:\n{str(carbon_results)}\n\n"
            
            "CHALLENGE REQUIREMENTS:\n"
            "- Create exactly 6 challenges total (NEVER MORE, NEVER LESS)\n"
            "- 3 Easy challenges (simple daily habits, 5-10 minutes)\n"
            "- 2 Medium challenges (weekly commitments, 30-60 minutes)\n"
            "- 1 Hard challenge (significant change, 2+ hours or major lifestyle shift)\n"
            "- Each challenge should be specific, actionable, and measurable\n"
            "- Match challenges to user's lifestyle, barriers, and motivations\n"
            "- Include realistic CO2 savings estimates\n"
            "- Provide clear steps for completion\n"
            "- Set appropriate deadlines based on difficulty\n\n"
            
            "DIFFICULTY DEFINITIONS:\n"
            "- Easy: Quick daily actions (5-10 minutes), minimal effort, immediate\n"
            "- Medium: Weekly commitments requiring some planning (30-60 minutes)\n"
            "- Hard: Significant lifestyle changes or long-term projects (2+ hours or major change)\n\n"
            
            "Focus on the user's top carbon reduction opportunities from their analysis.\n"
            "RETURN ONLY JSON - no text before or after."
        ),
        expected_output=(
            "A complete JSON object with EXACTLY 6 challenges:\n"
            "{\n"
            '  "week_focus": "Primary sustainability theme for this week",\n'
            '  "priority_area": "Top carbon reduction area from analysis",\n'
            '  "challenges": [\n'
            '    {\n'
            '      "id": "challenge_1",\n'
            '      "title": "Challenge title (specific and actionable)",\n'
            '      "description": "Clear description of what to do",\n'
            '      "difficulty": "easy",\n'
            '      "category": "diet/transport/energy/waste/consumption",\n'
            '      "steps": ["Step 1", "Step 2", "Step 3"],\n'
            '      "co2_savings_kg": 2.5,\n'
            '      "time_required": "5-10 minutes daily",\n'
            '      "deadline": "Daily this week",\n'
            '      "success_metrics": "How to measure completion",\n'
            '      "motivation": "Why this matters for the user",\n'
            '      "completed": false\n'
            '    }\n'
            '  ],\n'
            '  "total_potential_savings": 15.2,\n'
            '  "motivation_message": "Encouraging message tailored to user\'s goals"\n'
            "}\n\n"
            "CRITICAL: Must include EXACTLY 6 challenges - 3 easy, 2 medium, 1 hard. Return only valid JSON."
        ),
        agent=agent,
        async_execution=False,
        output_json=PlannerAgentOutput,
    )


def create_feedback_aware_planning_task(agent, user_data, carbon_results, benchmark_results, feedback_history=None):
    """Creates the feedback-aware weekly planning task for Planner Agent (Two-Tiered Memory System)"""
    
    # Prepare feedback context
    feedback_context = ""
    if feedback_history and len(feedback_history) > 0:
        latest_feedback = feedback_history[0]['summary']
        feedback_context = f"\n\nUSER FEEDBACK HISTORY (Tier 2 Memory):\nLatest: {latest_feedback}\n"
        
        if len(feedback_history) > 1:
            feedback_context += f"Previous: {feedback_history[1]['summary']}\n"
    
    return Task(
        description=(
            "Create EXACTLY 6 personalized challenges using the Two-Tiered Memory System. "
            "Use user feedback to filter and adapt challenge selection.\n\n"
            
            "CRITICAL REQUIREMENTS:\n"
            "- MUST create exactly 6 challenges (never more, never less)\n"
            "- MUST include 3 easy + 2 medium + 1 hard challenge\n"
            "- NEVER delete incomplete challenges unless user specifically requests it\n"
            "- Each challenge must be unique and actionable\n\n"
            
            "RETURN ONLY JSON. No markdown, no extra text, no explanations.\n\n"
            
            f"USER PROFILE (Tier 1 - Stable Memory):\n{str(user_data)[:300]}...\n"
            f"CARBON ANALYSIS:\n{str(carbon_results)[:200]}...\n"
            f"BENCHMARK DATA:\n{str(benchmark_results)[:200]}...\n"
            f"{feedback_context}"
            
            "PERSONALIZATION INSTRUCTIONS:\n"
            "1. If feedback mentions difficulty preferences, adjust challenge difficulty accordingly\n"
            "2. If feedback mentions category preferences (transport, energy, diet), prioritize those areas\n"
            "3. If feedback mentions motivations (money, health, convenience), highlight those benefits\n"
            "4. If feedback mentions constraints (no car, apartment living), avoid impossible challenges\n"
            "5. If feedback requests more variety, diversify categories\n\n"
            
            "Create exactly 6 personalized challenges (NEVER MORE, NEVER LESS):\n"
            "- 3 easy challenges (simple daily habits, 5-10 minutes)\n"
            "- 2 medium challenges (weekly commitments, 30-60 minutes)\n" 
            "- 1 hard challenge (significant change, 2+ hours or major lifestyle shift)\n"
            "- Adapt difficulty distribution based on user feedback\n"
            "- Include clear steps for completion\n"
            "- Estimate realistic CO2 savings (1-25 kg)\n"
            "- Align with user motivations and remove barriers mentioned in feedback\n\n"
            
            "CRITICAL: Adapt challenge selection based on feedback while maintaining exactly 6 challenges."
        ),
        expected_output=(
            "Complete JSON with EXACTLY 6 feedback-adapted challenges:\n"
            "{\n"
            '  "week_focus": "Theme adapted to user feedback",\n'
            '  "priority_area": "Area from feedback and carbon analysis",\n'
            '  "challenges": [\n'
            '    {\n'
            '      "id": "challenge_1",\n'
            '      "title": "Feedback-adapted challenge title",\n'
            '      "description": "Clear description adapted to user preferences",\n'
            '      "difficulty": "easy",\n'
            '      "category": "diet/transport/energy/waste/consumption",\n'
            '      "steps": ["Step 1", "Step 2", "Step 3"],\n'
            '      "co2_savings_kg": 2.5,\n'
            '      "time_required": "5-10 minutes daily",\n'
            '      "deadline": "Daily this week",\n'
            '      "success_metrics": "How to measure completion",\n'
            '      "motivation": "Why this matters based on user feedback",\n'
            '      "completed": false\n'
            '    }\n'
            '  ],\n'
            '  "total_potential_savings": 15.2,\n'
            '  "motivation_message": "Encouraging message incorporating user feedback",\n'
            '  "feedback_adaptation_notes": "How the plan was adapted based on feedback"\n'
            "}\n\n"
            "CRITICAL: Must include EXACTLY 6 challenges (3 easy, 2 medium, 1 hard) adapted to user feedback."
        ),
        agent=agent,
        async_execution=False,
        output_json=FeedbackAwarePlannerOutput,
    )

# # Task 2
# # -----------------------------
def create_daily_tasks_generation_task(agent, user_data, carbon_results, benchmark_results, completed_tasks):
    """Creates task for generating new daily tasks when user completes 3 out of 5 tasks"""
    
    return Task(
        description=(
            "As a Personal Sustainability Planner, the user has completed 3 out of 5 tasks and earned new daily challenges! "
            "Generate 3 new DAILY tasks that they can do repeatedly to maintain momentum.\n\n"
            
            "CRITICAL: Return ONLY valid JSON. No markdown, no text, no explanations.\n\n"
            
            f"USER DATA:\n{user_data}\n\n"
            f"CARBON RESULTS:\n{carbon_results}\n\n"
            f"BENCHMARKS:\n{benchmark_results}\n\n"
            f"COMPLETED TASKS:\n{completed_tasks}\n\n"
            
            "Generate 3 NEW daily sustainability tasks:\n"
            "- All must be DAILY tasks (repeatable actions)\n"
            "- Different from previously completed tasks\n"
            "- Focus on building sustainable daily habits\n"
            "- Should be quick and easy to integrate into daily routine\n"
            "- Estimate small but consistent CO2 savings\n\n"
            
            "DAILY TASK EXAMPLES:\n"
            "- Use reusable water bottle today\n"
            "- Turn off lights when leaving room\n"
            "- Take stairs instead of elevator\n"
            "- Unplug electronics after use\n"
            "- Use cold water for washing\n\n"
            
            "Keep all text fields concise (max 80 characters each).\n"
            "Return pure JSON starting with { and ending with }."
        ),
        expected_output=(
            "Return ONLY a simple JSON object for daily tasks:\n"
            "{\n"
            '  "congratulations_message": "Celebration message for completing 3 tasks",\n'
            '  "daily_focus": "Theme for these daily habits",\n'
            '  "new_daily_tasks": [\n'
            '    {\n'
            '      "id": "daily_task_unique_id",\n'
            '      "title": "Short daily action title",\n'
            '      "action": "Simple daily action to take",\n'
            '      "why": "Why this daily habit matters",\n'
            '      "steps": ["Quick step 1", "Quick step 2"],\n'
            '      "co2_savings": 2,\n'
            '      "difficulty": "easy",\n'
            '      "task_type": "daily",\n'
            '      "frequency": "daily",\n'
            '      "completed": false\n'
            '    }\n'
            '  ],\n'
            '  "motivation": "Encouragement for daily habit building"\n'
            "}\n"
            "CRITICAL: Must include exactly 3 daily tasks. All text under 80 characters."
        ),
        agent=agent,
        async_execution=False,
        output_json=DailyTasksOutput,
    )

# # Task 3
# # -----------------------------
def create_update_planning_task(agent, user_data, carbon_results, benchmark_results, user_update_text):
    """Creates an adaptive planning task based on user's latest update from dashboard"""
    
    return Task(
        description=(
            "As a Personal Sustainability Planner, analyze user's latest update and adapt weekly plan accordingly. "
            "Use their feedback to improve future recommendations and adjust current challenges.\n"
            "IMPORTANT: You must respond with ONLY a valid JSON object. No text before or after.\n\n"
            
            "CRITICAL REQUIREMENTS:\n"
            "- MUST create exactly 6 challenges (never more, never less)\n"
            "- MUST include 3 easy + 2 medium + 1 hard challenge\n"
            "- NEVER delete incomplete challenges unless user specifically requests it\n"
            "- Each challenge must be unique and actionable\n\n"
            
            "USER'S LATEST UPDATE:\n"
            f'"{user_update_text}"\n\n'
            
            "EXISTING USER CONTEXT:\n"
            f"USER PROFILE:\n{user_data}\n\n"
            f"CARBON ANALYSIS:\n{carbon_results}\n\n"
            f"SUSTAINABILITY SCORES:\n{benchmark_results}\n\n"
            
            "ADAPTIVE PLANNING TASKS:\n"
            "1. ANALYZE UPDATE: Understand user's progress, challenges, or new circumstances\n"
            "2. ADJUST STRATEGY: Modify approach based on their feedback or new information\n"
            "3. GENERATE UPDATED PLAN: Create exactly 6 new challenges considering their update\n"
            "4. INCORPORATE LEARNINGS: Use their feedback to personalize future recommendations\n"
            "5. MAINTAIN MOMENTUM: Keep them motivated while addressing their concerns\n\n"
            
            "CHALLENGE REQUIREMENTS:\n"
            "- Create exactly 6 challenges total (NEVER MORE, NEVER LESS)\n"
            "- 3 Easy challenges (simple daily habits, 5-10 minutes)\n"
            "- 2 Medium challenges (weekly commitments, 30-60 minutes)\n"
            "- 1 Hard challenge (significant change, 2+ hours or major lifestyle shift)\n"
            "- Adapt based on user's update and feedback\n\n"
            
            "RESPONSE STRATEGY:\n"
            "- If they report completion: Celebrate success and escalate difficulty\n"
            "- If they report challenges: Simplify actions and address barriers\n"
            "- If they share new info: Incorporate into planning strategy\n"
            "- If they seem discouraged: Focus on easier wins and motivation\n"
            "- If they're motivated: Introduce more ambitious challenges\n\n"
            
            "YOUR RESPONSE: Pure JSON starting with { and ending with }"
        ),
        expected_output=(
            "A valid JSON object with exactly these fields:\n"
            "{\n"
            '  "update_analysis": "Summary of what user shared and implications",\n'
            '  "planning_adjustments": "How the plan was modified based on their update",\n'
            '  "week_focus": "Adapted theme for this week based on user feedback",\n'
            '  "challenges": [\n'
            '    {\n'
            '      "id": "challenge_1",\n'
            '      "title": "Catchy, actionable title",\n'
            '      "description": "Specific action adapted to user feedback",\n'
            '      "difficulty": "easy",\n'
            '      "category": "diet/transport/energy/waste/consumption",\n'
            '      "steps": ["Step 1", "Step 2", "Step 3"],\n'
            '      "co2_savings_kg": 2.5,\n'
            '      "time_required": "5-10 minutes daily",\n'
            '      "deadline": "Daily this week",\n'
            '      "success_metrics": "How to measure completion",\n'
            '      "motivation": "Why this matters considering their update",\n'
            '      "completed": false\n'
            '    }\n'
            '  ],\n'
            '  "total_potential_savings": 15.2,\n'
            '  "motivation_message": "Personalized encouragement addressing their update",\n'
            '  "future_planning_notes": "Insights to remember for next planning"\n'
            "}\n"
            "CRITICAL: Create exactly 6 challenges (3 easy, 2 medium, 1 hard). No text outside JSON."
        ),
        agent=agent,
        async_execution=False,
        output_json=UpdatePlannerOutput,
    )