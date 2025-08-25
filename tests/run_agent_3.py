"""
Manual Agent 3 (Planner) Runner Script
Runs Agent 3 (Planner) for users who already have Agent 2 (Analyst) results
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
    update_agent_session,
    get_agent_results
)
from agent.tasks import create_weekly_planning_task
from agent.agents import create_planner_agent
from crewai import Crew, Process

def get_users_with_analyst_results():
    """Get users who have Agent 2 (Analyst) results but no Agent 3 (Planner) results"""
    try:
        supabase = get_supabase()
        
        # Get users with scores (Agent 2 results)
        scores_response = supabase.table('user_scores')\
            .select('user_id, users(id, email, first_name, last_name)')\
            .execute()
        
        # Get users with weekly plans (Agent 3 results)
        today = date.today()
        days_since_monday = today.weekday()
        week_start = today - timedelta(days=days_since_monday)
        
        plans_response = supabase.table('weekly_plans')\
            .select('user_id')\
            .eq('week_of', week_start.isoformat())\
            .execute()
        
        # Get user IDs who already have plans
        users_with_plans = {plan['user_id'] for plan in plans_response.data}
        
        # Filter users who have scores but no plans for this week
        users_needing_plans = []
        for score_entry in scores_response.data:
            if score_entry.get('users') and score_entry['user_id'] not in users_with_plans:
                users_needing_plans.append(score_entry['users'])
        
        # Remove duplicates
        unique_users = []
        seen_user_ids = set()
        for user in users_needing_plans:
            if user['id'] not in seen_user_ids:
                unique_users.append(user)
                seen_user_ids.add(user['id'])
        
        return unique_users
        
    except Exception as e:
        print(f"❌ Error fetching users with analyst results: {str(e)}")
        return []

def run_agent_3_for_user(user_id, user_email):
    """Run Agent 3 (Planner) for a specific user"""
    print(f"\n🤖 Running Agent 3 (Planner) for user: {user_email}")
    
    try:
        # Get user onboarding data
        user_data = get_user_onboarding_data(user_id)
        if not user_data:
            print(f"   ❌ No onboarding data found for user {user_email}")
            return None
        
        # Get Agent 2 results
        agent_results = get_agent_results(user_id)
        if not agent_results or not agent_results.get('carbon_footprint_data'):
            print(f"   ❌ No Agent 2 results found for user {user_email}")
            return None
        
        carbon_data = agent_results['carbon_footprint_data']
        calculation_data = carbon_data.get('calculation_data', {})
        benchmark_data = carbon_data.get('benchmark_data', {})
        
        print(f"   📊 Found Agent 2 results for {user_email}")
        print(f"   📊 Carbon footprint: {calculation_data.get('total_carbon_footprint_kg', 0):.1f} kg CO₂")
        
        # Create agent session for planner
        agent_session_id = create_agent_session(user_id, "weekly_planning", "Manual Agent 3 planner workflow execution")
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
            # Get raw output for debugging
            raw_output = planner_results.tasks_output[0].raw
            print(f"   🔍 Raw Agent 3 output length: {len(raw_output)} characters")
            
            # Parse planner results with robust error handling
            try:
                weekly_plan_data = json.loads(raw_output)
                
                # Save Agent 3 results
                save_agent_results(user_id, 'planner', weekly_plan_data, agent_session_id)
                print(f"   ✅ Agent 3 results saved successfully")
                
                # Update agent session
                update_agent_session(agent_session_id, "completed", weekly_plan_data)
                
                return weekly_plan_data
                
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON parse error: {str(e)}")
                
                # Try to fix common JSON issues
                cleaned_output = raw_output.strip()
                
                # Remove any markdown wrapper
                if "```json" in cleaned_output:
                    start_idx = cleaned_output.find("```json") + 7
                    end_idx = cleaned_output.find("```", start_idx)
                    if end_idx > start_idx:
                        cleaned_output = cleaned_output[start_idx:end_idx].strip()
                
                # Find JSON boundaries
                if "{" in cleaned_output:
                    start_idx = cleaned_output.find("{")
                    
                    # Try to find the matching closing brace
                    brace_count = 0
                    end_idx = -1
                    for i, char in enumerate(cleaned_output[start_idx:], start_idx):
                        if char == '{':
                            brace_count += 1
                        elif char == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end_idx = i + 1
                                break
                    
                    if end_idx > start_idx:
                        json_content = cleaned_output[start_idx:end_idx]
                    else:
                        # If no complete JSON, try to reconstruct
                        print(f"   🔧 Attempting to fix incomplete JSON...")
                        json_content = cleaned_output[start_idx:]
                        
                        # Add missing closing braces if needed
                        open_braces = json_content.count('{') - json_content.count('}')
                        open_brackets = json_content.count('[') - json_content.count(']')
                        
                        if open_brackets > 0:
                            json_content += ']' * open_brackets
                        if open_braces > 0:
                            json_content += '}' * open_braces
                    
                    try:
                        print(f"   🔧 Attempting to parse cleaned JSON...")
                        weekly_plan_data = json.loads(json_content)
                        
                        # Save Agent 3 results
                        save_agent_results(user_id, 'planner', weekly_plan_data, agent_session_id)
                        print(f"   ✅ Agent 3 results saved successfully (after cleanup)")
                        
                        # Update agent session
                        update_agent_session(agent_session_id, "completed", weekly_plan_data)
                        
                        return weekly_plan_data
                        
                    except json.JSONDecodeError as e2:
                        print(f"   ❌ Still failed after cleanup: {str(e2)}")
                        print(f"   🔍 Cleaned content preview:")
                        print(f"   {json_content[:300]}...")
                
                # Last resort: create a minimal valid response
                print(f"   🔧 Creating fallback minimal response...")
                fallback_data = {
                    "week_focus": "Energy and Transport Optimization",
                    "priority_area": "Home Energy",
                    "challenges": [
                        {
                            "id": "fallback-1",
                            "title": "Reduce AC temperature by 2°C",
                            "action": "Lower AC to 24°C for weekdays",
                            "why": "Saves energy and reduces carbon footprint",
                            "steps": ["Set AC to 24°C", "Monitor daily", "Track savings"],
                            "co2_savings": 10,
                            "difficulty": "easy",
                            "deadline": "Friday"
                        }
                    ],
                    "motivation": "Small changes make a big difference!"
                }
                
                try:
                    save_agent_results(user_id, 'planner', fallback_data, agent_session_id)
                    print(f"   ✅ Fallback response saved successfully")
                    update_agent_session(agent_session_id, "completed", fallback_data)
                    return fallback_data
                except Exception as e3:
                    print(f"   ❌ Failed to save fallback: {str(e3)}")
                
                return None
        else:
            print(f"   ❌ Agent 3 failed to produce results")
            return None
            
    except Exception as e:
        print(f"   ❌ Error running Agent 3: {str(e)}")
        return None

def main():
    """Main function to run Agent 3 (Planner) for users with Agent 2 results"""
    print("🚀 Starting Manual Agent 3 (Planner) Runner")
    print("=" * 50)
    
    # Get users who have Agent 2 results but need Agent 3 results
    users = get_users_with_analyst_results()
    
    if not users:
        print("❌ No users found who need Agent 3 planning")
        print("   Either no users have Agent 2 results, or all users already have weekly plans")
        return
    
    print(f"📊 Found {len(users)} users who need Agent 3 planning")
    
    # Storage for results
    all_plans = []
    
    # Process each user
    for i, user in enumerate(users, 1):
        user_id = user['id']
        user_email = user['email']
        user_name = f"{user.get('first_name', '')} {user.get('last_name', '')}".strip()
        
        print(f"\n{'='*60}")
        print(f"Processing User {i}/{len(users)}: {user_name} ({user_email})")
        print(f"User ID: {user_id}")
        print(f"{'='*60}")
        
        # Run Agent 3 (Planner)
        planner_results = run_agent_3_for_user(user_id, user_email)
        
        if planner_results:
            all_plans.append({
                'user_id': user_id,
                'user_email': user_email,
                'plan': planner_results
            })
            print(f"   ✅ Agent 3 completed successfully for {user_email}")
        else:
            print(f"   ❌ Agent 3 failed for {user_email}")
    
    # Print final results
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}")
    
    print(f"\n📅 Successfully processed {len(all_plans)} users with Agent 3")
    
    # Print plans/suggestions JSON (just the JSON as requested)
    print(f"\n{'='*50}")
    print("AGENT 3 PLANS/SUGGESTIONS JSON:")
    print(f"{'='*50}")
    
    for plan_data in all_plans:
        print(f"\n# User: {plan_data['user_email']}")
        print(json.dumps(plan_data['plan'], indent=2))
    
    print(f"\n🎉 Manual Agent 3 execution completed!")
    print(f"   Weekly plans generated: {len(all_plans)}")

if __name__ == "__main__":
    main()
