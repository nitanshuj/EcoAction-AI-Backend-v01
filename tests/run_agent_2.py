"""
Manual Agent Runner Script
Runs Agent 2 (Analyst) and Agent 3 (Planner) for all users in the database
"""

import sys
import os
import json
from datetime import date, timedelta

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_model.database import (
    get_supabase, 
    get_user_onboarding_data, 
    save_agent_results,
    create_agent_session,
    update_agent_session
)
from agent.crew import run_analyst_workflow
from agent.tasks import create_weekly_planning_task
from agent.agents import create_planner_agent
from crewai import Crew, Process

def get_all_users():
    """Get all users from the database"""
    try:
        supabase = get_supabase()
        response = supabase.table('users').select('id, email, first_name, last_name').execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching users: {str(e)}")
        return []

def get_users_with_profiles():
    """Get users who have completed onboarding (have user_profiles)"""
    try:
        supabase = get_supabase()
        response = supabase.table('user_profiles')\
            .select('user_id, users(id, email, first_name, last_name)')\
            .execute()
        
        users_with_profiles = []
        for profile in response.data:
            if profile.get('users'):
                users_with_profiles.append(profile['users'])
        
        return users_with_profiles
    except Exception as e:
        print(f"❌ Error fetching users with profiles: {str(e)}")
        return []

def run_agent_2_for_user(user_id, user_email):
    """Run Agent 2 (Analyst) for a specific user"""
    print(f"\n🤖 Running Agent 2 (Analyst) for user: {user_email}")
    
    try:
        # Get user onboarding data
        user_data = get_user_onboarding_data(user_id)
        if not user_data:
            print(f"   ❌ No onboarding data found for user {user_email}")
            return None
        
        print(f"   📊 Found onboarding data for {user_email}")
        
        # Create agent session
        agent_session_id = create_agent_session(user_id, "scoring", "Manual agent workflow execution")
        print(f"   📝 Created agent session: {agent_session_id}")
        
        # Run Agent 2 (Analyst) workflow
        print(f"   🔄 Running analyst workflow...")
        analyst_results = run_analyst_workflow(user_data)
        
        if analyst_results and hasattr(analyst_results, 'tasks_output') and analyst_results.tasks_output:
            # Parse analyst results
            try:
                # Extract calculation task result (first task)
                calculation_data = json.loads(analyst_results.tasks_output[0].raw)
                # Extract benchmarking task result (second task)
                benchmark_data = json.loads(analyst_results.tasks_output[1].raw)
                
                # Combine analyst results
                combined_analyst_results = {
                    'calculation_data': calculation_data,
                    'benchmark_data': benchmark_data
                }
                
                # Save Agent 2 results
                save_agent_results(user_id, 'analyst', combined_analyst_results, agent_session_id)
                print(f"   ✅ Agent 2 results saved successfully")
                
                # Update agent session
                update_agent_session(agent_session_id, "completed", combined_analyst_results)
                
                return combined_analyst_results
                
            except json.JSONDecodeError as e:
                print(f"   ❌ Error parsing Agent 2 results: {str(e)}")
                return None
        else:
            print(f"   ❌ Agent 2 failed to produce results")
            return None
            
    except Exception as e:
        print(f"   ❌ Error running Agent 2: {str(e)}")
        return None

def run_agent_3_for_user(user_id, user_email, analyst_results):
    """Run Agent 3 (Planner) for a specific user"""
    print(f"\n🤖 Running Agent 3 (Planner) for user: {user_email}")
    
    try:
        # Get user onboarding data
        user_data = get_user_onboarding_data(user_id)
        if not user_data:
            print(f"   ❌ No onboarding data found for user {user_email}")
            return None
        
        # Extract data from analyst results
        calculation_data = analyst_results.get('calculation_data', {})
        benchmark_data = analyst_results.get('benchmark_data', {})
        
        print(f"   📊 Using analyst results for planning...")
        
        # Create agent session for planner
        agent_session_id = create_agent_session(user_id, "weekly_planning", "Manual planner workflow execution")
        print(f"   📝 Created planner session: {agent_session_id}")
        
        # Create planner agent and task
        print(f"   🔄 Creating weekly planning task...")
        planner_agent = create_planner_agent()
        planning_task = create_weekly_planning_task(
            planner_agent, 
            user_data, 
            calculation_data, 
            benchmark_data
        )
        
        # Create and run planner crew
        planner_crew = Crew(
            agents=[planner_agent],
            tasks=[planning_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        print(f"   🔄 Running planner workflow...")
        planner_results = planner_crew.kickoff()
        
        if planner_results and hasattr(planner_results, 'tasks_output') and planner_results.tasks_output:
            # Parse planner results
            try:
                weekly_plan_data = json.loads(planner_results.tasks_output[0].raw)
                
                # Save Agent 3 results
                save_agent_results(user_id, 'planner', weekly_plan_data, agent_session_id)
                print(f"   ✅ Agent 3 results saved successfully")
                
                # Update agent session
                update_agent_session(agent_session_id, "completed", weekly_plan_data)
                
                return weekly_plan_data
                
            except json.JSONDecodeError as e:
                print(f"   ❌ Error parsing Agent 3 results: {str(e)}")
                return None
        else:
            print(f"   ❌ Agent 3 failed to produce results")
            return None
            
    except Exception as e:
        print(f"   ❌ Error running Agent 3: {str(e)}")
        return None

def main():
    """Main function to run Agent 2 (Analyst) for all users"""
    print("🚀 Starting Manual Agent 2 (Analyst) Runner")
    print("=" * 50)
    
    # Get all users with profiles (completed onboarding)
    users = get_users_with_profiles()
    
    if not users:
        print("❌ No users with profiles found")
        return
    
    print(f"📊 Found {len(users)} users with completed onboarding")
    
    # Storage for results
    all_scores = []
    
    # Process each user
    for i, user in enumerate(users, 1):
        user_id = user['id']
        user_email = user['email']
        user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        
        print(f"\n{'='*60}")
        print(f"Processing User {i}/{len(users)}: {user_name} ({user_email})")
        print(f"User ID: {user_id}")
        print(f"{'='*60}")
        
        # Run Agent 2 (Analyst) only
        analyst_results = run_agent_2_for_user(user_id, user_email)
        
        if analyst_results:
            all_scores.append({
                'user_id': user_id,
                'user_email': user_email,
                'scores': analyst_results
            })
            print(f"   ✅ Agent 2 completed successfully for {user_email}")
        else:
            print(f"   ❌ Agent 2 failed for {user_email}")
    
    # Print final results
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}")
    
    print(f"\n📊 Successfully processed {len(all_scores)} users with Agent 2")
    
    # Print scores JSON (just the JSON as requested)
    print(f"\n{'='*50}")
    print("AGENT 2 SCORES JSON:")
    print(f"{'='*50}")
    
    for score_data in all_scores:
        print(f"\n# User: {score_data['user_email']}")
        print(json.dumps(score_data['scores'], indent=2))
    
    print(f"\n🎉 Manual Agent 2 execution completed!")
    print(f"   Scores generated: {len(all_scores)}")
    print("   Agent 3 (Planner) can be triggered manually from the dashboard")

if __name__ == "__main__":
    main()
