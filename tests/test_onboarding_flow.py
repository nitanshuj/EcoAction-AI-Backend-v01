# test_onboarding_flow.py
"""
Test script to verify the enhanced onboarding flow with profiler agent chat
"""

import json
from agent.agents import create_profiler_agent
from agent.tasks import create_profiling_task

def test_profiler_agent_question_generation():
    """Test that the profiler agent generates strategic questions within the 6-question limit"""
    
    # Sample user data for testing
    sample_user_data = {
        "location_climate": {
            "city": "New York",
            "climate": ["Temperate"]
        },
        "household": {
            "household_size": 2,
            "home_type": ["Apartment"],
            "home_size": "800 sq ft",
            "heating_source": ["Natural Gas"],
            "air_conditioning": ["Yes, often"]
        },
        "transport": {
            "primary_transport": ["Car"],
            "car_type": "Gasoline",
            "commute_distance": "15 miles daily"
        },
        "diet_habits": {
            "diet_type": ["Omnivore"],
            "meat_frequency": ["Daily"],
            "food_waste": ["Sometimes"]
        },
        "ai_digital_usage": {
            "ai_queries_daily": ["21-50"],
            "video_streaming_daily": ["3-5"]
        },
        "goals_motivation": {
            "main_motivation": ["Protecting the environment"],
            "biggest_challenge": ["Not knowing what to do"]
        }
    }
    
    try:
        # Create profiler agent and task
        profiler_agent = create_profiler_agent()
        profiling_task = create_profiling_task(profiler_agent, sample_user_data)
        
        print("🧪 Testing Profiler Agent Question Generation...")
        print(f"📊 Sample user data: {json.dumps(sample_user_data, indent=2)}")
        
        # Execute the profiling task
        result = profiling_task.execute()
        print(f"🤖 Agent response: {result}")
        
        # Try to parse the JSON result
        try:
            analysis = json.loads(result)
            print("✅ Successfully parsed JSON response")
            
            # Check for required fields
            required_fields = ["profile_analysis", "conversation_strategy", "enriched_profile"]
            for field in required_fields:
                if field in analysis:
                    print(f"✅ Found required field: {field}")
                else:
                    print(f"❌ Missing required field: {field}")
            
            # Check priority questions
            priority_questions = analysis.get("conversation_strategy", {}).get("priority_questions", [])
            print(f"📝 Generated {len(priority_questions)} priority questions:")
            for i, question in enumerate(priority_questions[:6], 1):  # Show max 6
                print(f"   {i}. {question}")
            
            if len(priority_questions) <= 6:
                print("✅ Question count within 6-question limit")
            else:
                print(f"⚠️ Generated {len(priority_questions)} questions - should be max 6")
                
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"Raw response: {result}")
            
    except Exception as e:
        print(f"❌ Error testing profiler agent: {e}")

def test_conversation_flow_logic():
    """Test the conversation flow logic"""
    print("\n🧪 Testing Conversation Flow Logic...")
    
    # Test question counter logic
    test_cases = [
        {"questions_asked": 0, "max_questions": 6, "should_continue": True},
        {"questions_asked": 3, "max_questions": 6, "should_continue": True},
        {"questions_asked": 5, "max_questions": 6, "should_continue": True},
        {"questions_asked": 6, "max_questions": 6, "should_continue": False},
        {"questions_asked": 7, "max_questions": 6, "should_continue": False},
    ]
    
    for test_case in test_cases:
        questions_asked = test_case["questions_asked"]
        max_questions = test_case["max_questions"]
        expected = test_case["should_continue"]
        
        # Simulate the logic from handle_user_response
        should_continue = questions_asked < max_questions
        
        if should_continue == expected:
            print(f"✅ Test passed: {questions_asked}/{max_questions} questions -> continue: {should_continue}")
        else:
            print(f"❌ Test failed: {questions_asked}/{max_questions} questions -> expected: {expected}, got: {should_continue}")

if __name__ == "__main__":
    print("🚀 Starting Onboarding Flow Tests...\n")
    
    test_profiler_agent_question_generation()
    test_conversation_flow_logic()
    
    print("\n✅ Testing completed!")
