# agent/test_analysis.py
import os
import sys
import json

# Add project root to the Python path to allow imports from other folders
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent.crew import run_analyst_workflow, create_analyst_crew
from agent.agents import create_analyst_agent, create_planner_agent
from agent.tasks import create_calculation_task
from data_model.database import get_user_profile_data

# Use a real user ID from your Supabase table that has onboarding data
TEST_USER_ID = "a7fc7052-b582-440e-b8d6-ca07493f987d" 

MOCK_ONBOARDING_DATA = {}

def get_user_data():
    """Get user onboarding data for testing."""
    try:
        # Attempt to load environment variables for Supabase
        import dotenv
        dotenv.load_dotenv()
        
        # Fetch real data if available
        data = get_user_profile_data(TEST_USER_ID)
        if data and 'onboarding_data' in data and data['onboarding_data']:
            print(f"✅ Successfully fetched real data for user {TEST_USER_ID}.")
            return data['onboarding_data']
        else:
            # Fallback to mock data if no real data is found
            print(f"⚠️  Could not fetch real data for user {TEST_USER_ID}, using mock data.")
            return MOCK_ONBOARDING_DATA
    except Exception as e:
        # Handle cases where Supabase connection fails
        print(f"❌ Supabase connection failed: {e}. Using mock data.")
        return MOCK_ONBOARDING_DATA

def run_analyst_test():
    """Run the analyst agent test."""
    print("🌱 EcoAction AI - Analyst Agent Test")
    print("=" * 50)
    
    # Debug environment variables
    print("\n🔧 Environment Debug:")
    print(f"- OPENAI_API_BASE: {os.environ.get('OPENAI_API_BASE', 'Not set')}")
    print(f"- OPENAI_API_KEY: {'Set' if os.environ.get('OPENAI_API_KEY') else 'Not set'}")
    print(f"- AI_ML_API_KEY: {'Set' if os.getenv('AI_ML_API_KEY') else 'Not set'}")
    
    # Get user data
    user_data = get_user_data()
    
    print("\n📋 User Data Summary:")
    print(f"- Location: {user_data.get('location_climate', {}).get('city', 'Unknown')}")
    print(f"- Household size: {user_data.get('household', {}).get('household_size', 'Unknown')}")
    print(f"- Primary transport: {user_data.get('transport', {}).get('primary_transport', 'Unknown')}")
    print(f"- Diet type: {user_data.get('diet_habits', {}).get('diet_type', 'Unknown')}")
    
    print("\n🚀 Running Analyst Agent...")
    print("-" * 30)
    
    try:
        # Test LiteLLM configuration first
        print("\n🧪 Testing LiteLLM Configuration...")
        import litellm
        
        # Test a simple completion call
        try:
            test_response = litellm.completion(
                model="openai/gpt-4.1-nano-2025-04-14",
                messages=[{"role": "user", "content": "Say 'Hello World' in JSON format"}],
                max_tokens=50
            )
            print(f"✅ LiteLLM test successful: {test_response.choices[0].message.content}")
        except Exception as e:
            print(f"❌ LiteLLM test failed: {e}")
            print("This explains why the agent is getting empty responses.")
            return
        
        # Use the complete analyst crew workflow
        print("🔄 Executing complete analyst workflow (Analyst + Planner agents)...")
        crew = create_analyst_crew(user_data)
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("📊 COMPLETE WORKFLOW RESULTS (3 AGENTS)")
        print("=" * 60)
        
        # Extract and display clean JSON
        if result:
            # Convert result to string if it's not already
            result_str = str(result).strip()
            
            # Try to extract JSON from the result
            json_start = result_str.find('{')
            json_end = result_str.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = result_str[json_start:json_end]
                try:
                    # Parse and reformat the JSON
                    parsed_json = json.loads(json_str)
                    print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing error: {e}")
                    print("Raw JSON string:")
                    print(json_str)
            else:
                # If no JSON found, try to parse the entire result
                try:
                    if isinstance(result, str):
                        parsed_result = json.loads(result)
                        print(json.dumps(parsed_result, indent=2, ensure_ascii=False))
                    else:
                        print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
                except json.JSONDecodeError:
                    print("⚠️ Result is not valid JSON. Raw output:")
                    print(result)
        else:
            print("❌ No result returned from agent")
            
        print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Error running analyst agent: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_analyst_test()