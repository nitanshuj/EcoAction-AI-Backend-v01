#!/usr/bin/env python3
"""Test script to debug database functions"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from data_model.database import debug_weekly_plans, debug_user_actions, get_supabase
    print("✅ Successfully imported database functions")
    
    # Test Supabase connection
    try:
        supabase = get_supabase()
        print("✅ Supabase client initialized")
        
        # Try to get a sample of weekly_plans to see the table structure
        response = supabase.table('weekly_plans').select('*').limit(3).execute()
        print(f"✅ Weekly plans table query successful. Found {len(response.data)} records.")
        
        if response.data:
            for i, plan in enumerate(response.data):
                print(f"  Plan {i+1}: user_id={plan.get('user_id', 'N/A')}, week_of={plan.get('week_of', 'N/A')}")
                print(f"    Has suggestions: {'suggestions' in plan and plan['suggestions'] is not None}")
                if plan.get('suggestions'):
                    print(f"    Suggestions keys: {list(plan['suggestions'].keys()) if isinstance(plan['suggestions'], dict) else 'Not a dict'}")
        
        # Test user_actions table
        response2 = supabase.table('user_actions').select('*').limit(3).execute()
        print(f"✅ User actions table query successful. Found {len(response2.data)} records.")
        
    except Exception as e:
        print(f"❌ Database query error: {e}")
        
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ General error: {e}")
