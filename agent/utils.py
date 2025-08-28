# agent/utils.py
# --------------

import re, os, json, sys
from typing import Dict, Any



# --------------------------------------------
# This function(s) is only for the Agent 3 Output
# --------------------------------------------
def parse_text_to_json(text_string: str) -> dict:
    """
    Parses a structured text string about weekly challenges into a JSON dict.

    Args:
        text_string: The input string containing the weekly focus, priority area,
                     and a list of challenges with their details.

    Returns:
        A dictionary representing the structured data.
    """
    output = {}

    # Use regex to find the main "WEEK FOCUS" and "PRIORITY AREA".
    try:
        week_match = re.search(r'WEEK FOCUS:\s*(.*?)(?=\s*PRIORITY AREA:|$)', text_string, re.DOTALL)
        priority_match = re.search(r'PRIORITY AREA:\s*(.*?)(?=\s*Tasks:|$)', text_string, re.DOTALL)
        
        output['week_focus'] = week_match.group(1).strip() if week_match else "Sustainable Actions"
        output['priority_area'] = priority_match.group(1).strip() if priority_match else "Energy Efficiency"
    except AttributeError:
        output['week_focus'] = "Sustainable Actions"
        output['priority_area'] = "Energy Efficiency"

    # Enhanced challenge pattern to handle variations
    challenge_pattern = re.compile(
        r'(\d+)\.\s*(EASY|MEDIUM|HARD)\s*-\s*(.*?)\s*'  # 1. ID, Difficulty, Title
        r'Description:\s*(.*?)\s*'                      # 2. Description
        r'Category:\s*(.*?)\s*'                         # 3. Category
        r'CO2 Savings:\s*([\d\.]+)\s*kg.*?\s*'          # 4. CO2 Savings
        r'Time:\s*(.*?)\s*'                             # 5. Time
        r'Motivation:\s*(.*?)(?=\n\s*\d+\.|\n\s*TOTAL|\Z)',  # 6. Motivation
        re.DOTALL | re.IGNORECASE
    )

    challenges = []
    total_savings = 0.0

    # Iterate over all matches found in the text
    for match in challenge_pattern.finditer(text_string):
        challenge_id, difficulty, title, description, category, co2, time, motivation = match.groups()
        
        co2_val = float(co2) if co2 else 2.0
        total_savings += co2_val

        # Clean up category name
        category_clean = category.strip().lower()
        if category_clean in ['travel', 'transportation']:
            category_clean = 'transport'
        elif category_clean == 'food':
            category_clean = 'diet'

        challenges.append({
            'id': f'challenge_{challenge_id}',
            'title': title.strip(),
            'description': description.strip(),
            'difficulty': difficulty.strip().lower(),
            'category': category_clean,
            'co2_savings_kg': co2_val,
            'time_required': time.strip(),
            'motivation': motivation.strip()
        })

    output['challenges'] = challenges
    
    # Extract total savings from text or calculate
    total_match = re.search(r'TOTAL SAVINGS:\s*([\d\.]+)', text_string)
    if total_match:
        output['total_potential_savings'] = float(total_match.group(1))
    else:
        output['total_potential_savings'] = round(total_savings, 2)
    
    # Extract motivation message
    motivation_match = re.search(r'MOTIVATION MESSAGE:\s*(.*?)(?=\n\n|\Z)', text_string, re.DOTALL)
    if motivation_match:
        output['motivation_message'] = motivation_match.group(1).strip()
    else:
        output['motivation_message'] = "Every small action adds up to make a big difference for our planet!"

    return output


def parse_feedback_aware_text_to_json(text_string: str) -> dict:
    """
    Parses feedback-aware planning text output into JSON structure.
    """
    output = parse_text_to_json(text_string)  # Start with basic parsing
    
    # Add feedback-specific fields
    output['feedback_adaptation_notes'] = "Plan adapted based on user feedback and preferences"
    
    # Enhance challenge structure for feedback-aware format
    for i, challenge in enumerate(output['challenges']):
        challenge.update({
            'steps': [f"Step 1 for {challenge['title']}", f"Step 2 for {challenge['title']}", f"Step 3 for {challenge['title']}"],
            'deadline': 'Daily this week',
            'success_metrics': f"Complete {challenge['title'].lower()} as described",
            'completed': False
        })
    
    return output


def parse_update_planning_text_to_json(text_string: str, user_update_text: str = "") -> dict:
    """
    Parses update planning text output into JSON structure.
    """
    output = {}
    
    # Extract update analysis
    analysis_match = re.search(r'UPDATE ANALYSIS:\s*(.*?)(?=\s*WEEK FOCUS:|$)', text_string, re.DOTALL)
    output['update_analysis'] = analysis_match.group(1).strip() if analysis_match else f"User provided update: {user_update_text[:100]}..."
    
    # Use base parser for common fields
    base_output = parse_text_to_json(text_string)
    output.update(base_output)
    
    # Extract planning notes
    notes_match = re.search(r'PLANNING NOTES:\s*(.*?)(?=\n\n|\Z)', text_string, re.DOTALL)
    output['planning_adjustments'] = "Challenges adapted based on user's latest feedback and circumstances"
    output['future_planning_notes'] = notes_match.group(1).strip() if notes_match else "Remember user preferences for future planning sessions"
    
    # Enhance challenge structure for update format
    for challenge in output['challenges']:
        challenge.update({
            'steps': [f"Step 1 for {challenge['title']}", f"Step 2 for {challenge['title']}", f"Step 3 for {challenge['title']}"],
            'deadline': 'Daily this week',
            'success_metrics': f"Complete {challenge['title'].lower()} as described",
            'completed': False
        })
    
    return output


def parse_agent3_text_output(text_output: str, task_type: str = "basic", user_update_text: str = "") -> dict:
    """
    Universal parser for Agent 3 text outputs. Routes to appropriate parser based on task type.
    
    Args:
        text_output: Raw text output from Agent 3
        task_type: Type of task ("basic", "feedback_aware", "update_planning")
        user_update_text: User update text (for update_planning tasks)
    
    Returns:
        Parsed JSON dictionary
    """
    try:
        if task_type == "feedback_aware":
            return parse_feedback_aware_text_to_json(text_output)
        elif task_type == "update_planning":
            return parse_update_planning_text_to_json(text_output, user_update_text)
        else:
            return parse_text_to_json(text_output)
            
    except Exception as e:
        print(f"❌ Error parsing {task_type} output: {e}")
        # Return fallback structure for 4 challenges (2 easy + 1 medium + 1 hard)
        return {
            "week_focus": "Sustainable Actions",
            "priority_area": "Energy Efficiency",
            "challenges": [
                {
                    "id": f"challenge_{i+1}",
                    "title": f"Challenge {i+1}",
                    "description": "A sustainability action",
                    "difficulty": "easy" if i < 2 else ("medium" if i < 3 else "hard"),
                    "category": "energy",
                    "co2_savings_kg": 2.0,
                    "time_required": "15 minutes",
                    "motivation": "Help the environment"
                }
                for i in range(4)
            ],
            "total_potential_savings": 8.0,
            "motivation_message": "Keep up the great work!",
            "parsing_error": str(e),
            "raw_output": text_output
        }


def parse_update_planning_text_to_json(text_string: str, user_update_text: str = "") -> dict:
    """
    Parses update planning text output into JSON structure.
    """
    output = {}
    
    # Extract update analysis
    analysis_match = re.search(r'UPDATE ANALYSIS:\s*(.*?)(?=\s*WEEK FOCUS:|$)', text_string, re.DOTALL)
    output['update_analysis'] = analysis_match.group(1).strip() if analysis_match else f"User provided update: {user_update_text[:100]}..."
    
    # Use base parser for common fields
    base_output = parse_text_to_json(text_string)
    output.update(base_output)
    
    # Extract planning notes
    notes_match = re.search(r'PLANNING NOTES:\s*(.*?)(?=\n\n|\Z)', text_string, re.DOTALL)
    output['planning_adjustments'] = "Challenges adapted based on user's latest feedback and circumstances"
    output['future_planning_notes'] = notes_match.group(1).strip() if notes_match else "Remember user preferences for future planning sessions"
    
    # Enhance challenge structure for update format
    for challenge in output['challenges']:
        challenge.update({
            'steps': [f"Step 1 for {challenge['title']}", f"Step 2 for {challenge['title']}", f"Step 3 for {challenge['title']}"],
            'deadline': 'Daily this week',
            'success_metrics': f"Complete {challenge['title'].lower()} as described",
            'completed': False
        })
    
    return output


def parse_agent3_text_output(text_output: str, task_type: str = "basic", user_update_text: str = "") -> dict:
    """
    Universal parser for Agent 3 text outputs. Routes to appropriate parser based on task type.
    
    Args:
        text_output: Raw text output from Agent 3
        task_type: Type of task ("basic", "feedback_aware", "update_planning")
        user_update_text: User update text (for update_planning tasks)
    
    Returns:
        Parsed JSON dictionary
    """
    try:
        if task_type == "feedback_aware":
            return parse_feedback_aware_text_to_json(text_output)
        elif task_type == "update_planning":
            return parse_update_planning_text_to_json(text_output, user_update_text)
        else:  # basic weekly planning
            return parse_text_to_json(text_output)
    except Exception as e:
        print(f"❌ Error parsing {task_type} output: {e}")
        # Return fallback structure
        return {
            "week_focus": "Sustainable Actions",
            "priority_area": "Energy Efficiency",
            "challenges": [
                {
                    "id": f"challenge_{i+1}",
                    "title": f"Challenge {i+1}",
                    "description": "A sustainability action",
                    "difficulty": "easy" if i < 3 else ("medium" if i < 5 else "hard"),
                    "category": "energy",
                    "co2_savings_kg": 2.0,
                    "time_required": "15 minutes",
                    "motivation": "Help the environment"
                }
                for i in range(6)
            ],
            "total_potential_savings": 12.0,
            "motivation_message": "Keep up the great work!",
            "parsing_error": str(e),
            "raw_output": text_output
        }


# REMOVED: parse_daily_tasks_text_to_json function no longer needed
# (Using only weekly planning with easy/medium/hard challenges)


def load_challenges_metadata():
    """Load the challenges metadata from the data folder"""
    try:
        # Get the path to the challenges metadata file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        challenges_path = os.path.join(project_root, "data", "challenges_metadata.json")
        
        with open(challenges_path, 'r', encoding='utf-8') as f:
            challenges = json.load(f)
        
        # Group challenges by difficulty for easy reference
        easy_challenges = [c for c in challenges if c.get('difficulty') == 'Easy']
        medium_challenges = [c for c in challenges if c.get('difficulty') == 'Medium'] 
        hard_challenges = [c for c in challenges if c.get('difficulty') == 'Hard']
        
        return {
            'all_challenges': challenges,
            'easy': easy_challenges[:10],  # Limit to first 10 for prompt brevity
            'medium': medium_challenges[:10],
            'hard': hard_challenges[:5]
        }
    except Exception as e:
        print(f"Warning: Could not load challenges metadata: {e}")
        return {'all_challenges': [], 'easy': [], 'medium': [], 'hard': []}