# tasks.py
from crewai import Task

def create_profiling_task(agent, user_data):
    """Creates the user profiling and data enrichment task for Profiler Agent"""
    
    return Task(
        description=(
            "Analyze user's onboarding JSON data deeply, identify personalized data gaps, and ask 3-5 contextual questions "
            "based on their specific lifestyle patterns and carbon footprint areas.\n\n"
            
            "USER ONBOARDING DATA:\n"
            f"{user_data}\n\n"
            
            "TASK STEPS:\n"
            "1. DEEP ANALYSIS: Study user's specific lifestyle choices, transportation habits, energy usage, and diet patterns\n"
            "2. PERSONALIZED GAP IDENTIFICATION: Find missing quantities that matter most for THIS user's carbon profile\n"
            "3. CONTEXTUAL QUESTION CRAFTING: Create 3-5 targeted questions based on user's specific responses\n"
            "4. GENERATE VARIED QUESTIONS: Ensure questions are different each time by prioritizing the most impactful areas\n\n"
            
            "QUESTION EXAMPLES (adapt these concepts to the user's specific situation):\n"
            "Transportation Examples:\n"
            "- 'What temperature do you set your thermostat to in winter?'\n"
            "- 'How many miles exactly do you drive per week for work?'\n"
            "- 'How often do you combine errands into one trip?'\n"
            "\n"
            "Energy Examples:\n"
            "- 'How many hours per day do you run your AC during summer?'\n"
            "- 'What percentage of your appliances do you unplug when not in use?'\n"
            "- 'How many LED vs traditional bulbs do you have?'\n"
            "\n"
            "Diet Examples:\n"
            "- 'How many meat-based meals do you eat per week?'\n"
            "- 'What percentage of your food comes from local sources?'\n"
            "- 'How much food waste do you generate weekly (in pounds)?'\n\n"
            
            "QUESTION REQUIREMENTS:\n"
            "- Must be directly relevant to user's specific lifestyle\n"
            "- Focus on quantifiable, measurable behaviors\n"
            "- Target high-impact carbon areas specific to this user\n"
            "- Generate different questions each time based on their unique profile\n"
        ),
        expected_output=(
            "A valid JSON object with exactly these fields:\n"
            "{\n"
            '  "user_lifestyle_analysis": "Brief analysis of user\'s main carbon impact areas",\n'
            '  "personalized_data_gaps": ["specific missing info relevant to this user\'s lifestyle"],\n'
            '  "specific_questions": [\n'
            '    "Contextual question 1 based on user data?",\n'
            '    "Contextual question 2 targeting their habits?",\n'
            '    "Contextual question 3 about measurable behavior?"\n'
            '  ],\n'
            '  "question_rationale": ["Why each question matters for this user\'s carbon footprint"],\n'
            '  "enriched_user_profile": {\n'
            '    "original_data": "copy of original user data",\n'
            '    "lifestyle_insights": "key patterns identified from their responses",\n'
            '    "carbon_priority_areas": ["top 3 areas for this user to focus on"],\n'
            '    "question_responses": {\n'
            '      "question_1_answer": "",\n'
            '      "question_2_answer": "",\n'
            '      "question_3_answer": ""\n'
            '    }\n'
            '  }\n'
            "}\n"
            "CRITICAL: No text outside the JSON object. Start with { and end with }."
        ),
        agent=agent,
        async_execution=False,
    )

def create_calculation_task(agent, user_data):
    """Creates the carbon calculation and impact categorization task for Analyst Agent"""
    
    return Task(
        description=(
            "As a Senior Sustainability Analyst, calculate precise annual carbon footprint and categorize impact areas. "
            "IMPORTANT: You must respond with ONLY a valid JSON object. No text before or after.\n\n"
            
            "USER PROFILE DATA:\n"
            f"{user_data}\n\n"
            
            "TASK 1 - CALCULATE FOOTPRINT: Precisely compute annual carbon footprint using standard emission factors:\n"
            "Categories to analyze:\n"
            "1. Transportation (vehicle type, mileage, flights)\n"
            "2. Diet (food types, consumption frequency)\n"
            "3. Home Energy (heating, cooling, electricity usage)\n"
            "4. Shopping & Consumer Goods (frequency, types)\n"
            "5. Digital Footprint (AI usage, streaming, cloud storage, devices)\n"
            "6. Other activities (hobbies, lifestyle choices)\n\n"

            "EMISSION FACTORS (use your knowledge for missing ones):\n"
            "- Gasoline car: 0.404 kg CO2/mile | Diesel: 0.453 kg CO2/mile | Electric: 0.200 kg CO2/mile\n"
            "- Beef: 27.0 kg CO2/kg | Chicken: 6.9 kg CO2/kg | Vegetables: 2.0 kg CO2/kg\n"
            "- Natural gas: 5.3 kg CO2/therm | Electricity: 0.7 kg CO2/kWh\n"
            "- AI query: 4.32g CO2 | Video streaming: 36g CO2/hour | Cloud storage: 0.5 kg CO2/GB/year\n\n"
            
            "TASK 2 - CATEGORIZE IMPACT: Identify top 2-3 highest impact categories only.\n"
            "Focus on categories contributing >15% of total footprint.\n\n"
            
            "YOUR RESPONSE: Pure JSON starting with { and ending with }"
        ),
        expected_output=(
            "A valid JSON object with exactly these fields:\n"
            "{\n"
            '  "total_carbon_footprint_kg": number,\n'
            '  "category_breakdown": {\n'
            '    "transportation_kg": number,\n'
            '    "diet_kg": number,\n'
            '    "home_energy_kg": number,\n'
            '    "shopping_kg": number,\n'
            '    "digital_footprint_kg": number,\n'
            '    "other_kg": number\n'
            '  },\n'
            '  "top_impact_categories": ["category1", "category2", "category3"],\n'
            '  "calculation_method": "brief description of emission factors used",\n'
            '  "data_confidence": "high/medium/low"\n'
            "}\n"
            "CRITICAL: No text outside the JSON object. Start with { and end with }."
        ),
        agent=agent,
        async_execution=False,
    )

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
            "CRITICAL: No text outside the JSON object. Start with { and end with }."
        ),
        agent=agent,
        async_execution=False,
    )

def create_weekly_planning_task(agent, user_data, carbon_results, benchmark_results):
    """Creates the weekly action planning task for Planner Agent"""
    
    return Task(
        description=(
            "Create a tiny weekly plan. CRITICAL: Maximum 1500 characters total output.\n\n"
            
            "RETURN ONLY JSON. No markdown, no extra text, no explanations.\n\n"
            
            f"USER: {str(user_data)[:200]}...\n"
            f"CARBON: {str(carbon_results)[:200]}...\n"
            f"BENCHMARK: {str(benchmark_results)[:200]}...\n\n"
            
            "Create exactly 3 mini challenges:\n"
            "- 2 daily tasks\n" 
            "- 1 weekly task\n"
            "- Maximum 30 characters per text field\n"
            "- Maximum 2 steps per challenge\n"
            "- Keep CO2 savings simple (1-20)\n\n"
            
            "STRICT: Complete JSON under 1500 chars total."
        ),
        expected_output=(
            "ONLY this tiny JSON (max 30 chars per string):\n"
            "{\n"
            '  "week_focus": "Short theme",\n'
            '  "priority_area": "Main area",\n'
            '  "challenges": [\n'
            '    {\n'
            '      "id": "d1",\n'
            '      "title": "Short title",\n'
            '      "action": "Brief action",\n'
            '      "why": "Quick reason",\n'
            '      "steps": ["Step1", "Step2"],\n'
            '      "co2_savings": 5,\n'
            '      "difficulty": "easy",\n'
            '      "task_type": "daily",\n'
            '      "deadline": "Week",\n'
            '      "completed": false\n'
            '    }\n'
            '  ],\n'
            '  "motivation_message": "Short message"\n'
            "}\n"
            "EXACTLY 3 challenges. All text under 30 chars. Complete JSON only."
        ),
        agent=agent,
        async_execution=False,
    )

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
            "Must include exactly 3 daily tasks. All text under 80 characters."
        ),
        agent=agent,
        async_execution=False,
    )

def create_update_planning_task(agent, user_data, carbon_results, benchmark_results, user_update_text):
    """Creates an adaptive planning task based on user's latest update from dashboard"""
    
    return Task(
        description=(
            "As a Personal Sustainability Planner, analyze user's latest update and adapt weekly plan accordingly. "
            "Use their feedback to improve future recommendations and adjust current challenges.\n"
            "IMPORTANT: You must respond with ONLY a valid JSON object. No text before or after.\n\n"
            
            "USER'S LATEST UPDATE:\n"
            f'"{user_update_text}"\n\n'
            
            "EXISTING USER CONTEXT:\n"
            f"USER PROFILE:\n{user_data}\n\n"
            f"CARBON ANALYSIS:\n{carbon_results}\n\n"
            f"SUSTAINABILITY SCORES:\n{benchmark_results}\n\n"
            
            "ADAPTIVE PLANNING TASKS:\n"
            "1. ANALYZE UPDATE: Understand user's progress, challenges, or new circumstances\n"
            "2. ADJUST STRATEGY: Modify approach based on their feedback or new information\n"
            "3. GENERATE UPDATED PLAN: Create 4-5 new weekly challenges considering their update\n"
            "4. INCORPORATE LEARNINGS: Use their feedback to personalize future recommendations\n"
            "5. MAINTAIN MOMENTUM: Keep them motivated while addressing their concerns\n\n"
            
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
            '  "updated_challenges": [\n'
            '    {\n'
            '      "challenge_id": "unique_id_for_tracking",\n'
            '      "title": "Catchy, actionable title",\n'
            '      "description": "Specific action adapted to user feedback",\n'
            '      "personalized_why": "Why this matters considering their update",\n'
            '      "implementation_steps": [\n'
            '        "Step 1: specific action",\n'
            '        "Step 2: specific action",\n'
            '        "Step 3: measurement/tracking"\n'
            '      ],\n'
            '      "difficulty_level": "easy/medium/hard",\n'
            '      "estimated_co2_savings_kg": number,\n'
            '      "cost_impact": "savings/cost in local currency",\n'
            '      "completion_deadline": "specific day this week",\n'
            '      "success_metric": "how to measure completion",\n'
            '      "adaptation_reason": "why this was chosen based on user update"\n'
            '    }\n'
            '  ],\n'
            '  "motivational_response": "Personalized encouragement addressing their update",\n'
            '  "future_planning_notes": "Insights to remember for next week planning"\n'
            "}\n"
            "CRITICAL: Create exactly 4-5 updated_challenges. No text outside JSON."
        ),
        agent=agent,
        async_execution=False,
    )