# test_profiler_agent.py
"""Test script for Agent 1 (Profiler) functionality"""

import sys, os, json

# Add the project root to the path so imports like `agent.crew` work
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agent.crew import run_profiler_workflow
from agent.models import validate_profiler_output

def test_profiler_agent():
    """Test the profiler agent with sample data"""
    
    # Sample user data (similar to what comes from onboarding form)
    sample_user_data = {
        "user_id": "test-user-123",
        "location": {
            "city": "San Francisco",
            "country": "United States", 
            "climate": "Mediterranean"
        },
        "household": {
            "size": 2,
            "home_type": ["Apartment"],
            "home_size": "800 sq ft",
            "ownership": ["Rent"],
            "heating_source": ["Natural Gas"],
            "air_conditioning": "Sometimes",
            "appliances": ["Refrigerator", "Washing Machine", "Microwave"],
            "energy_conservation": "Often"
        },
        "transportation": {
            "primary_transport": ["Personal Car"],
            "car_type": ["Sedan"],
            "vehicle_fuel": ["Hybrid"],
            "commute_distance": "20 miles",
            "rideshare_usage": "Occasionally",
            "public_transport_usage": "Weekly"
        },
        "diet": {
            "diet_type": ["Omnivore"],
            "meat_frequency": "A few times a week",
            "food_waste": "Sometimes",
            "shopping_frequency": "Weekly"
        },
        "consumption": {
            "clothes_shopping": "Seasonally",
            "new_vs_secondhand": "A mix of both",
            "eco_importance": "Very important",
            "recycling_habits": "I recycle everything I can",
            "composting": "I'd like to start",
            "plastic_usage": "Sometimes"
        },
        "travel": {
            "flights_per_year": "1-2 short-haul",
            "flight_reason": ["Vacation"],
            "lifestyle": "Average consumer",
            "hobbies": ["Cooking", "Gaming"]
        },
        "digital": {
            "ai_queries_daily": "6-20",
            "image_generation_monthly": "1-10",
            "video_streaming_daily": "3-5",
            "cloud_storage_usage": "Moderate (50-500GB)",
            "device_usage": "Laptop",
            "online_meetings_weekly": "6-15"
        },
        "goals": {
            "main_motivation": ["Protecting the environment"],
            "biggest_challenge": ["Not knowing what to do"],
            "improvement_area": ["Reducing carbon footprint"],
            "other_improvement_area": ""
        },
        "additional_info": "I want to start composting and reduce my energy bills. I work from home most days."
    }
    
    try:        
        
        print("🧪 Testing Profiler Agent (Agent 1)...")
        print(f"📋 Input data: {json.dumps(sample_user_data, indent=2)}")
        
        # Run profiler workflow
        print("\n🚀 Running profiler workflow...")
        results = run_profiler_workflow(sample_user_data)
        
        if results:
            print("✅ Profiler workflow completed!")
            
            # Parse results from CrewAI output
            try:
                # CrewAI returns structured output with .json property
                if hasattr(results, 'json') and results.json:
                    # If results.json is a string, parse it
                    if isinstance(results.json, str):
                        parsed_results = json.loads(results.json)
                    else:
                        parsed_results = results.json
                elif hasattr(results, 'raw') and results.raw:
                    # Fallback to raw output if json not available
                    parsed_results = json.loads(results.raw)
                else:
                    # Last resort - try to parse the string representation
                    result_str = str(results)
                    parsed_results = json.loads(result_str)
                    
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"❌ Failed to parse results as JSON: {e}")
                print(f"Raw results: {results}")
                return False
            
            print(f"\n📊 Raw Results: {json.dumps(parsed_results, indent=2)}")
            
            # Validate with Pydantic
            try:
                validated_output = validate_profiler_output(parsed_results)
                print("\n✅ Pydantic validation successful!")
                print(f"📋 Validated output: {validated_output.model_dump()}")
                
                # Display key insights using new model structure
                print(f"\n🔍 Demographics: {validated_output.demographics.location}")
                print(f"🍽️ Diet Type: {validated_output.lifestyle_habits.diet.type}")
                print(f"� Transportation: {validated_output.lifestyle_habits.transportation.primary_mode}")
                print(f"💡 Key Levers: {len(validated_output.key_levers)}")
                print(f"📝 Narrative: {validated_output.narrative_text[:50]}...")
                
                # Display key levers
                print("\n🎯 Key Carbon Reduction Levers:")
                for i, lever in enumerate(validated_output.key_levers, 1):
                    print(f"  {i}. {lever}")
                
                return True
                
            except ValueError as e:
                print(f"❌ Pydantic validation failed: {str(e)}")
                return False
                
        else:
            print("❌ Profiler workflow returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Error testing profiler agent: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_profiler_agent()
    print(f"\n{'🎉 Test PASSED' if success else '💥 Test FAILED'}")
