# tests/test_agent_3.py
"""
Agent 3 (Planner) Tests - Simplified
Focus only on Agent 3 planning workflows with unique JSON parsing functions.
"""

import sys, os, json, warnings
warnings.filterwarnings("ignore")

# Add the parent directory to Python path so we can import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.crew import (
    run_planner_workflow,
    run_feedback_aware_planning_workflow,
    run_update_planning_workflow
)
from agent.utils import parse_agent3_text_output


# ============================================================================
# Agent 3 (Task: Initial generation)
# Output: json file (Use only utils functions for json parsing (made uniquely for each task))
# ============================================================================

def test_initial_generation(test_data):
    """Test Agent 3 initial challenge generation"""
    print("=" * 80)
    print("AGENT 3 (TASK: INITIAL GENERATION)")
    print("=" * 80)

    try:
        print("🔄 Running initial challenge generation...")
        # Run the workflow
        results = run_planner_workflow(user_id="test-user-123", test_data=test_data)

        if not results:
            print("❌ No results from initial generation")
            return False

        # Parse using utils function (unique for this task)
        if isinstance(results, str):
            parsed_data = parse_agent3_text_output(results, task_type="initial")
        else:
            print("Could not parse results and conver to JSON!!")
            parsed_data = results

        print("✅ Initial generation completed successfully!")
        print(f"📋 Generated {len(parsed_data.get('challenges', []))} challenges")

        # Display results
        print("\n" + "=" * 50)
        print("Raw Output: Task 1-Initial Challenge Generation)")
        print("=" * 50)
        print(json.dumps(parsed_data, indent=2))

        return True

    except Exception as e:
        print(f"❌ Error in initial generation: {e}")
        return False


# ============================================================================
# Agent 3 (Task: feedback based generation)
# Input: A feedback (hard-coded)
# Output: json_file with new challenges. Use only utils functions for json parsing (made uniquely for each task)
# ============================================================================

def test_feedback_based_generation(test_data):
    """Test Agent 3 feedback-based challenge generation"""
    print("=" * 80)
    print("AGENT 3 (TASK: FEEDBACK BASED GENERATION)")
    print("=" * 80)

    # Hard-coded feedback input
    feedback_text = "I found the transportation challenges too difficult since I live far from work. Can you suggest more home-based activities?"

    print(f"📝 Input Feedback: {feedback_text}")

    try:
        print("🔄 Running feedback-based generation...")

    # Run the workflow with feedback (test_data provided by caller)
        results = run_feedback_aware_planning_workflow(
            user_id="test-user-123",
            raw_feedback=feedback_text,
            test_data=test_data
        )

        if not results:
            print("❌ No results from feedback-based generation")
            return False

        # Parse using utils function (unique for this task)
        if isinstance(results, str):
            parsed_data = parse_agent3_text_output(results, task_type="feedback")
        else:
            parsed_data = results

        print("✅ Feedback-based generation completed successfully!")
        print(f"📋 Generated {len(parsed_data.get('challenges', []))} challenges")

        # Display results
        print("\n" + "=" * 50)
        print("Raw Output: Task 2-Feedback Based Generation")
        print("=" * 50)
        print(json.dumps(parsed_data, indent=2))

        return True

    except Exception as e:
        print(f"❌ Error in feedback-based generation: {e}")
        return False


# ============================================================================
# Agent 3 (Task: Updating the tasks)
# Just click a button, and the tasks are updated.
# Output: json_file with new tasks (Use only utils functions for json parsing (made uniquely for each task))
# ============================================================================

def test_updating_tasks(test_data):
    """Test Agent 3 task updating"""
    print("=" * 80)
    print("AGENT 3 (TASK: UPDATING THE TASKS)")
    print("=" * 80)

    # Simulate button click with update text
    update_text = "I completed 4 out of 6 challenges this week! The recycling one was easy but the public transport challenge was hard because of bad weather."

    print(f"🔘 Button clicked with update: {update_text}")

    try:
        print("🔄 Running task update...")

    # Run the workflow with update (test_data provided by caller)
        results = run_update_planning_workflow(
            user_id="test-user-123",
            user_update_text=update_text,
            test_data=test_data
        )

        if not results:
            print("❌ No results from task update")
            return False

        # Parse using utils function (unique for this task)
        if isinstance(results, str):
            parsed_data = parse_agent3_text_output(results, task_type="update")
        else:
            parsed_data = results

        print("✅ Task update completed successfully!")
        print(f"📋 Generated {len(parsed_data.get('challenges', []))} new challenges")

        # Display results
        print("\n" + "=" * 50)
        print("Raw Output: Task 3-Updating the tasks")
        print("=" * 50)
        print(json.dumps(parsed_data, indent=2))
        print("=" * 50)

        return True

    except Exception as e:
        print(f"❌ Error in task update: {e}")
        return False


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def run_all_tests(test_data):
    """Run all Agent 3 tests"""
    print("=" * 80)
    print("AGENT 3 TEST SUITE - SIMPLIFIED")
    print("=" * 80)

    test_results = []

    # Run all three tests (pass test_data through)
    test_results.append(("Initial Generation", test_initial_generation(test_data)))
    test_results.append(("Feedback-Based Generation", test_feedback_based_generation(test_data)))
    test_results.append(("Task Updating", test_updating_tasks(test_data)))

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed_tests = 0
    total_tests = len(test_results)

    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
        if result:
            passed_tests += 1

    print(f"\nOVERALL RESULT: {passed_tests}/{total_tests} tests passed")

    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Agent 3 is working correctly.")
    elif passed_tests > 0:
        print("⚠️ SOME TESTS FAILED. Review the failed tests above.")
    else:
        print("❌ ALL TESTS FAILED. Agent 3 needs debugging.")

    return passed_tests == total_tests


if __name__ == "__main__":
    # Run all tests
    print("Running Agent 3 simplified test suite...")
    print("This will test all 3 Agent 3 workflows with real data from test-file-3.json")
    print()

    # Load the test JSON once and pass it into each test.
    # Assumption: the test JSON is located at experimentation/test-json-3-enhanced-profile.json
    test_file_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "tests",
        "test-file-3.json",
    )

    if not os.path.exists(test_file_path):
        print(f"Test file not found: {test_file_path}")
        print("Please provide the correct path to your test JSON file.")
        sys.exit(1)

    with open(test_file_path, "r", encoding="utf-8") as fh:
        test_data = json.load(fh)

    run_all_tests(test_data)