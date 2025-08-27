#!/usr/bin/env python3
"""
Debug script for JSON extraction
"""

import json
import re
from agent.models import extract_json_from_text, validate_planner_output

def debug_json_extraction():
    """Debug the JSON extraction process"""
    
    json_with_markdown = '''
    Here's the result:
    ```json
    {
        "week_focus": "Transportation Week",
        "priority_area": "Transportation",
        "challenges": [
            {
                "id": "challenge_1",
                "title": "Walk More",
                "description": "Walk for short trips instead of driving",
                "difficulty": "easy",
                "category": "transport",
                "steps": ["Identify walkable trips", "Plan route", "Track walks"],
                "co2_savings_kg": 2.5,
                "time_required": "20 minutes daily",
                "deadline": "Daily this week",
                "success_metrics": "Number of walks taken",
                "motivation": "Get exercise and fresh air"
            },
            {
                "id": "challenge_2",
                "title": "Bike to Work",
                "description": "Use bicycle for commuting twice this week",
                "difficulty": "easy",
                "category": "transport",
                "steps": ["Check bike condition", "Plan safe route", "Pack work clothes"],
                "co2_savings_kg": 8.4,
                "time_required": "30 minutes daily",
                "deadline": "Twice this week",
                "success_metrics": "Bike commutes completed",
                "motivation": "Save gas money and get fit"
            },
            {
                "id": "challenge_3",
                "title": "Carpool Setup",
                "description": "Organize carpooling with colleagues",
                "difficulty": "easy",
                "category": "transport",
                "steps": ["Find carpool partners", "Create schedule", "Share contact info"],
                "co2_savings_kg": 12.1,
                "time_required": "15 minutes setup",
                "deadline": "By end of week",
                "success_metrics": "Carpool arrangement confirmed",
                "motivation": "Build workplace connections"
            },
            {
                "id": "challenge_4",
                "title": "Public Transit Pass",
                "description": "Purchase and use public transit pass",
                "difficulty": "medium",
                "category": "transport",
                "steps": ["Research transit options", "Buy monthly pass", "Plan routes", "Use 3 times"],
                "co2_savings_kg": 25.3,
                "time_required": "2 hours setup",
                "deadline": "Use 3 times this week",
                "success_metrics": "Transit trips completed",
                "motivation": "Explore city from new perspective"
            },
            {
                "id": "challenge_5",
                "title": "Car Maintenance",
                "description": "Complete car tune-up for efficiency",
                "difficulty": "medium",
                "category": "transport",
                "steps": ["Schedule appointment", "Get oil change", "Check tire pressure", "Replace air filter"],
                "co2_savings_kg": 18.7,
                "time_required": "3 hours total",
                "deadline": "By end of week",
                "success_metrics": "Maintenance completed",
                "motivation": "Better fuel efficiency and performance"
            },
            {
                "id": "challenge_6",
                "title": "Hybrid Car Research",
                "description": "Research hybrid or electric vehicle options",
                "difficulty": "hard",
                "category": "transport",
                "steps": ["Research models", "Calculate costs", "Test drive options", "Compare financing"],
                "co2_savings_kg": 150.0,
                "time_required": "8+ hours",
                "deadline": "Within month",
                "success_metrics": "Research completed with decision plan",
                "motivation": "Long-term environmental impact"
            }
        ],
        "total_potential_savings": 217.0,
        "motivation_message": "Transform your transportation habits this week!"
    }
    ```
    '''
    
    print("🔍 Debugging JSON extraction...")
    print(f"Input length: {len(json_with_markdown)}")
    
    # Try to extract JSON
    try:
        extracted = extract_json_from_text(json_with_markdown)
        print("✅ JSON extraction successful")
        print(f"📊 Extracted keys: {list(extracted.keys())}")
        
        # Try validation
        result = validate_planner_output(extracted)
        print("✅ Validation successful")
        print(f"📊 Challenges: {len(result.challenges)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
        # Try manual extraction for debugging
        print("\n🔍 Manual extraction attempts:")
        
        # Look for the JSON block manually
        pattern = r'```json\s*(\{.*?\})\s*```'
        matches = re.findall(pattern, json_with_markdown, re.DOTALL)
        print(f"Matches found: {len(matches)}")
        
        if matches:
            print("📄 First match preview:")
            print(matches[0][:200])
            print("...")
            
            # Try parsing the match directly
            try:
                parsed = json.loads(matches[0])
                print("✅ Direct parsing of match successful")
                print(f"📊 Keys: {list(parsed.keys())}")
            except Exception as parse_error:
                print(f"❌ Direct parsing failed: {parse_error}")

if __name__ == "__main__":
    debug_json_extraction()
