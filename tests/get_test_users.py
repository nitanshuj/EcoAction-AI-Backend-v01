#!/usr/bin/env python3
"""
Get user IDs from database to test with
"""

from data_model.database import get_supabase

def get_test_user_ids():
    """Get some user IDs from the database for testing"""
    try:
        supabase = get_supabase()
        
        # Get first few users with profiler results
        response = supabase.table('users')\
            .select('id, user_profile')\
            .not_.is_('user_profile', 'null')\
            .limit(3)\
            .execute()
        
        if response.data:
            print("Available users with profiles:")
            for user in response.data:
                user_id = user['id']
                has_profile = bool(user.get('user_profile'))
                print(f"  - {user_id}: Has profile: {has_profile}")
            
            return [user['id'] for user in response.data]
        else:
            print("No users found with profiles")
            return []
            
    except Exception as e:
        print(f"Error getting user IDs: {str(e)}")
        return []

if __name__ == "__main__":
    user_ids = get_test_user_ids()
    if user_ids:
        print(f"\nFirst user ID to test with: {user_ids[0]}")
    else:
        print("No user IDs available for testing")
