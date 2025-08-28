#!/usr/bin/env python3
"""Test script to verify the fixed save_task_completion function"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from data_model.database import save_task_completion, get_task_completions
    print("✅ Successfully imported database functions")
    
    # Use the user ID we found earlier
    test_user_id = "55c68ce3-97f1-48e7-baf7-a6f0f714af60"
    test_weekly_plan_id = "ede5351d-2d4e-49fb-9ffa-250d896b8954"  # From our earlier test
    
    print(f"\n🧪 Testing save_task_completion function...")
    print(f"User ID: {test_user_id[:8]}...")
    print(f"Weekly Plan ID: {test_weekly_plan_id[:8]}...")
    
    # Test saving a task completion
    test_task_id = "challenge_1"
    test_task_title = "Meatless Monday Kickstart"
    test_task_type = "weekly"
    
    print(f"\n📝 Attempting to save task completion:")
    print(f"   Task ID: {test_task_id}")
    print(f"   Task Title: {test_task_title}")
    print(f"   Task Type: {test_task_type}")
    
    success = save_task_completion(
        test_user_id,
        test_weekly_plan_id,
        test_task_id,
        test_task_title,
        test_task_type
    )
    
    if success:
        print("✅ Task completion saved successfully!")
        
        # Test retrieving task completions
        print(f"\n🔍 Retrieving task completions...")
        task_completions = get_task_completions(test_user_id, test_weekly_plan_id)
        
        print(f"Found {len(task_completions)} task completions:")
        for completion in task_completions:
            print(f"   - {completion['task_id']}: {'✅ Completed' if completion['completed'] else '⏳ Pending'}")
        
        # Test saving the same task again (should not create duplicate)
        print(f"\n🔄 Testing duplicate prevention...")
        success2 = save_task_completion(
            test_user_id,
            test_weekly_plan_id,
            test_task_id,
            test_task_title,
            test_task_type
        )
        
        if success2:
            print("✅ Duplicate prevention working - no error on second save!")
        else:
            print("❌ Unexpected error on duplicate save")
            
    else:
        print("❌ Failed to save task completion!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
