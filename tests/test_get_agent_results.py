#!/usr/bin/env python3
"""Test script to check get_agent_results specifically"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_model.database import get_agent_results, check_agents_status
    print("✅ Successfully imported database functions")
    
    # Use the user ID we saw in the debug output
    test_user_id = "55c68ce3-97f1-48e7-baf7-a6f0f714af60"
    
    print(f"\n🔍 Testing get_agent_results for user: {test_user_id[:8]}...")
    
    # Test get_agent_results
    agent_results = get_agent_results(test_user_id)
    
    if agent_results:
        print("✅ get_agent_results returned data!")
        print(f"📊 Keys in result: {list(agent_results.keys())}")
        
        if 'weekly_plan_data' in agent_results:
            weekly_data = agent_results['weekly_plan_data']
            print(f"📅 Weekly plan data found: {type(weekly_data)}")
            print(f"📅 Weekly plan keys: {list(weekly_data.keys()) if isinstance(weekly_data, dict) else 'Not a dict'}")
            
            if isinstance(weekly_data, dict) and 'challenges' in weekly_data:
                challenges = weekly_data['challenges']
                print(f"🎯 Found {len(challenges)} challenges")
                if challenges:
                    print(f"🎯 First challenge: {challenges[0].get('title', 'No title')}")
        
        if 'carbon_footprint_data' in agent_results:
            print("📈 Carbon footprint data found!")
        
    else:
        print("❌ get_agent_results returned None or empty")
    
    # Test check_agents_status
    print(f"\n🔍 Testing check_agents_status...")
    status = check_agents_status(test_user_id)
    print(f"📊 Agent status: {status}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
