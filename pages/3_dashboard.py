# pages/3_dashboard.py
import streamlit as st
import sys
import os
import pandas as pd
import json

# Add the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_model.auth import get_current_user, get_user_profile
from data_model.database import (
    get_user_progress_summary, 
    get_user_recent_actions, 
    get_user_onboarding_data,
    save_weekly_plan_results, 
    get_latest_weekly_plan, 
    get_latest_scoring_results,
    save_task_completion,
    get_task_completions,
    get_completed_tasks_count,
    save_daily_tasks,
    get_daily_tasks,
    get_supabase
)
from agent.crew import run_update_planning_workflow, run_daily_tasks_generation_workflow

# Page configuration
st.set_page_config(
    page_title="EcoAction AI - Dashboard",
    page_icon="📊",
    layout="wide"
)

# Simple styling function
def apply_simple_styles():
    """Apply comprehensive independent visual theme"""
    st.markdown("""
    <style>
    /* Import Poppins font family */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #ffffff 100%) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Block container styling */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif !important;
        color: #2C3E50 !important;
        font-weight: 600 !important;
    }
    
    /* Primary button styling */
    .stButton > button {
        background: linear-gradient(45deg, #6495ED, #4169E1) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(100, 149, 237, 0.3) !important;
        width: 100% !important;
        height: 3rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #4169E1, #1E90FF) !important;
        box-shadow: 0 6px 20px rgba(100, 149, 237, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0px) !important;
        box-shadow: 0 2px 10px rgba(100, 149, 237, 0.3) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Check authentication status
current_user = get_current_user()

if not current_user:
    # Apply simple styles for non-authenticated users
    apply_simple_styles()
    
    # Simple authentication message for dashboard
    st.markdown("""
    <div class="dashboard-welcome-card">
        <h1>📊 EcoAction AI Dashboard</h1>
        <p>Track your carbon footprint, get personalized recommendations, and see your environmental impact over time.</p>
        <p><strong>Please sign in to your account or create a new one to access your personal dashboard.</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🔐 Sign In", use_container_width=True):
                st.switch_page("pages/1_auth.py")
        
        with col_b:
            if st.button("🌟 Sign Up", use_container_width=True):
                st.switch_page("pages/1_auth.py")
    
    st.stop()

# Apply simple styles for authenticated users
apply_simple_styles()

# User is authenticated, continue with normal dashboard
user = current_user

if user:
    user_profile = get_user_profile(user.id)
    
    # Get display name
    if user_profile and user_profile.get('first_name'):
        display_name = user_profile.get('first_name', 'User')
    else:
        display_name = user.email.split('@')[0] if user.email else 'User'
    
    # Dashboard header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #6495ED 0%, #4169E1 50%, #1E90FF 100%); 
                border-radius: 20px; padding: 2rem; margin-bottom: 2rem; text-align: center; 
                color: white; box-shadow: 0 8px 32px rgba(100, 149, 237, 0.3);">
        <h1 style="color: white; margin-bottom: 0.5rem;">📊 Your EcoAction Dashboard</h1>
        <p style="color: #E6F3FF; font-size: 1.1rem; margin: 0;">
            Welcome back, {display_name}! Track your progress and discover new ways to reduce your carbon footprint.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check agent status first
    from data_model.database import check_agents_status, get_agent_results
    
    try:
        agents_status = check_agents_status(user.id)
        agent_results = get_agent_results(user.id)
    except Exception as e:
        st.error(f"Error checking agents status: {str(e)}")
        # Default to showing agents as not completed if there's an error
        agents_status = {'analyst_completed': False, 'planner_completed': False}
        agent_results = None
    
    # Check if user has scores in user_scores table to determine if they can access Agent 3
    try:
        supabase = get_supabase()
        scores_check = supabase.table('user_scores').select('id').eq('user_id', user.id).execute()
        has_scores = len(scores_check.data) > 0
    except Exception as e:
        st.error(f"Error checking user scores: {str(e)}")
        has_scores = False
    
    if not has_scores:
        # Show waiting message if no scores found
        st.markdown("""
        <div style="background: linear-gradient(135deg, #FFF9C4 0%, #FFEB3B 50%, #FFC107 100%); 
                    border-radius: 15px; padding: 2rem; margin: 2rem 0; text-align: center; 
                    border: 2px solid #FF9800; box-shadow: 0 4px 15px rgba(255, 152, 0, 0.2);">
            <h2 style="color: #E65100; margin-bottom: 1rem;">⏳ Processing Your Data</h2>
            <p style="color: #BF360C; font-size: 1.1rem; margin-bottom: 1rem;">
                We're currently analyzing your carbon footprint data. Please wait while our AI processes your information.
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; margin: 1.5rem 0;">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">
                        🔄
                    </div>
                    <div style="font-weight: 600; color: #E65100;">Analysis in Progress</div>
                    <div style="font-size: 0.9rem; color: #BF360C;">
                        Your challenges will be available soon
                    </div>
                </div>
            </div>
            <p style="color: #BF360C; font-size: 0.9rem; margin-top: 1rem;">
                Check back in a few moments for your personalized sustainability challenges!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Refresh button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Check Again", type="primary", use_container_width=True):
                st.rerun()
        
        st.stop()
    
    # Get agent results to display carbon data and weekly plans
    try:
        agent_results = get_agent_results(user.id)
    except Exception as e:
        st.error(f"Error getting agent results: {str(e)}")
        agent_results = None
    
    # Display carbon footprint analysis results if available
    if agent_results and agent_results.get('carbon_footprint_data'):
        carbon_data = agent_results['carbon_footprint_data']
        
        # Extract calculation and benchmark data
        calculation_data = carbon_data.get('calculation_data', {})
        benchmark_data = carbon_data.get('benchmark_data', {})
        
        # Carbon Footprint Analysis Header
        st.markdown("---")
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #45A049 100%); 
                    border-radius: 15px; padding: 2rem; margin: 2rem 0; text-align: center; 
                    color: white; box-shadow: 0 8px 32px rgba(76, 175, 80, 0.3);">
            <h2 style="color: white; margin-bottom: 0.5rem;">🌍 Your Carbon Footprint Analysis</h2>
            <p style="color: #E8F5E8; font-size: 1.1rem; margin: 0;">
                Powered by AI - Personalized insights based on your lifestyle
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Main metrics section from real data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_footprint_kg = calculation_data.get('total_carbon_footprint_kg', 0)
            total_footprint_tonnes = calculation_data.get('total_carbon_footprint_tonnes', total_footprint_kg/1000)
            st.metric(
                "Annual Carbon Footprint", 
                f"{total_footprint_tonnes:.2f} tonnes CO₂",
                help="Your estimated annual carbon emissions"
            )
        
        with col2:
            sustainability_score = calculation_data.get('sustainability_score', benchmark_data.get('sustainability_score', 0))
            score_category = calculation_data.get('score_category', benchmark_data.get('score_category', 'Unknown'))
            st.metric(
                "Sustainability Score", 
                f"{sustainability_score}/10",
                delta=score_category,
                help="Your overall sustainability rating"
            )
        
        with col3:
            regional_comparison = calculation_data.get('regional_comparison', benchmark_data.get('regional_comparison', {}))
            comparison_status = regional_comparison.get('comparison_status', 'unknown')
            percentage_diff = regional_comparison.get('percentage_difference', 0)
            delta_text = f"{percentage_diff:+.1f}%" if percentage_diff != 0 else "0%"
            st.metric(
                "vs. Regional Average", 
                comparison_status.title(),
                delta=delta_text,
                help="How you compare to others in your region"
            )
        
        with col4:
            top_categories = calculation_data.get('top_impact_categories', [])
            top_category = top_categories[0] if top_categories else 'N/A'
            st.metric(
                "Top Impact Area", 
                top_category,
                help="Your highest emission category"
            )
        
        # Category Breakdown Chart
        st.subheader("📊 Emissions by Category")
        category_breakdown = calculation_data.get('category_breakdown', {})
        
        if category_breakdown:
            # Create DataFrame for visualization
            categories = []
            emissions = []
            
            category_mapping = {
                'transportation_kg': 'Transportation',
                'diet_kg': 'Diet',
                'home_energy_kg': 'Home Energy',
                'shopping_kg': 'Shopping',
                'digital_footprint_kg': 'Digital Footprint',
                'other_kg': 'Other'
            }
            
            for key, value in category_breakdown.items():
                if value > 0:  # Only show non-zero categories
                    display_name = category_mapping.get(key, key.replace('_kg', '').replace('_', ' ').title())
                    categories.append(display_name)
                    emissions.append(value)
            
            if categories and emissions:
                df = pd.DataFrame({
                    'Category': categories,
                    'Annual Emissions (kg CO₂)': emissions
                })
                
                # Display as bar chart
                st.bar_chart(df.set_index('Category'))
                
                # Display as table with percentages
                df['Percentage'] = (df['Annual Emissions (kg CO₂)'] / df['Annual Emissions (kg CO₂)'].sum() * 100).round(1)
                df['Percentage'] = df['Percentage'].astype(str) + '%'
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Key Lever Validations
        st.subheader("🔧 Key Reduction Opportunities")
        key_lever_validations = calculation_data.get('key_lever_validations', [])
        
        if key_lever_validations:
            for i, validation in enumerate(key_lever_validations, 1):
                lever = validation.get('lever', '')
                validated = validation.get('validated', False)
                potential_reduction = validation.get('potential_reduction_kg', 0)
                validation_reason = validation.get('validation_reason', '')
                impact_category = validation.get('impact_category', '')
                
                status_icon = "✅" if validated else "❌"
                status_color = "#4CAF50" if validated else "#F44336"
                
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                            border-left: 5px solid {status_color}; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                    <h4 style="color: #2C3E50; margin-bottom: 0.5rem;">
                        {status_icon} {lever}
                    </h4>
                    <div style="color: #666; margin-bottom: 0.5rem;">
                        <strong>Impact Category:</strong> {impact_category} | 
                        <strong>Potential Reduction:</strong> {potential_reduction:.0f} kg CO₂/year
                    </div>
                    <div style="color: #666; font-style: italic;">
                        {validation_reason}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Psychographic Insights
        st.subheader("💭 Personalized Insights")
        psychographic_insights = calculation_data.get('psychographic_insights', [])
        
        if psychographic_insights:
            for i, insight in enumerate(psychographic_insights, 1):
                insight_text = insight.get('insight_text', '')
                related_motivation = insight.get('related_motivation', '')
                addresses_barrier = insight.get('addresses_barrier', '')
                actionable_step = insight.get('actionable_next_step', '')
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                            border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                            border: 1px solid #2196F3; box-shadow: 0 2px 10px rgba(33,150,243,0.1);">
                    <h4 style="color: #1976D2; margin-bottom: 1rem;">💡 Insight #{i}</h4>
                    <p style="color: #2C3E50; font-size: 1.1rem; margin-bottom: 1rem; line-height: 1.6;">
                        {insight_text}
                    </p>
                    <div style="background: rgba(255,255,255,0.7); border-radius: 8px; padding: 1rem; margin-top: 1rem;">
                        <div style="color: #666; margin-bottom: 0.5rem;">
                            <strong>🎯 Addresses your motivation:</strong> {related_motivation}
                        </div>
                        <div style="color: #666; margin-bottom: 0.5rem;">
                            <strong>🚧 Helps overcome barrier:</strong> {addresses_barrier}
                        </div>
                        <div style="color: #1976D2; font-weight: 600;">
                            <strong>🚀 Next step:</strong> {actionable_step}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Fun Comparison Facts
        fun_facts = calculation_data.get('fun_comparison_facts', [])
        if fun_facts:
            st.subheader("🎯 Fun Comparison Facts")
            for fact in fun_facts:
                st.info(f"💡 {fact}")
        
        # Priority Reduction Areas
        priority_areas = calculation_data.get('priority_reduction_areas', [])
        if priority_areas:
            st.subheader("🎯 Priority Focus Areas")
            cols = st.columns(len(priority_areas))
            for i, area in enumerate(priority_areas):
                with cols[i]:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%); 
                                border-radius: 12px; padding: 1rem; text-align: center; 
                                border: 2px solid #FF9800; margin: 0.5rem 0;">
                        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🎯</div>
                        <div style="color: #E65100; font-weight: 600;">{area}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Calculation Details
        with st.expander("📋 Calculation Details"):
            calculation_method = calculation_data.get('calculation_method', 'Standard emission factors applied')
            data_confidence = calculation_data.get('data_confidence', 'medium')
            
            confidence_color = {
                'high': '#4CAF50',
                'medium': '#FF9800', 
                'low': '#F44336'
            }.get(data_confidence, '#666')
            
            st.markdown(f"""
            **Calculation Method:** {calculation_method}
            
            **Data Confidence:** <span style="color: {confidence_color}; font-weight: 600;">{data_confidence.upper()}</span>
            
            **Regional Comparison:** Compared to {regional_comparison.get('user_location', 'regional')} average of {regional_comparison.get('local_average_kg', 0):.1f} kg CO₂/year
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Weekly action plan section
        st.subheader("🗓️ Your Personalized Weekly Plan")
        
        # Check if we have planner results
        planner_data = agent_results.get('weekly_plan_data')
        
        if planner_data:
            # Display weekly plan data
            week_focus = planner_data.get('week_focus', 'Sustainable Actions')
            st.info(f"**This Week's Focus:** {week_focus}")
            
            # Display motivation message
            if 'motivation' in planner_data:
                st.markdown(f"💪 **{planner_data['motivation']}**")
            elif 'motivation_message' in planner_data:
                st.markdown(f"💪 **{planner_data['motivation_message']}**")
            
            # Display weekly challenges
            weekly_challenges = planner_data.get('challenges', planner_data.get('weekly_challenges', []))
            
            # Get the actual weekly plan ID from the database
            latest_weekly_plan = get_latest_weekly_plan(user.id)
            if latest_weekly_plan:
                weekly_plan_id = latest_weekly_plan['id']
            else:
                # If no weekly plan found, we can't track completions
                weekly_plan_id = None
                st.warning("⚠️ Unable to find weekly plan in database. Task completion tracking may not work properly.")
            
            # Get completion status from database only if we have a valid weekly_plan_id
            if weekly_plan_id:
                task_completions = get_task_completions(user.id, weekly_plan_id)
                completion_map = {tc['task_id']: tc['completed'] for tc in task_completions}
            else:
                completion_map = {}
            
            # Update challenges with completion status from database
            for i, challenge in enumerate(weekly_challenges):
                task_id = f"challenge_{i+1}"
                challenge['completed'] = completion_map.get(task_id, challenge.get('completed', False))
            
            completed_count = sum(1 for challenge in weekly_challenges if challenge.get('completed', False))
            total_challenges = len(weekly_challenges)
            
            # Progress tracking display
            progress_percentage = (completed_count / total_challenges * 100) if total_challenges > 0 else 0
            
            # Progress header
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"### 📊 Progress: {completed_count}/{total_challenges} Challenges")
            with col2:
                st.metric("Daily Tasks", "🔓 Unlocked" if completed_count >= 3 else "🔒 Locked")
            with col3:
                st.metric("Completion", f"{progress_percentage:.0f}%")
            
            # Progress bar
            st.progress(progress_percentage / 100)
            
            if completed_count >= 3:
                st.success("🎉 Great progress! You've unlocked daily challenges!")
            elif completed_count >= 1:
                st.info(f"💪 Keep going! Complete {3 - completed_count} more challenges to unlock daily tasks.")
            else:
                st.info("🚀 Start completing challenges to unlock daily task rewards!")
            
            st.markdown("---")
            
            # Display daily tasks if unlocked (only if we have a valid weekly_plan_id)
            if weekly_plan_id:
                daily_tasks = get_daily_tasks(user.id, weekly_plan_id)
                if daily_tasks:
                    st.subheader("🔄 Your Daily Challenges")
                    st.info("🎁 Congratulations! You've unlocked these daily tasks by completing 3+ weekly challenges!")
                    
                    for i, task in enumerate(daily_tasks, 1):
                        task_completed = task.get('completed', False)
                        status_icon = "✅" if task_completed else "⏳"
                        
                        with st.expander(f"{status_icon} Daily Task {i}: {task.get('title', 'Daily Task')}"):
                            st.write(f"**Action:** {task.get('action', '')}")
                            st.write(f"**Why:** {task.get('why', '')}")
                            st.write(f"**Impact:** {task.get('impact', 'Builds sustainable habits')}")
                            
                            if not task_completed:
                                if st.button(f"✅ Complete Daily Task {i}", key=f"complete_daily_{i}"):
                                    # Save daily task completion
                                    task_id = f"daily_task_{i}"
                                    success = save_task_completion(
                                        user.id, 
                                        weekly_plan_id, 
                                        task_id, 
                                        task.get('title', f'Daily Task {i}'), 
                                        'daily'
                                    )
                                    
                                    if success:
                                        task['completed'] = True
                                        st.success(f"🎉 Daily task {i} completed!")
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        st.error("Failed to save completion. Please try again.")
                
                st.markdown("---")
            
            # Weekly Challenges Section
            st.subheader("🎯 Weekly Challenges")
            
            for i, challenge in enumerate(weekly_challenges, 1):
                challenge_completed = challenge.get('completed', False)
                task_type = challenge.get('task_type', 'weekly')
                status_icon = "✅" if challenge_completed else "⏳"
                type_badge = "🔄 Daily" if task_type == "daily" else "📅 Long-term"
                
                with st.expander(f"{status_icon} {type_badge} Challenge {i}: {challenge.get('title', 'Weekly Challenge')}"):
                    # Handle both old and new data structures
                    description = challenge.get('action', challenge.get('description', ''))
                    if description:
                        st.write(f"**Action:** {description}")
                    
                    # Why this matters
                    why_text = challenge.get('why', challenge.get('personalized_why', ''))
                    if why_text:
                        st.write(f"**Why this matters:** {why_text}")
                    
                    # Implementation steps
                    implementation_steps = challenge.get('steps', challenge.get('implementation_steps', []))
                    if implementation_steps:
                        st.write("**How to do it:**")
                        for step in implementation_steps:
                            st.write(f"• {step}")
                    
                    # Challenge metrics
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        difficulty = challenge.get('difficulty', challenge.get('difficulty_level', 'medium'))
                        st.metric("Difficulty", difficulty.title())
                    with col2:
                        co2_savings = challenge.get('co2_savings', challenge.get('estimated_co2_savings_kg', 0))
                        st.metric("CO₂ Savings", f"{co2_savings} kg")
                    with col3:
                        deadline = challenge.get('deadline', challenge.get('completion_deadline', 'This week'))
                        st.metric("Deadline", deadline)
                    with col4:
                        st.metric("Type", task_type.title())
                    
                    # Complete button (only if not completed)
                    if not challenge_completed:
                        if st.button(f"✅ Complete Challenge {i}", key=f"complete_challenge_{i}"):
                            # Save task completion to database only if we have a valid weekly_plan_id
                            success = False
                            if weekly_plan_id:
                                task_id = f"challenge_{i}"
                                task_title = challenge.get('title', f'Weekly Challenge {i}')
                                task_type = challenge.get('task_type', 'weekly')
                                
                                success = save_task_completion(
                                    user.id, 
                                    weekly_plan_id, 
                                    task_id, 
                                    task_title, 
                                    task_type
                                )
                            else:
                                st.error("❌ Cannot save completion: No valid weekly plan found in database.")
                            
                            if success:
                                # Update in-memory status
                                challenge['completed'] = True
                                st.success(f"🎉 Great job! Challenge {i} completed!")
                                
                                # Check if this triggers daily tasks generation
                                completed_count = get_completed_tasks_count(user.id, weekly_plan_id)
                                if completed_count >= 3:
                                    if not get_daily_tasks(user.id, weekly_plan_id):
                                        st.info("🎉 You've unlocked daily challenges! Generating new daily tasks...")
                                        
                                        # Generate daily tasks using Agent 3
                                        try:
                                            from data_model.database import get_latest_scoring_results, get_user_onboarding_data
                                            scoring_results = get_latest_scoring_results(user.id)
                                            user_onboarding_data = get_user_onboarding_data(user.id)
                                            
                                            daily_results = run_daily_tasks_generation_workflow(
                                                user_onboarding_data, 
                                                scoring_results, 
                                                planner_data, 
                                                completed_count
                                            )
                                            
                                            if daily_results and hasattr(daily_results, 'raw'):
                                                daily_tasks_data = json.loads(daily_results.raw)
                                                daily_tasks = daily_tasks_data.get('daily_tasks', [])
                                                
                                                # Save daily tasks to database
                                                save_daily_tasks(user.id, weekly_plan_id, daily_tasks)
                                                st.success("🎁 New daily challenges generated!")
                                        except Exception as e:
                                            st.error(f"Error generating daily tasks: {str(e)}")
                                
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("Failed to save task completion. Please try again.")
                    else:
                        st.success("✅ Challenge completed!")
        
        else:
            # No planner results - show Generate Challenges button
            st.info("🤖 Ready to generate your personalized weekly sustainability challenges!")
            st.markdown("""
            Click the button below to create your personalized weekly challenges 
            based on your carbon footprint analysis.
            """)
            
            # Generate Challenges button
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎯 Generate Challenges", type="primary", use_container_width=True):
                    with st.spinner("🤖 Agent 3 is creating your personalized weekly challenges..."):
                        from data_model.database import get_user_onboarding_data, save_agent_results, create_agent_session, update_agent_session
                        from agent.agents import create_planner_agent
                        from agent.tasks import create_weekly_planning_task
                        from crewai import Crew, Process
                        
                        try:
                            # Get user data
                            user_onboarding_data = get_user_onboarding_data(user.id)
                            
                            # Create agent session for planner
                            agent_session_id = create_agent_session(user.id, "weekly_planning", "Generate challenges workflow execution from dashboard")
                            
                            # Create planner agent and task
                            planner_agent = create_planner_agent()
                            planning_task = create_weekly_planning_task(
                                planner_agent, 
                                user_onboarding_data, 
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
                            
                            planner_results = planner_crew.kickoff()
                            
                            if planner_results and hasattr(planner_results, 'tasks_output') and planner_results.tasks_output:
                                try:
                                    raw_output = planner_results.tasks_output[0].raw
                                    
                                    # Try to parse JSON with fallback handling
                                    try:
                                        weekly_plan_data = json.loads(raw_output)
                                    except json.JSONDecodeError:
                                        # Try to extract JSON from raw output
                                        if "{" in raw_output:
                                            start_idx = raw_output.find("{")
                                            # Find matching closing brace
                                            brace_count = 0
                                            end_idx = -1
                                            for i, char in enumerate(raw_output[start_idx:], start_idx):
                                                if char == '{':
                                                    brace_count += 1
                                                elif char == '}':
                                                    brace_count -= 1
                                                    if brace_count == 0:
                                                        end_idx = i + 1
                                                        break
                                            
                                            if end_idx > start_idx:
                                                json_content = raw_output[start_idx:end_idx]
                                                weekly_plan_data = json.loads(json_content)
                                            else:
                                                raise json.JSONDecodeError("Could not find complete JSON", raw_output, 0)
                                        else:
                                            raise json.JSONDecodeError("No JSON found", raw_output, 0)
                                    
                                    # Save the results
                                    save_agent_results(user.id, 'planner', weekly_plan_data, agent_session_id)
                                    save_weekly_plan_results(user.id, agent_session_id, weekly_plan_data)
                                    update_agent_session(agent_session_id, "completed", weekly_plan_data)
                                    
                                    st.success("✅ Weekly challenges generated successfully!")
                                    st.balloons()
                                    st.rerun()
                                    
                                except Exception as e:
                                    st.error(f"Error processing planner results: {str(e)}")
                                    update_agent_session(agent_session_id, "failed", {"error": str(e)})
                            else:
                                st.error("❌ Agent 3 failed to generate challenges")
                                update_agent_session(agent_session_id, "failed", {"error": "No results generated"})
                                
                        except Exception as e:
                            st.error(f"Error running Agent 3: {str(e)}")
    
    else:
        # No agent results available
        st.warning("No carbon footprint analysis found. Please complete your onboarding first.")
        if st.button("🌱 Go to Onboarding", use_container_width=True):
            st.switch_page("pages/2_onboarding.py")

    # Agent 3 Update Section - Available to all users with completed analysis
    if agent_results and agent_results.get('carbon_footprint_data'):
        st.markdown("---")
        st.subheader("📝 Share Your Progress with Agent 3")
        st.info("💬 Tell us about your recent sustainability actions or challenges. Agent 3 will update your weekly plan based on your feedback!")
        
        # User update text input
        user_update = st.text_area(
            "Share your sustainability progress, challenges, or changes:",
            placeholder="Example: I've been biking to work 3 days this week, but struggled with reducing meat consumption. Also started composting at home...",
            height=100,
            help="Share any updates about your sustainability journey. Agent 3 will analyze this and update your weekly plan accordingly."
        )
        
        if st.button("🤖 Update My Plan with Agent 3", type="primary", use_container_width=True):
            if user_update.strip():
                with st.spinner("🤖 Agent 3 is analyzing your update and creating new recommendations..."):
                    try:
                        # Get current data
                        carbon_data = agent_results['carbon_footprint_data']
                        calculation_data = carbon_data.get('calculation_data', {})
                        benchmark_data = carbon_data.get('benchmark_data', {})
                        
                        from data_model.database import get_user_onboarding_data, save_agent_results, create_agent_session, update_agent_session
                        user_onboarding_data = get_user_onboarding_data(user.id)
                        
                        # Run Agent 3 update workflow
                        update_results = run_update_planning_workflow(
                            user_onboarding_data,
                            calculation_data,
                            benchmark_data,
                            user_update
                        )
                        
                        if update_results and hasattr(update_results, 'tasks_output') and update_results.tasks_output:
                            try:
                                raw_output = update_results.tasks_output[0].raw
                                
                                # Parse the updated plan
                                if raw_output.strip().startswith('{'):
                                    updated_plan_data = json.loads(raw_output)
                                else:
                                    # Extract JSON from text
                                    start = raw_output.find('{')
                                    end = raw_output.rfind('}') + 1
                                    if start != -1 and end > start:
                                        updated_plan_data = json.loads(raw_output[start:end])
                                    else:
                                        raise json.JSONDecodeError("No valid JSON found", raw_output, 0)
                                
                                # Create new agent session for the update
                                agent_session_id = create_agent_session(user.id, "weekly_planning", f"Plan update based on user feedback: {user_update[:50]}...")
                                
                                # Save updated results
                                save_agent_results(user.id, 'planner', updated_plan_data, agent_session_id)
                                update_agent_session(agent_session_id, "completed", updated_plan_data)
                                
                                # Also save to weekly_plans table
                                save_weekly_plan_results(user.id, agent_session_id, updated_plan_data)
                                
                                st.success("✅ Your plan has been updated successfully based on your feedback!")
                                st.balloons()
                                st.rerun()
                                
                            except json.JSONDecodeError as e:
                                st.error(f"❌ Failed to parse Agent 3 response: {str(e)}")
                                st.text_area("Raw Agent 3 output:", raw_output, height=200)
                        else:
                            st.error("❌ Agent 3 failed to generate updated plan")
                            
                    except Exception as e:
                        st.error(f"❌ Error running Agent 3 update: {str(e)}")
            else:
                st.warning("⚠️ Please enter some feedback before updating your plan.")
    
    else:
        # No carbon analysis results available yet - show waiting message
        st.info("📊 Your carbon footprint analysis results will appear here once available.")
        
        # Show Agent 3 activation for generating initial challenges
        st.markdown("---")
        st.subheader("🎯 Generate Your First Challenges")
        st.info("🤖 Ready to create your personalized weekly sustainability challenges!")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Generate Challenges", type="primary", use_container_width=True):
                with st.spinner("🤖 Agent 3 is creating your personalized weekly challenges..."):
                    from data_model.database import get_user_onboarding_data, save_agent_results, create_agent_session, update_agent_session
                    from agent.agents import create_planner_agent
                    from agent.tasks import create_weekly_planning_task
                    from crewai import Crew, Process
                    
                    try:
                        # Get user data
                        user_onboarding_data = get_user_onboarding_data(user.id)
                        
                        if not user_onboarding_data:
                            st.error("❌ No onboarding data found. Please complete onboarding first.")
                            if st.button("🌱 Go to Onboarding"):
                                st.switch_page("pages/2_onboarding.py")
                            st.stop()
                        
                        # Create agent session for planner
                        agent_session_id = create_agent_session(user.id, "weekly_planning", "Initial challenges generation from dashboard")
                        
                        # Create planner agent and task with basic data
                        planner_agent = create_planner_agent()
                        planning_task = create_weekly_planning_task(
                            planner_agent, 
                            user_onboarding_data, 
                            {}, # Empty calculation data
                            {}  # Empty benchmark data
                        )
                        
                        # Create and run planner crew
                        planner_crew = Crew(
                            agents=[planner_agent],
                            tasks=[planning_task],
                            process=Process.sequential,
                            verbose=False,
                            memory=False
                        )
                        
                        planner_results = planner_crew.kickoff()
                        
                        if planner_results and hasattr(planner_results, 'tasks_output') and planner_results.tasks_output:
                            try:
                                raw_output = planner_results.tasks_output[0].raw
                                
                                # Try to parse JSON
                                try:
                                    weekly_plan_data = json.loads(raw_output)
                                except json.JSONDecodeError:
                                    # Try to extract JSON from raw output
                                    if "{" in raw_output:
                                        start_idx = raw_output.find("{")
                                        end_idx = raw_output.rfind("}") + 1
                                        if start_idx != -1 and end_idx > start_idx:
                                            json_content = raw_output[start_idx:end_idx]
                                            weekly_plan_data = json.loads(json_content)
                                        else:
                                            raise json.JSONDecodeError("Could not find complete JSON", raw_output, 0)
                                    else:
                                        raise json.JSONDecodeError("No JSON found", raw_output, 0)
                                
                                # Save the results
                                save_agent_results(user.id, 'planner', weekly_plan_data, agent_session_id)
                                save_weekly_plan_results(user.id, agent_session_id, weekly_plan_data)
                                update_agent_session(agent_session_id, "completed", weekly_plan_data)
                                
                                st.success("✅ Weekly challenges generated successfully!")
                                st.balloons()
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"Error processing results: {str(e)}")
                                update_agent_session(agent_session_id, "failed", {"error": str(e)})
                        else:
                            st.error("❌ Agent 3 failed to generate challenges")
                            update_agent_session(agent_session_id, "failed", {"error": "No results generated"})
                            
                    except Exception as e:
                        st.error(f"Error running Agent 3: {str(e)}")
