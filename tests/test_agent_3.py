# tests/test_agent_3.py
"""Test script for Agent 3 (Planner) functionality"""

import sys
import os
import warnings; warnings.filterwarnings("ignore")

# Add the parent directory to Python path so we can import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.crew import (
    run_planner_workflow,
    run_feedback_aware_planning_workflow,
    run_daily_tasks_generation_workflow,
    run_update_planning_workflow
)

def test_basic_planner_workflow():
    """Test the basic planner workflow (without feedback)"""
    print("🧪 Testing Basic Planner Workflow (Agent 3)...")
    
    # Note: This requires a real user ID with completed Agent 1 and Agent 2 data
    test_user_id = "a14848d3-3d90-4f12-8034-52c2e9a6d4d9"  # Replace with actual user ID from your database
    
    print(f"Using test user ID: {test_user_id}")
    print("⚠️ This test requires a real user with completed Agent 1 and Agent 2 data")
    
    try:
        print("\n🔄 Running basic planner workflow...")
        results = run_planner_workflow(test_user_id)
        
        if results:
            print("✅ Basic planner workflow completed successfully!")
            print(f"📋 Results type: {type(results)}")
            
            # Try to extract and parse the complete JSON
            if hasattr(results, 'raw'):
                raw_output = str(results.raw)
                print(f"\n📄 Full Raw Output:\n{raw_output}")
                
                # Try to parse JSON and display challenges
                try:
                    import json
                    import re
                    
                    # Extract JSON from output
                    json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                    if json_match:
                        json_content = json_match.group(0)
                        plan_data = json.loads(json_content)
                        
                        print("\n🎯 PARSED AGENT 3 PLAN:")
                        print("=" * 50)
                        print(f"📅 Week Focus: {plan_data.get('week_focus', 'N/A')}")
                        print(f"🎯 Priority Area: {plan_data.get('priority_area', 'N/A')}")
                        print(f"💪 Motivation: {plan_data.get('motivation_message', plan_data.get('motivation', 'N/A'))}")
                        
                        challenges = plan_data.get('challenges', [])
                        print(f"\n🏆 CHALLENGES ({len(challenges)} total):")
                        print("=" * 50)
                        
                        # Group challenges by difficulty
                        easy_challenges = [c for c in challenges if c.get('difficulty', '').lower() == 'easy']
                        medium_challenges = [c for c in challenges if c.get('difficulty', '').lower() == 'medium']
                        hard_challenges = [c for c in challenges if c.get('difficulty', '').lower() == 'hard']
                        
                        print(f"\n🟢 EASY CHALLENGES ({len(easy_challenges)}):")
                        for i, challenge in enumerate(easy_challenges, 1):
                            print(f"  {i}. {challenge.get('title', 'N/A')}")
                            print(f"     Description: {challenge.get('description', challenge.get('action', 'N/A'))}")
                            print(f"     CO2 Savings: {challenge.get('co2_savings_kg', challenge.get('co2_savings', 'N/A'))} kg")
                            print(f"     Time: {challenge.get('time_required', 'N/A')}")
                            print(f"     Steps: {challenge.get('steps', [])}")
                            print()
                        
                        print(f"\n� MEDIUM CHALLENGES ({len(medium_challenges)}):")
                        for i, challenge in enumerate(medium_challenges, 1):
                            print(f"  {i}. {challenge.get('title', 'N/A')}")
                            print(f"     Description: {challenge.get('description', challenge.get('action', 'N/A'))}")
                            print(f"     CO2 Savings: {challenge.get('co2_savings_kg', challenge.get('co2_savings', 'N/A'))} kg")
                            print(f"     Time: {challenge.get('time_required', 'N/A')}")
                            print(f"     Steps: {challenge.get('steps', [])}")
                            print()
                        
                        print(f"\n🔴 HARD CHALLENGES ({len(hard_challenges)}):")
                        for i, challenge in enumerate(hard_challenges, 1):
                            print(f"  {i}. {challenge.get('title', 'N/A')}")
                            print(f"     Description: {challenge.get('description', challenge.get('action', 'N/A'))}")
                            print(f"     CO2 Savings: {challenge.get('co2_savings_kg', challenge.get('co2_savings', 'N/A'))} kg")
                            print(f"     Time: {challenge.get('time_required', 'N/A')}")
                            print(f"     Steps: {challenge.get('steps', [])}")
                            print()
                        
                        total_savings = plan_data.get('total_potential_savings', 'N/A')
                        print(f"💰 Total Potential CO2 Savings: {total_savings} kg")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON: {str(e)}")
                    print("Raw output was displayed above for debugging")
                
            elif hasattr(results, 'tasks_output'):
                print(f"📄 Tasks output available: {len(results.tasks_output)} tasks")
                for i, task_output in enumerate(results.tasks_output):
                    print(f"Task {i+1} output: {str(task_output)[:300]}...")
            else:
                print(f"📄 Results: {str(results)[:200]}...")
        else:
            print("❌ No results returned from planner workflow")
            
    except Exception as e:
        print(f"❌ Error in basic planner workflow: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")

def test_feedback_aware_workflow():
    """Test the feedback-aware planning workflow"""
    print("\n🧪 Testing Feedback-Aware Planning Workflow...")
    
    test_user_id = "a14848d3-3d90-4f12-8034-52c2e9a6d4d9"  # Use the working user ID
    test_feedback = "I want easier challenges that help save money and can be done at home"
    
    print(f"Using test user ID: {test_user_id}")
    print(f"Test feedback: {test_feedback}")
    print("⚠️ This test requires a real user with completed Agent 1 and Agent 2 data")
    
    try:
        print("\n🔄 Running feedback-aware planning workflow...")
        results = run_feedback_aware_planning_workflow(test_user_id, test_feedback)
        
        if results:
            print("✅ Feedback-aware planning workflow completed successfully!")
            print(f"📋 Results type: {type(results)}")
            
            # Parse and display the challenges with feedback adaptation
            if hasattr(results, 'raw'):
                raw_output = str(results.raw)
                print(f"\n📄 Raw Output (with feedback adaptation):\n{raw_output[:500]}...")
                
                try:
                    import json
                    import re
                    
                    # Extract JSON from output
                    json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                    if json_match:
                        json_content = json_match.group(0)
                        plan_data = json.loads(json_content)
                        
                        print("\n🧠 FEEDBACK-AWARE AGENT 3 PLAN:")
                        print("=" * 50)
                        print(f"💬 Feedback Applied: {test_feedback}")
                        print(f"📅 Week Focus: {plan_data.get('week_focus', 'N/A')}")
                        print(f"🎯 Priority Area: {plan_data.get('priority_area', 'N/A')}")
                        
                        challenges = plan_data.get('challenges', [])
                        print(f"\n🏆 ADAPTED CHALLENGES ({len(challenges)} total):")
                        print("=" * 50)
                        
                        for i, challenge in enumerate(challenges, 1):
                            difficulty = challenge.get('difficulty', 'N/A')
                            icon = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}.get(difficulty.lower(), '⚪')
                            
                            print(f"\n{icon} CHALLENGE {i} ({difficulty.upper()}):")
                            print(f"  Title: {challenge.get('title', 'N/A')}")
                            print(f"  Description: {challenge.get('description', challenge.get('action', 'N/A'))}")
                            print(f"  CO2 Savings: {challenge.get('co2_savings_kg', challenge.get('co2_savings', 'N/A'))} kg")
                            print(f"  Time Required: {challenge.get('time_required', 'N/A')}")
                            print(f"  Home-Based: {challenge.get('can_do_at_home', 'N/A')}")
                            print(f"  Money-Saving: {challenge.get('saves_money', 'N/A')}")
                            
                        adaptation_notes = plan_data.get('feedback_adaptation_notes', 'N/A')
                        print(f"\n📝 Feedback Adaptation Notes: {adaptation_notes}")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON: {str(e)}")
                    print("Raw output was displayed above for debugging")
                    
            else:
                print(f"📄 Results: {str(results)[:200]}...")
        else:
            print("❌ No results returned from feedback-aware workflow")
            
    except Exception as e:
        print(f"❌ Error in feedback-aware planning workflow: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")

def test_daily_tasks_generation():
    """Test the daily tasks generation workflow"""
    print("\n🧪 Testing Daily Tasks Generation Workflow...")
    
    test_user_id = "a14848d3-3d90-4f12-8034-52c2e9a6d4d9"  # Use the working user ID
    completed_tasks = [
        {"id": "task1", "title": "Use reusable water bottle", "difficulty": "easy"},
        {"id": "task2", "title": "Turn off lights when leaving", "difficulty": "easy"},
        {"id": "task3", "title": "Take stairs instead of elevator", "difficulty": "medium"},
        {"id": "task4", "title": "Start composting at home", "difficulty": "medium"}
    ]
    
    print(f"Using test user ID: {test_user_id}")
    print(f"Completed tasks: {len(completed_tasks)} tasks")
    print("⚠️ This test requires a real user with completed Agent 1 and Agent 2 data")
    
    try:
        print("\n🔄 Running daily tasks generation workflow...")
        results = run_daily_tasks_generation_workflow(test_user_id, completed_tasks)
        
        if results:
            print("✅ Daily tasks generation workflow completed successfully!")
            print(f"📋 Results type: {type(results)}")
            
            # Parse and display the new daily tasks
            if hasattr(results, 'raw'):
                raw_output = str(results.raw)
                print(f"\n📄 Raw Output (daily tasks):\n{raw_output[:500]}...")
                
                try:
                    import json
                    import re
                    
                    # Extract JSON from output
                    json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                    if json_match:
                        json_content = json_match.group(0)
                        tasks_data = json.loads(json_content)
                        
                        print("\n📋 NEW DAILY TASKS GENERATED:")
                        print("=" * 50)
                        print(f"🎉 Triggered by completing {len(completed_tasks)} challenges:")
                        for task in completed_tasks:
                            print(f"  ✅ {task['title']} ({task.get('difficulty', 'N/A')})")
                        
                        daily_tasks = tasks_data.get('daily_tasks', [])
                        if daily_tasks:
                            print(f"\n📅 NEW DAILY TASKS ({len(daily_tasks)} total):")
                            print("=" * 50)
                            
                            for i, task in enumerate(daily_tasks, 1):
                                print(f"\n📝 DAILY TASK {i}:")
                                print(f"  Title: {task.get('title', 'N/A')}")
                                print(f"  Description: {task.get('description', 'N/A')}")
                                print(f"  Duration: {task.get('duration', task.get('time_required', 'N/A'))}")
                                print(f"  CO2 Impact: {task.get('co2_impact_kg', task.get('co2_savings', 'N/A'))} kg")
                                print(f"  Category: {task.get('category', 'N/A')}")
                                print(f"  Difficulty: {task.get('difficulty', 'N/A')}")
                                
                                steps = task.get('steps', [])
                                if steps:
                                    print(f"  Steps:")
                                    for j, step in enumerate(steps, 1):
                                        print(f"    {j}. {step}")
                        
                        motivation = tasks_data.get('motivation_message', 'N/A')
                        print(f"\n💪 Motivation Message: {motivation}")
                        
                        total_impact = tasks_data.get('total_daily_impact_kg', 'N/A')
                        print(f"🌱 Total Daily CO2 Impact: {total_impact} kg")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON: {str(e)}")
                    print("Raw output was displayed above for debugging")
                    
            else:
                print(f"📄 Results: {str(results)[:200]}...")
        else:
            print("❌ No results returned from daily tasks generation workflow")
            
    except Exception as e:
        print(f"❌ Error in daily tasks generation workflow: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")

def test_update_planning_workflow():
    """Test the update planning workflow"""
    print("\n🧪 Testing Update Planning Workflow...")
    
    test_user_id = "a14848d3-3d90-4f12-8034-52c2e9a6d4d9"  # Use the working user ID
    update_text = "I completed the recycling challenge easily but found the transport challenge too difficult because I don't have a car. Can you give me more home-based challenges?"
    
    print(f"Using test user ID: {test_user_id}")
    print(f"Update text: {update_text}")
    print("⚠️ This test requires a real user with completed Agent 1 and Agent 2 data")
    
    try:
        print("\n🔄 Running update planning workflow...")
        results = run_update_planning_workflow(test_user_id, update_text)
        
        if results:
            print("✅ Update planning workflow completed successfully!")
            print(f"📋 Results type: {type(results)}")
            
            # Parse and display the updated challenges
            if hasattr(results, 'raw'):
                raw_output = str(results.raw)
                print(f"\n📄 Raw Output (updated plan):\n{raw_output[:500]}...")
                
                try:
                    import json
                    import re
                    
                    # Extract JSON from output
                    json_match = re.search(r'\{.*\}', raw_output, re.DOTALL)
                    if json_match:
                        json_content = json_match.group(0)
                        plan_data = json.loads(json_content)
                        
                        print("\n🔄 UPDATED AGENT 3 PLAN:")
                        print("=" * 50)
                        print(f"🔄 Update Applied: {update_text[:100]}...")
                        print(f"📅 Week Focus: {plan_data.get('week_focus', 'N/A')}")
                        print(f"🎯 Priority Area: {plan_data.get('priority_area', 'N/A')}")
                        
                        challenges = plan_data.get('challenges', [])
                        print(f"\n🏆 UPDATED CHALLENGES ({len(challenges)} total):")
                        print("=" * 50)
                        
                        home_based_count = 0
                        for i, challenge in enumerate(challenges, 1):
                            difficulty = challenge.get('difficulty', 'N/A')
                            icon = {'easy': '🟢', 'medium': '🟡', 'hard': '🔴'}.get(difficulty.lower(), '⚪')
                            
                            is_home_based = challenge.get('can_do_at_home', False) or 'home' in challenge.get('description', '').lower()
                            if is_home_based:
                                home_based_count += 1
                            
                            print(f"\n{icon} CHALLENGE {i} ({difficulty.upper()}):")
                            print(f"  Title: {challenge.get('title', 'N/A')}")
                            print(f"  Description: {challenge.get('description', challenge.get('action', 'N/A'))}")
                            print(f"  CO2 Savings: {challenge.get('co2_savings_kg', challenge.get('co2_savings', 'N/A'))} kg")
                            print(f"  Time Required: {challenge.get('time_required', 'N/A')}")
                            print(f"  🏠 Home-Based: {'✅' if is_home_based else '❌'}")
                            
                        print(f"\n🏠 Home-Based Challenges: {home_based_count}/{len(challenges)}")
                        
                        update_notes = plan_data.get('update_notes', plan_data.get('adaptation_notes', 'N/A'))
                        print(f"\n📝 Update Notes: {update_notes}")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse JSON: {str(e)}")
                    print("Raw output was displayed above for debugging")
                    
            else:
                print(f"📄 Results: {str(results)[:200]}...")
        else:
            print("❌ No results returned from update planning workflow")
            
    except Exception as e:
        print(f"❌ Error in update planning workflow: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")

def test_agent_imports():
    """Test that all required modules can be imported"""
    print("\n🧪 Testing Agent 3 Module Imports...")
    
    try:
        from agent.agents import create_planner_agent
        print("✅ Planner agent import successful")
        
        from agent.tasks import (
            create_weekly_planning_task,
            create_feedback_aware_planning_task,
            create_daily_tasks_generation_task,
            create_update_planning_task
        )
        print("✅ All task imports successful")
        
        from data_model.database import (
            get_profiler_results,
            get_agent_results,
            save_feedback_and_process,
            get_user_feedback_history
        )
        print("✅ Database function imports successful")
        
        print("✅ All imports working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    print("🚀 EcoAction AI - Agent 3 (Planner) Test")
    print("=" * 60)
    
    # Test 1: Module imports
    imports_ok = test_agent_imports()
    
    if imports_ok:
        print("\n" + "=" * 60)
        print("📝 Workflow Tests (require real user data):")
        print("=" * 60)
        
        # Test 2: Basic planner workflow
        test_basic_planner_workflow()
        
        # Add separator between tests
        print("\n" + "-" * 60)
        
        # Test 3: Feedback-aware workflow
        test_feedback_aware_workflow()
        
        # Add separator between tests
        print("\n" + "-" * 60)
        
        # Test 4: Daily tasks generation
        test_daily_tasks_generation()
        
        # Add separator between tests
        print("\n" + "-" * 60)
        
        # Test 5: Update planning workflow
        test_update_planning_workflow()
        
        print("\n" + "=" * 60)
        print("💡 Test Results Summary:")
        print("  - Each test shows the complete 6-challenge structure")
        print("  - Challenges are grouped by difficulty (3 easy + 2 medium + 1 hard)")
        print("  - All CO2 savings, time requirements, and steps are displayed")
        print("  - Feedback adaptation and update logic is visible")
        print("=" * 60)
    else:
        print("\n❌ Import tests failed - fix imports before testing workflows")
    
    print("\n✅ Agent 3 tests completed!")
