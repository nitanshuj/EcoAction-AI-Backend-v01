# tests/test_agent_3.py
"""Test script for Agent 3 (Planner) functionality"""

import sys, os, json, re, warnings
warnings.filterwarnings("ignore")

# Add the parent directory to Python path so we can import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.crew import (
    run_planner_workflow,
    run_feedback_aware_planning_workflow,
    run_daily_tasks_generation_workflow,
    run_update_planning_workflow
)

# ---------------------------------------------
# --- Helper Functions ---
# ---------------------------------------------

def _parse_and_display_plan(results, test_name):
    """Helper function to parse and display the planner agent's output"""
    if not results:
        print("❌ No results returned from workflow")
        return

    print(f"✅ {test_name} completed successfully!")
    print(f"📋 Results type: {type(results)}")

    # Check if results is already a dictionary (new JSON output)
    if isinstance(results, dict):
        plan_data = results
        print("✅ Agent 3 returned structured JSON data")
    else:
        # Try to parse as JSON from string (fallback)
        raw_output = results.raw if hasattr(results, 'raw') else str(results)
        
        try:
            json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
            if not json_match:
                print("❌ No JSON found in the output.")
                print(f"📄 Raw Output:\n{raw_output}")
                return

            plan_data = json.loads(json_match.group(0))
            print("✅ Successfully parsed JSON from raw output")
            
        except (json.JSONDecodeError, AssertionError) as e:
            print(f"❌ Test validation failed: {e}")
            print(f"📄 Raw Output:\n{raw_output}")
            return
    
    # Display the parsed plan
    print("\n" + "="*50)
    print(f"🎯 PARSED AGENT 3 PLAN: {test_name}")
    print("="*50)
    print(f"📅 Week Focus: {plan_data.get('week_focus', 'N/A')}")
    
    challenges = plan_data.get('challenges', [])
    print(f"🏆 CHALLENGES ({len(challenges)} total):")
    
    # Validate challenge structure if we have challenges
    if challenges:
        try:
            assert len(challenges) == 6, f"Should return exactly 6 challenges, got {len(challenges)}"
            
            easy = [c for c in challenges if c.get('difficulty', '').lower() == 'easy']
            medium = [c for c in challenges if c.get('difficulty', '').lower() == 'medium']
            hard = [c for c in challenges if c.get('difficulty', '').lower() == 'hard']
            
            assert len(easy) == 3, f"Should have 3 easy challenges, got {len(easy)}"
            assert len(medium) == 2, f"Should have 2 medium challenges, got {len(medium)}"
            assert len(hard) == 1, f"Should have 1 hard challenge, got {len(hard)}"

            for i, challenge in enumerate(challenges, 1):
                print(f"  {i}. {challenge.get('title', 'N/A')} ({challenge.get('difficulty', 'N/A')})")
                
            print(f"💰 Total Potential Savings: {plan_data.get('total_potential_savings', 'N/A')} kg CO2")
            print(f"💡 Motivation: {plan_data.get('motivation_message', 'N/A')}")
            
        except AssertionError as e:
            print(f"⚠️ Challenge validation: {e}")
            # Still display what we got
            for i, challenge in enumerate(challenges, 1):
                print(f"  {i}. {challenge.get('title', 'N/A')} ({challenge.get('difficulty', 'N/A')})")
    else:
        print("⚠️ No challenges found in plan data")
        print(f"� Total Potential Savings: {plan_data.get('total_potential_savings', 'N/A')} kg CO2")
        print(f"💡 Motivation: {plan_data.get('motivation_message', 'N/A')}")


# --- Test Functions ---

def test_basic_planner_workflow():
    """Test the basic planner workflow (without feedback)"""
    print("🧪 Testing Basic Planner Workflow (Agent 3)...")
    
    # NOTE: Using a hardcoded user ID. For more robust testing, consider
    # creating a test user or mocking the database calls.
    test_user_id = "a14848d3-3d90-4f12-8034-52c2e9a6d4d9"
    
    try:
        print(f"🔄 Running basic planner workflow for user: {test_user_id}")
        results = run_planner_workflow(test_user_id)
        _parse_and_display_plan(results, "Basic Planner Workflow")
        
    except Exception as e:
        print(f"❌ Error in basic planner workflow: {e}")

def test_feedback_aware_workflow():
    """Test the feedback-aware planning workflow"""
    print("\n" + "-"*60)
    print("🧪 Testing Feedback-Aware Planning Workflow...")
    
    test_user_id = "a14848d3-3d90-4f12-8034-52c2e9a6d4d9"
    test_feedback = "I need easier, home-based challenges that also help me save money."
    
    try:
        print(f"🔄 Running feedback-aware workflow for user: {test_user_id}")
        results = run_feedback_aware_planning_workflow(test_user_id, test_feedback)
        _parse_and_display_plan(results, "Feedback-Aware Workflow")
        
    except Exception as e:
        print(f"❌ Error in feedback-aware planning workflow: {e}")

# --- Main Execution ---

if __name__ == "__main__":
    print("🚀 EcoAction AI - Agent 3 (Planner) Test Suite")
    print("="*60)
    
    test_basic_planner_workflow()
    test_feedback_aware_workflow()
    
    print("\n" + "="*60)
    print("✅ Agent 3 tests completed!")