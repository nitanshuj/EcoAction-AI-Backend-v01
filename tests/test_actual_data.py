#!/usr/bin/env python3
"""Test script to verify the actual data from database displays correctly"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_model.database import get_agent_results, get_latest_weekly_plan
    print("✅ Successfully imported database functions")
    
    # Use the user ID we found earlier
    test_user_id = "55c68ce3-97f1-48e7-baf7-a6f0f714af60"
    
    print(f"\n🔍 Testing with actual user data: {test_user_id[:8]}...")
    
    # Get agent results
    agent_results = get_agent_results(test_user_id)
    
    if agent_results and 'weekly_plan_data' in agent_results:
        weekly_plan_data = agent_results['weekly_plan_data']
        print("✅ Found weekly plan data!")
        
        # Extract challenges
        weekly_challenges = weekly_plan_data.get('challenges', weekly_plan_data.get('weekly_challenges', []))
        
        if weekly_challenges:
            print(f"✅ Found {len(weekly_challenges)} challenges!")
            
            for i, challenge in enumerate(weekly_challenges, 1):
                # Test the exact logic from the dashboard
                challenge_title = challenge.get('title', f'Challenge {i}')
                challenge_difficulty = challenge.get('difficulty', challenge.get('difficulty_level', 'medium')).upper()
                co2_savings = challenge.get('co2_savings_kg', challenge.get('co2_savings', challenge.get('estimated_co2_savings_kg', 0)))
                description = challenge.get('description', challenge.get('action', ''))
                category = challenge.get('category', 'General').title()
                time_required = challenge.get('time_required', challenge.get('time', 'N/A'))
                
                print(f"\n🎯 Challenge {i}: {challenge_title}")
                print(f"   Difficulty: {challenge_difficulty}")
                print(f"   Category: {category}")
                print(f"   CO2 Savings: {co2_savings} kg")
                print(f"   Time: {time_required}")
                print(f"   Description: {description[:80]}...")
            
            # Test the weekly plan info
            week_focus = weekly_plan_data.get('week_focus', 'Sustainable Actions')
            motivation_message = weekly_plan_data.get('motivation_message', weekly_plan_data.get('motivation', ''))
            total_savings = weekly_plan_data.get('total_potential_savings', 0)
            
            print(f"\n📅 Week Focus: {week_focus}")
            print(f"💪 Motivation: {motivation_message[:100]}...")
            print(f"🌍 Total Potential Savings: {total_savings} kg CO₂")
            
            print(f"\n✅ Dashboard should successfully display all {len(weekly_challenges)} challenges!")
            
        else:
            print("❌ No challenges found in weekly plan data")
    else:
        print("❌ No weekly plan data found")
        
    # Also test the latest weekly plan function
    print(f"\n🔍 Testing get_latest_weekly_plan...")
    latest_plan = get_latest_weekly_plan(test_user_id)
    if latest_plan:
        plan_id = latest_plan['id']
        print(f"✅ Found latest weekly plan: {plan_id}")
        print(f"   Week of: {latest_plan.get('week_of', 'N/A')}")
        print(f"   Has suggestions: {'suggestions' in latest_plan}")
    else:
        print("❌ No latest weekly plan found")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
