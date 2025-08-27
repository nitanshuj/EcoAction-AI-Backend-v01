#!/usr/bin/env python3
"""
Test script for Agent 3 JSON validation fixes
Tests the new Pydantic validation logic for Agent 3 outputs
"""

import json
from agent.models import (
    validate_planner_output,
    validate_feedback_aware_output,
    validate_daily_tasks_output,
    validate_update_planner_output,
    Challenge,
    PlannerAgentOutput,
    FeedbackAwarePlannerOutput,
    DailyTasksOutput,
    UpdatePlannerOutput
)

def test_challenge_validation():
    """Test individual challenge validation"""
    print("🧪 Testing Challenge validation...")
    
    # Valid challenge
    valid_challenge = {
        "id": "challenge_1",
        "title": "Reduce Meat Consumption",
        "description": "Replace one meat meal per day with a plant-based alternative",
        "difficulty": "easy",
        "category": "diet",
        "steps": ["Choose plant-based protein", "Plan meals ahead", "Track progress"],
        "co2_savings_kg": 3.5,
        "time_required": "10 minutes daily",
        "deadline": "Daily this week",
        "success_metrics": "Count plant-based meals",
        "motivation": "Help save animals and the planet"
    }
    
    try:
        challenge = Challenge.model_validate(valid_challenge)
        print("✅ Valid challenge validation passed")
    except Exception as e:
        print(f"❌ Valid challenge validation failed: {e}")
        return False
    
    # Invalid challenge (missing required field)
    invalid_challenge = {
        "id": "challenge_1",
        "title": "Reduce Meat Consumption",
        # Missing description and other required fields
        "difficulty": "easy"
    }
    
    try:
        Challenge.model_validate(invalid_challenge)
        print("❌ Invalid challenge validation should have failed")
        return False
    except Exception:
        print("✅ Invalid challenge validation correctly failed")
    
    return True

def test_planner_output_validation():
    """Test PlannerAgentOutput validation"""
    print("\n🧪 Testing PlannerAgentOutput validation...")
    
    # Valid planner output with exactly 6 challenges (3 easy, 2 medium, 1 hard)
    valid_output = {
        "week_focus": "Energy Efficiency Focus Week",
        "priority_area": "Home Energy",
        "challenges": [
            # 3 Easy challenges
            {
                "id": "challenge_1",
                "title": "Turn Off Lights",
                "description": "Turn off lights when leaving a room",
                "difficulty": "easy",
                "category": "energy",
                "steps": ["Check all rooms", "Switch off unused lights", "Make it a habit"],
                "co2_savings_kg": 1.2,
                "time_required": "2 minutes daily",
                "deadline": "Daily this week",
                "success_metrics": "Lights turned off count",
                "motivation": "Save money on electricity bills"
            },
            {
                "id": "challenge_2",
                "title": "Unplug Electronics",
                "description": "Unplug electronics when not in use",
                "difficulty": "easy",
                "category": "energy",
                "steps": ["Identify vampire devices", "Unplug after use", "Use power strips"],
                "co2_savings_kg": 2.1,
                "time_required": "5 minutes daily",
                "deadline": "Daily this week",
                "success_metrics": "Devices unplugged count",
                "motivation": "Reduce phantom energy consumption"
            },
            {
                "id": "challenge_3",
                "title": "Adjust Thermostat",
                "description": "Lower thermostat by 2 degrees",
                "difficulty": "easy",
                "category": "energy",
                "steps": ["Find optimal temperature", "Adjust settings", "Monitor comfort"],
                "co2_savings_kg": 4.5,
                "time_required": "1 minute daily",
                "deadline": "Daily this week",
                "success_metrics": "Temperature setting maintained",
                "motivation": "Significant energy savings"
            },
            # 2 Medium challenges
            {
                "id": "challenge_4",
                "title": "Weatherstrip Windows",
                "description": "Install weatherstripping on drafty windows",
                "difficulty": "medium",
                "category": "energy",
                "steps": ["Identify drafts", "Buy weatherstrip", "Install carefully", "Test seal"],
                "co2_savings_kg": 15.8,
                "time_required": "2 hours total",
                "deadline": "By end of week",
                "success_metrics": "Windows sealed successfully",
                "motivation": "Long-term comfort and savings"
            },
            {
                "id": "challenge_5",
                "title": "Energy Audit",
                "description": "Conduct home energy audit",
                "difficulty": "medium",
                "category": "energy",
                "steps": ["Download audit checklist", "Inspect all areas", "Document findings", "Plan improvements"],
                "co2_savings_kg": 8.3,
                "time_required": "3 hours total",
                "deadline": "By end of week",
                "success_metrics": "Audit completed with action plan",
                "motivation": "Identify biggest energy wasters"
            },
            # 1 Hard challenge
            {
                "id": "challenge_6",
                "title": "Install Smart Thermostat",
                "description": "Replace old thermostat with smart programmable one",
                "difficulty": "hard",
                "category": "energy",
                "steps": ["Research models", "Purchase thermostat", "Install or hire electrician", "Program schedules"],
                "co2_savings_kg": 45.2,
                "time_required": "4-6 hours",
                "deadline": "Within 2 weeks",
                "success_metrics": "Smart thermostat installed and programmed",
                "motivation": "Automated energy optimization"
            }
        ],
        "total_potential_savings": 77.1,
        "motivation_message": "These energy-focused challenges can save you money while reducing your carbon footprint!"
    }
    
    try:
        result = validate_planner_output(valid_output)
        print("✅ Valid planner output validation passed")
        print(f"📊 Validated {len(result.challenges)} challenges")
    except Exception as e:
        print(f"❌ Valid planner output validation failed: {e}")
        return False
    
    # Test invalid output (wrong challenge count)
    invalid_output = valid_output.copy()
    invalid_output["challenges"] = valid_output["challenges"][:4]  # Only 4 challenges
    
    try:
        validate_planner_output(invalid_output)
        print("❌ Invalid planner output (wrong count) should have failed")
        return False
    except Exception:
        print("✅ Invalid planner output (wrong count) correctly failed")
    
    # Test invalid difficulty distribution
    invalid_difficulty = valid_output.copy()
    invalid_difficulty["challenges"] = valid_output["challenges"].copy()
    invalid_difficulty["challenges"][0]["difficulty"] = "hard"  # Now 2 hard, 2 easy, 2 medium
    
    try:
        validate_planner_output(invalid_difficulty)
        print("❌ Invalid difficulty distribution should have failed")
        return False
    except Exception:
        print("✅ Invalid difficulty distribution correctly failed")
    
    return True

def test_json_string_extraction():
    """Test JSON extraction from string format"""
    print("\n🧪 Testing JSON string extraction...")
    
    # Test with markdown code block
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
    
    try:
        result = validate_planner_output(json_with_markdown)
        print("✅ JSON extraction from markdown code block passed")
    except Exception as e:
        print(f"❌ JSON extraction from markdown failed: {e}")
        return False
    
    return True

def test_daily_tasks_validation():
    """Test DailyTasksOutput validation"""
    print("\n🧪 Testing DailyTasksOutput validation...")
    
    valid_daily_tasks = {
        "congratulations_message": "Great job completing your challenges!",
        "daily_focus": "Sustainable Habits",
        "new_daily_tasks": [
            {
                "id": "daily_1",
                "title": "Use Reusable Water Bottle",
                "action": "Carry and refill reusable water bottle",
                "why": "Reduces single-use plastic waste",
                "steps": ["Fill bottle", "Carry with you", "Refill as needed"],
                "co2_savings": 0.5,
                "difficulty": "easy",
                "task_type": "daily",
                "frequency": "daily"
            },
            {
                "id": "daily_2",
                "title": "Digital Receipt",
                "action": "Choose email receipts over paper",
                "why": "Saves paper and reduces waste",
                "steps": ["Ask for email receipt", "Decline paper", "Organize digitally"],
                "co2_savings": 0.2,
                "difficulty": "easy",
                "task_type": "daily",
                "frequency": "daily"
            },
            {
                "id": "daily_3",
                "title": "5-Minute Cleanup",
                "action": "Spend 5 minutes organizing belongings",
                "why": "Extends product lifespan through better care",
                "steps": ["Set 5-minute timer", "Organize one area", "Put items in proper place"],
                "co2_savings": 0.3,
                "difficulty": "easy",
                "task_type": "daily",
                "frequency": "daily"
            }
        ],
        "motivation": "Small daily actions create lasting environmental impact!"
    }
    
    try:
        result = validate_daily_tasks_output(valid_daily_tasks)
        print("✅ Valid daily tasks validation passed")
        print(f"📅 Validated {len(result.new_daily_tasks)} daily tasks")
    except Exception as e:
        print(f"❌ Valid daily tasks validation failed: {e}")
        return False
    
    # Test invalid task count
    invalid_tasks = valid_daily_tasks.copy()
    invalid_tasks["new_daily_tasks"] = valid_daily_tasks["new_daily_tasks"][:2]  # Only 2 tasks
    
    try:
        validate_daily_tasks_output(invalid_tasks)
        print("❌ Invalid daily tasks count should have failed")
        return False
    except Exception:
        print("✅ Invalid daily tasks count correctly failed")
    
    return True

def run_all_tests():
    """Run all validation tests"""
    print("🚀 Starting Agent 3 JSON Validation Tests\n")
    
    tests = [
        test_challenge_validation,
        test_planner_output_validation,
        test_json_string_extraction,
        test_daily_tasks_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        else:
            print("❌ Test failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Agent 3 JSON validation is working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
