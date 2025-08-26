# Functions for user profiles & action logging (Supabase)
# utils/database.py
import streamlit as st
import pandas as pd
# Functions for user profiles & action logging (Supabase)
# utils/database.py
import streamlit as st
from datetime import date, timedelta
from supabase import Client
from .supabase_client import init_supabase

def get_supabase() -> Client:
    """Initialize and return the Supabase client."""
    return init_supabase()



def fetch_user_profile(user_id: str):
    """
    Fetch user profile from Supabase.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: User profile data or None if not found
    """
    try:
        supabase = get_supabase()
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        st.error(f"Error fetching user profile: {str(e)}")
        return None

def save_onboarding_data(user_id: str, onboarding_data: dict) -> bool:
    """
    Save or update user onboarding data in Supabase user_profiles table.
   
    Args:
        user_id (str): The user's UUID
        onboarding_data (dict): The onboarding form data
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        # Upsert the profile data in user_profiles table
        response = supabase.table('user_profiles').upsert({
            'user_id': user_id,
            'onboarding_data': onboarding_data
        }).execute()
        
        if response.data:
            # Don't update onboarding_status yet - wait for agent conversation to complete
            # The onboarding_status will be updated when finish_conversation() is called
            return True
        
        return False
        
    except Exception as e:
        st.error(f"Error saving onboarding data: {str(e)}")
        return False

def update_onboarding_status(user_id: str, status: bool = True) -> bool:
    """
    Update user's onboarding status.
    
    Args:
        user_id (str): The user's UUID
        status (bool): Onboarding completion status
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('users')\
            .update({'onboarding_status': status})\
            .eq('id', user_id)\
            .execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error updating onboarding status: {str(e)}")
        return False


def log_user_action(user_id: str, action_id: str, co2_saved: float) -> bool:
    """
    Log a completed user action in Supabase.
    
    Args:
        user_id (str): The user's UUID
        action_id (str): The ID of the completed action
        co2_saved (float): The CO2 saved by this action
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_actions').insert({
            'user_id': user_id,
            'action_id': action_id,
            'co2_saved': co2_saved
        }).execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error logging user action: {str(e)}")
        return False

def get_user_actions(user_id: str, limit: int = 50):
    """
    Get recent actions for a user.
    
    Args:
        user_id (str): The user's UUID
        limit (int): Number of actions to return
        
    Returns:
        list: List of user actions
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_actions')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('completed_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data
        
    except Exception as e:
        st.error(f"Error fetching user actions: {str(e)}")
        return []

def get_user_total_co2_saved(user_id: str) -> float:
    """
    Get total CO2 saved by a user.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        float: Total CO2 saved in kg
    """
    try:
        supabase = get_supabase()
        
        # Simple aggregation query since tables exist in Supabase
        response = supabase.table('user_actions')\
            .select('co2_saved')\
            .eq('user_id', user_id)\
            .execute()
        
        if response.data:
            total = sum(float(action['co2_saved']) for action in response.data)
            return total
        return 0.0
        
    except Exception as e:
        st.error(f"Error calculating total CO2 saved: {str(e)}")
        return 0.0

def get_country(user_id: str):
    """
    Get the user's country from Supabase.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        str: The user's country
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('users')\
            .select('country')\
            .eq('id', user_id)\
            .execute()
        
        if response.data:
            return response.data[0].get('country', '')
        return ''
        
    except Exception as e:
        st.error(f"Error fetching user country: {str(e)}")
        return ''

def get_user_recent_actions(user_id: str, limit: int = 10):
    """
    Get user's recent actions from Supabase.
    
    Args:
        user_id (str): The user's UUID
        limit (int): Number of recent actions to return
        
    Returns:
        list: Recent actions with action_id, completed_at, and co2_saved
    """
    try:
        supabase = get_supabase()
        
        # Direct query to existing table
        response = supabase.table('user_actions')\
            .select('action_id, completed_at, co2_saved')\
            .eq('user_id', user_id)\
            .order('completed_at', desc=True)\
            .limit(limit)\
            .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        st.error(f"Error fetching recent actions: {str(e)}")
        return []

def get_community_challenges(active_only: bool = True):
    """
    Get community challenges from Supabase.
    
    Args:
        active_only (bool): Whether to return only active challenges
        
    Returns:
        list: List of community challenges
    """
    try:
        supabase = get_supabase()
        
        query = supabase.table('community_challenges').select('*')
        
        if active_only:
            query = query.eq('is_active', True)
            
        response = query.order('created_at', desc=True).execute()
        
        return response.data
        
    except Exception as e:
        st.error(f"Error fetching community challenges: {str(e)}")
        return []

def join_community_challenge(user_id: str, challenge_id: str) -> bool:
    """
    Join a community challenge.
    
    Args:
        user_id (str): The user's UUID
        challenge_id (str): The challenge UUID
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_challenges').insert({
            'user_id': user_id,
            'challenge_id': challenge_id
        }).execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error joining challenge: {str(e)}")
        return False

def get_user_challenges(user_id: str):
    """
    Get challenges that a user has joined.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        list: List of user's challenges
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_challenges')\
            .select('*, community_challenges(*)')\
            .eq('user_id', user_id)\
            .execute()
        
        return response.data
        
    except Exception as e:
        st.error(f"Error fetching user challenges: {str(e)}")
        return []

def get_user_progress_summary(user_id: str):
    """
    Get user progress summary from existing Supabase tables.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: User progress summary
    """
    try:
        supabase = get_supabase()
        
        # Get user profile
        profile_response = supabase.table('users')\
            .select('*')\
            .eq('id', user_id)\
            .execute()
        
        # Get user actions
        actions_response = supabase.table('user_actions')\
            .select('*')\
            .eq('user_id', user_id)\
            .execute()
        
        actions = actions_response.data if actions_response.data else []
        
        # Calculate summary
        total_actions = len(actions)
        total_co2_saved = sum(float(action['co2_saved']) for action in actions)
        last_action_date = None
        
        if actions:
            # Sort by completed_at and get the latest
            sorted_actions = sorted(actions, key=lambda x: x['completed_at'], reverse=True)
            last_action_date = sorted_actions[0]['completed_at']
        
        return {
            'user_id': user_id,
            'total_actions_completed': total_actions,
            'total_co2_saved': total_co2_saved,
            'last_action_date': last_action_date
        }
        
    except Exception as e:
        st.error(f"Error fetching progress summary: {str(e)}")
        # Basic fallback
        return {
            'user_id': user_id,
            'total_actions_completed': 0,
            'total_co2_saved': 0.0,
            'last_action_date': None
        }

def update_user_email(user_id: str, new_email: str) -> bool:
    """
    Update user's email in their profile.
    
    Args:
        user_id (str): The user's UUID
        new_email (str): New email address
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('users')\
            .update({'email': new_email})\
            .eq('id', user_id)\
            .execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error updating email: {str(e)}")
        return False

def check_onboarding_status(user_id: str) -> bool:
    """
    Check if user has completed onboarding.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        bool: True if onboarding completed, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('users')\
            .select('onboarding_status')\
            .eq('id', user_id)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0].get('onboarding_status', False)
        return False
        
    except Exception as e:
        st.error(f"Error checking onboarding status: {str(e)}")
        return False



def get_user_profile_data(user_id: str):
    """
    Get user onboarding data from user_profiles table.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: User profile data or None if not found
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_profiles')\
            .select('*')\
            .eq('user_id', user_id)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        return None
        
    except Exception as e:
        st.error(f"Error fetching user profile data: {str(e)}")
        return None

def create_agent_session(user_id: str, agent_type: str, initial_prompt: str) -> str:
    """
    Create a new agent session.
    
    Args:
        user_id (str): The user's UUID
        agent_type (str): Type of agent session
        initial_prompt (str): The initial prompt for the agent
        
    Returns:
        str: Agent session ID or None if failed
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('agent_sessions').insert({
            'user_id': user_id,
            'agent_type': agent_type,
            'status': 'active',
            'initial_prompt': initial_prompt
        }).execute()
        
        if response.data:
            return response.data[0]['id']
        return None
        
    except Exception as e:
        st.error(f"Error creating agent session: {str(e)}")
        return None

def update_agent_session(session_id: str, status: str, final_output: dict = None) -> bool:
    """
    Update agent session with completion status and output.
    
    Args:
        session_id (str): Agent session ID
        status (str): Session status
        final_output (dict): Final output from agent
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        update_data = {'status': status}
        if status == 'completed':
            update_data['completed_at'] = 'now()'
        if final_output:
            update_data['final_output'] = final_output
        
        response = supabase.table('agent_sessions')\
            .update(update_data)\
            .eq('id', session_id)\
            .execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error updating agent session: {str(e)}")
        return False

def save_agent_message(session_id: str, role: str, content: str) -> bool:
    """
    Save agent message to the chat history.
    
    Args:
        session_id (str): Agent session ID
        role (str): Message role (user, assistant, system)
        content (str): Message content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('agent_messages').insert({
            'agent_session_id': session_id,
            'role': role,
            'content': content
        }).execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error saving agent message: {str(e)}")
        return False

def get_agent_messages(session_id: str):
    """
    Get all messages for an agent session.
    
    Args:
        session_id (str): Agent session ID
        
    Returns:
        list: List of messages or empty list if none found
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('agent_messages')\
            .select('*')\
            .eq('agent_session_id', session_id)\
            .order('created_at')\
            .execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        st.error(f"Error fetching agent messages: {str(e)}")
        return []

def get_user_onboarding_data(user_id: str):
    """
    Get user's onboarding data for agent processing.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: Onboarding data or None if not found
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_profiles')\
            .select('onboarding_data')\
            .eq('user_id', user_id)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]['onboarding_data']
        return None
        
    except Exception as e:
        st.error(f"Error fetching onboarding data: {str(e)}")
        return None

def save_agent_results(user_id: str, agent_type: str, results: dict, agent_session_id: str = None) -> bool:
    """
    Save agent analysis results to the user_scores or weekly_plans table based on your schema.
    
    Args:
        user_id (str): The user's UUID
        agent_type (str): Type of agent (analyst, planner)
        results (dict): Agent results data
        agent_session_id (str): Optional agent session ID
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        if agent_type == 'analyst':
            # Save to user_scores table according to your schema
            # The results from Agent 2 are the complete analysis data
            # Store the full results as 'scores' and create a simple benchmark entry
            calculation_data = results  # Store the complete Agent 2 output
            benchmark_data = {
                'regional_comparison': results.get('regional_comparison', {}),
                'sustainability_score': results.get('sustainability_score', 0),
                'score_category': results.get('score_category', 'Unknown')
            }
            
            # Check if user_scores record exists
            existing_response = supabase.table('user_scores')\
                .select('*')\
                .eq('user_id', user_id)\
                .execute()
            
            if existing_response.data:
                # Update existing record
                response = supabase.table('user_scores')\
                    .update({
                        'scores': calculation_data,
                        'benchmarks': benchmark_data,
                        'agent_session_id': agent_session_id,
                        'calculated_at': 'now()'
                    })\
                    .eq('user_id', user_id)\
                    .execute()
            else:
                # Create new record
                response = supabase.table('user_scores')\
                    .insert({
                        'user_id': user_id,
                        'scores': calculation_data,
                        'benchmarks': benchmark_data,
                        'agent_session_id': agent_session_id,
                        'calculated_at': 'now()'
                    })\
                    .execute()
                    
        elif agent_type == 'planner':
            # Save to weekly_plans table according to your schema
            from datetime import datetime, date
            
            # Get current week start date (Monday)
            today = date.today()
            days_since_monday = today.weekday()
            week_start = today - timedelta(days=days_since_monday)
            
            # Check if weekly plan for this week exists
            existing_response = supabase.table('weekly_plans')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('week_of', week_start.isoformat())\
                .execute()
            
            if existing_response.data:
                # Update existing weekly plan
                response = supabase.table('weekly_plans')\
                    .update({
                        'suggestions': results,
                        'agent_session_id': agent_session_id
                    })\
                    .eq('user_id', user_id)\
                    .eq('week_of', week_start.isoformat())\
                    .execute()
            else:
                # Create new weekly plan
                response = supabase.table('weekly_plans')\
                    .insert({
                        'user_id': user_id,
                        'week_of': week_start.isoformat(),
                        'suggestions': results,
                        'agent_session_id': agent_session_id
                    })\
                    .execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error saving agent results: {str(e)}")
        return False

def get_agent_results(user_id: str):
    """
    Get agent analysis results from user_scores and weekly_plans tables.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: Combined agent results data or None if not found
    """
    try:
        supabase = get_supabase()
        
        # Get scores from user_scores table
        scores_response = supabase.table('user_scores')\
            .select('*')\
            .eq('user_id', user_id)\
            .execute()
        
        # Get current week's plan from weekly_plans table
        from datetime import date, timedelta
        today = date.today()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        
        plans_response = supabase.table('weekly_plans')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('week_of', week_start.isoformat())\
            .execute()
        
        # Combine results
        result = {}
        
        if scores_response.data and len(scores_response.data) > 0:
            scores_data = scores_response.data[0]
            result['carbon_footprint_data'] = {
                'calculation_data': scores_data.get('scores', {}),
                'benchmark_data': scores_data.get('benchmarks', {})
            }
            result['analyst_completed'] = True
        else:
            result['analyst_completed'] = False
            
        if plans_response.data and len(plans_response.data) > 0:
            plan_data = plans_response.data[0]
            result['weekly_plan_data'] = plan_data.get('suggestions', {})
            result['planner_completed'] = True
        else:
            result['planner_completed'] = False
        
        return result if result else None
        
    except Exception as e:
        st.error(f"Error fetching agent results: {str(e)}")
        return None

def check_agents_status(user_id: str):
    """
    Check the completion status of agents for a user based on existing data.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: Status of agents (analyst_completed, planner_completed)
    """
    try:
        supabase = get_supabase()
        
        # Check if user_scores exists (analyst completed)
        scores_response = supabase.table('user_scores')\
            .select('id')\
            .eq('user_id', user_id)\
            .execute()
        
        analyst_completed = len(scores_response.data) > 0
        
        # Check if current week's plan exists (planner completed)
        from datetime import date, timedelta
        today = date.today()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        
        plans_response = supabase.table('weekly_plans')\
            .select('id')\
            .eq('user_id', user_id)\
            .eq('week_of', week_start.isoformat())\
            .execute()
        
        planner_completed = len(plans_response.data) > 0
        
        return {
            'analyst_completed': analyst_completed,
            'planner_completed': planner_completed
        }
        
    except Exception as e:
        st.error(f"Error checking agents status: {str(e)}")
        return {'analyst_completed': False, 'planner_completed': False}


def save_weekly_plan_results(user_id: str, session_id: str, plan_data: dict) -> bool:
    """
    Save weekly plan results to the database.
    
    Args:
        user_id (str): The user's UUID
        session_id (str): The agent session ID
        plan_data (dict): The weekly plan data
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        # Calculate week start date
        from datetime import date, timedelta
        today = date.today()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        
        response = supabase.table('weekly_plans').insert({
            'user_id': user_id,
            'agent_session_id': session_id,
            'week_of': week_start.isoformat(),
            'suggestions': plan_data
        }).execute()
        
        return len(response.data) > 0
        
    except Exception as e:
        st.error(f"Error saving weekly plan results: {str(e)}")
        return False

def get_latest_weekly_plan(user_id: str):
    """
    Get the latest weekly plan for a user.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: Latest weekly plan data or None
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('weekly_plans')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('created_at', desc=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        st.error(f"Error fetching latest weekly plan: {str(e)}")
        return None

def get_latest_scoring_results(user_id: str):
    """
    Get the latest scoring results for a user.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: Latest scoring results or None
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_scores')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('calculated_at', desc=True)\
            .limit(1)\
            .execute()
        
        if response.data:
            return response.data[0]
        return None
        
    except Exception as e:
        st.error(f"Error fetching latest scoring results: {str(e)}")
        return None


# ====================================================================
# TASK COMPLETION TRACKING FUNCTIONS
# ====================================================================

def save_task_completion(user_id: str, weekly_plan_id: str, task_id: str, task_title: str, task_type: str) -> bool:
    """
    Save a task completion to the database using user_actions table.
    
    Args:
        user_id (str): The user's UUID
        weekly_plan_id (str): The weekly plan UUID
        task_id (str): Unique task identifier (maps to suggestion_id)
        task_title (str): Task title/description (stored in notes)
        task_type (str): 'daily' or 'long_term' (stored in notes)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_actions').upsert({
            'user_id': user_id,
            'weekly_plan_id': weekly_plan_id,
            'suggestion_id': task_id,
            'status': 'completed',
            'notes': f"{task_title} ({task_type})"
        }).execute()
        
        return len(response.data) > 0
        
    except Exception as e:
        st.error(f"Error saving task completion: {str(e)}")
        return False

def get_task_completions(user_id: str, weekly_plan_id: str):
    """
    Get task completions for a specific weekly plan from user_actions table.
    
    Args:
        user_id (str): The user's UUID
        weekly_plan_id (str): The weekly plan UUID
        
    Returns:
        list: Task completion records with compatible format
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_actions')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('weekly_plan_id', weekly_plan_id)\
            .eq('status', 'completed')\
            .execute()
        
        # Convert user_actions format to expected task_completions format
        task_completions = []
        for action in response.data if response.data else []:
            task_completions.append({
                'task_id': action['suggestion_id'],
                'completed': action['status'] == 'completed',
                'user_id': action['user_id'],
                'weekly_plan_id': action['weekly_plan_id'],
                'created_at': action['created_at']
            })
        
        return task_completions
        
    except Exception as e:
        st.error(f"Error fetching task completions: {str(e)}")
        return []

def get_completed_tasks_count(user_id: str, weekly_plan_id: str) -> int:
    """
    Get the count of completed tasks for a weekly plan from user_actions table.
    
    Args:
        user_id (str): The user's UUID
        weekly_plan_id (str): The weekly plan UUID
        
    Returns:
        int: Number of completed tasks
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_actions')\
            .select('id', count='exact')\
            .eq('user_id', user_id)\
            .eq('weekly_plan_id', weekly_plan_id)\
            .eq('status', 'completed')\
            .execute()
        
        return response.count if response.count else 0
        
    except Exception as e:
        st.error(f"Error counting completed tasks: {str(e)}")
        return 0

def save_daily_tasks(user_id: str, weekly_plan_id: str, tasks: list) -> bool:
    """
    Save generated daily tasks to the database.
    
    Args:
        user_id (str): The user's UUID
        weekly_plan_id (str): The weekly plan UUID
        tasks (list): List of daily task objects
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('daily_tasks').insert({
            'user_id': user_id,
            'weekly_plan_id': weekly_plan_id,
            'task_data': tasks
        }).execute()
        
        return len(response.data) > 0
        
    except Exception as e:
        st.error(f"Error saving daily tasks: {str(e)}")
        return False

def get_daily_tasks(user_id: str, weekly_plan_id: str):
    """
    Get active daily tasks for a user and weekly plan.
    
    Args:
        user_id (str): The user's UUID
        weekly_plan_id (str): The weekly plan UUID
        
    Returns:
        list: Active daily tasks or empty list
    """
    try:
        supabase = get_supabase()
        
        # Get the most recent daily tasks for the weekly plan
        response = supabase.table('daily_tasks')\
            .select('task_data')\
            .eq('user_id', user_id)\
            .eq('weekly_plan_id', weekly_plan_id)\
            .order('generated_at', desc=True)\
            .limit(1)\
            .execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]['task_data']
        else:
            return []
            
    except Exception as e:
        st.error(f"Error fetching daily tasks: {str(e)}")
        return []


# ====================================================================
# PROFILER AGENT (AGENT 1) FUNCTIONS
# ====================================================================

def save_profiler_results(user_id: str, profiler_output: dict) -> bool:
    """
    Save profiler agent results to the database in the onboarding_final column.
    
    Args:
        user_id (str): The user's UUID
        profiler_output (dict): Agent 1 profiler results (enriched profile)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        supabase = get_supabase()
        
        # Update the onboarding_final column for existing user record
        response = supabase.table('user_profiles')\
            .update({'onboarding_final': profiler_output})\
            .eq('user_id', user_id)\
            .execute()
        
        # If no record was updated, try to insert a new one
        if not response.data:
            response = supabase.table('user_profiles').insert({
                'user_id': user_id,
                'onboarding_final': profiler_output
            }).execute()
        
        return True if response.data else False
        
    except Exception as e:
        st.error(f"Error saving profiler results: {str(e)}")
        return False

def get_profiler_results(user_id: str):
    """
    Get profiler agent results from the onboarding_final column.
    
    Args:
        user_id (str): The user's UUID
        
    Returns:
        dict: Profiler results or None if not found
    """
    try:
        supabase = get_supabase()
        
        response = supabase.table('user_profiles')\
            .select('onboarding_final')\
            .eq('user_id', user_id)\
            .execute()
        
        if response.data and len(response.data) > 0 and response.data[0]['onboarding_final']:
            return response.data[0]['onboarding_final']
        else:
            return None
            
    except Exception as e:
        st.error(f"Error fetching profiler results: {str(e)}")
        return None