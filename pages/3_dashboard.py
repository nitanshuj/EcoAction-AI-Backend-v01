# pages/3_dashboard.py

import sys
import streamlit as st
# import sys
import os
import pandas as pd
import altair as alt

# Add the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.utils import parse_text_to_json
from agent.utils import parse_agent3_text_output
from data_model.auth import get_current_user, get_user_profile
from data_model.database import check_agents_status, get_agent_results
from data_model.database import (
    get_supabase,
    # save_user_profile,
    # save_challenge_completion,
    # get_user_completed_challenges,
    # get_user_score,
    check_agents_status,
    get_agent_results,
    # save_weekly_plan,
    # get_weekly_plan,
    # get_user_weekly_plans,
    get_latest_weekly_plan,
    save_task_completion,
    get_task_completions,
    get_completed_tasks_count,
    save_weekly_plan_results,
    debug_weekly_plans,
    debug_user_actions,
    get_current_week_feedback, 
    get_user_feedback_history, 
    save_feedback_and_process,
    # check_user_engagement,
)
from agent.crew import (
    run_planner_workflow,
    run_feedback_aware_planning_workflow,
    run_update_planning_workflow,
)# Page configuration
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
    
    # Dashboard header with sidebar for quick actions
    with st.sidebar:
        st.markdown("### � Quick Actions")
        
        # New Plan button
        if st.button("🔄 Original Plan", type="secondary", help="Generate fresh weekly challenges", use_container_width=True):
            with st.spinner("🤖 Creating fresh plan..."):
                try:
                    # Run the basic planner workflow to generate a new plan
                    new_plan_results = run_planner_workflow(user.id)
                    
                    if new_plan_results:
                        # Parse and save the new plan
                        from agent.utils import parse_text_to_json
                        
                        new_plan = parse_text_to_json(new_plan_results)
                        
                        if new_plan:
                            # Save the new plan
                            from data_model.database import (
                                save_weekly_plan_results, 
                                create_agent_session, 
                                save_agent_results, 
                                update_agent_session)
                            
                            # Create session and save results
                            session_id = create_agent_session(user.id, "fresh_planning", "Fresh weekly plan generation")
                            save_agent_results(user.id, 'planner', new_plan, session_id)
                            update_agent_session(session_id, "completed", new_plan)
                            save_weekly_plan_results(user.id, session_id, new_plan)
                            
                            st.success("✅ Fresh plan generated!")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Failed to parse AI response")
                    else:
                        st.error("Failed to generate new plan")
                        
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        
        # User info and logout
        # st.markdown(f"**Welcome, {display_name}!**")
        # st.markdown(f"📧 {user.email}")
        
        # Logout button
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            # Clear the session state for authentication
            if 'authenticated' in st.session_state:
                del st.session_state['authenticated']
            if 'user' in st.session_state:
                del st.session_state['user']
            
            st.success("✅ Successfully logged out!")
            st.rerun()
    
    # Dashboard header (now full width)
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
        <div style="background: linear-gradient(135deg, #BFEE90 30%, #90EEBF 70%); 
                    border-radius: 15px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; 
                    color: white; box-shadow: 0 6px 24px rgba(76, 175, 80, 0.3);">
            <h3 style="color: white; margin-bottom: 0.5rem; font-size: 1.75rem;">🌍 Your Carbon Footprint Analysis</h3>
            <p style="color: #3D8EEB; font-size: 1rem; margin: 0;">
                Powered by AI – Personalized insights based on your lifestyle
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
                # Sort the DataFrame for an ordered chart (optional but good practice)
                df_sorted = df.sort_values(by='Annual Emissions (kg CO₂)', 
                                           ascending=False)

                # --- Create the chart using Altair ---
                chart = alt.Chart(df_sorted).mark_bar().encode(
                    x=alt.X('Category', title='Emission Category', sort=None, axis=alt.Axis(labelAngle=45)), # Custom X-axis title
                    y=alt.Y('Annual Emissions (kg CO₂)', title='Annual Emissions (kg CO₂)') # Custom Y-axis title
                )
                
                # Display the Altair chart in Streamlit
                st.altair_chart(chart, use_container_width=True)

            # --- Display the table (can still use the original DataFrame logic) ---
                df['Percentage'] = (df['Annual Emissions (kg CO₂)'] / df['Annual Emissions (kg CO₂)'].sum() * 100).round(1)
                df['Percentage'] = df['Percentage'].astype(str) + '%'
                st.dataframe(df.sort_values(by='Annual Emissions (kg CO₂)', ascending=False), 
                             use_container_width=True, 
                             hide_index=True)
        
        # Fun Comparison Facts - Move up and make bigger
        fun_facts = calculation_data.get('fun_comparison_facts', [])
        if fun_facts:
            st.subheader("🎯 Fun Comparison Facts")
            for fact in fun_facts:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #E8F5E8 0%, #C8E6C9 100%); 
                            border-radius: 15px; padding: 1.5rem; margin: 1rem 0; 
                            border-left: 5px solid #4CAF50; box-shadow: 0 4px 15px rgba(76, 175, 80, 0.2);">
                    <p style="color: #2E7D32; font-size: 1.2rem; margin: 0; font-weight: 500;">
                        💡 {fact}
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        # Psychographic Insights - Side by side
        st.subheader("💭 Personalized Insights")
        psychographic_insights = calculation_data.get('psychographic_insights', [])
        
        if psychographic_insights:
            # Display insights in 2 columns if there are at least 2
            if len(psychographic_insights) >= 2:
                col1, col2 = st.columns(2)
                
                for i, insight in enumerate(psychographic_insights[:2]):  # Show max 2 insights
                    insight_text = insight.get('insight_text', '')
                    related_motivation = insight.get('related_motivation', '')
                    addresses_barrier = insight.get('addresses_barrier', '')
                    actionable_step = insight.get('actionable_next_step', '')
                    
                    col = col1 if i == 0 else col2
                    
                    with col:
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%); 
                                    border-radius: 12px; padding: 1.2rem; margin: 0.5rem 0; 
                                    border: 1px solid #2196F3; box-shadow: 0 2px 10px rgba(33,150,243,0.1); height: 220px;">
                            <h5 style="color: #1976D2; margin-bottom: 0.8rem;">💡 Insight #{i+1}</h5>
                            <p style="color: #2C3E50; font-size: 0.95rem; margin-bottom: 0.8rem; line-height: 1.4;">
                                {insight_text[:100]}{"..." if len(insight_text) > 100 else ""}
                            </p>
                            <div style="background: rgba(255,255,255,0.7); border-radius: 6px; padding: 0.6rem; font-size: 0.85rem;">
                                <div style="color: #1976D2; font-weight: 600; margin-bottom: 0.3rem;">
                                    🚀 {actionable_step[:60]}{"..." if len(actionable_step) > 60 else ""}
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                # If only one insight, display it normally
                for i, insight in enumerate(psychographic_insights[:1]):
                    insight_text = insight.get('insight_text', '')
                    related_motivation = insight.get('related_motivation', '')
                    addresses_barrier = insight.get('addresses_barrier', '')
                    actionable_step = insight.get('actionable_next_step', '')
                    
                    st.info(f"💡 **Insight:** {insight_text}\n\n🚀 **Next step:** {actionable_step}")
        
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
        plan_header_col1, plan_header_col2 = st.columns([3, 1])
        
        # with plan_header_col1:
        #     st.subheader("🗓️ Your Challenges !!")

        st.markdown("""
        <div style="background: linear-gradient(135deg, #BFEE90 30%, #90EEBF 70%); 
                    border-radius: 15px; padding: 1.5rem; margin: 1.5rem 0; text-align: center; 
                    color: white; box-shadow: 0 6px 24px rgba(76, 175, 80, 0.3);">
            <h3 style="color: white; margin-bottom: 0.5rem; font-size: 1.75rem;">🗓️ Your Challenges !!</h3>
        </div>
        """, unsafe_allow_html=True)
                
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
                weekly_plan_id = str(latest_weekly_plan['id'])  # Use the UUID from weekly_plans table
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
                # Use the challenge's ID if available, otherwise use the index-based format
                challenge_id = challenge.get('id', f"challenge_{i+1}")
                challenge['completed'] = completion_map.get(challenge_id, challenge.get('completed', False))
            
            completed_count = sum(1 for challenge in weekly_challenges if challenge.get('completed', False))
            total_challenges = len(weekly_challenges)
            
            # Progress tracking display
            progress_percentage = (completed_count / total_challenges * 100) if total_challenges > 0 else 0
            
            # Progress header
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### 📊 Progress: {completed_count}/{total_challenges} Challenges")
            with col2:
                st.metric("Completion", f"{progress_percentage:.0f}%")
            
            # Progress bar
            st.progress(progress_percentage / 100)
            
            if completed_count >= 3:
                st.success("🎉 Great progress! Keep up the excellent work!")
            elif completed_count >= 1:
                st.info(f"💪 Keep going! You're making great progress!")
            else:
                st.info("🚀 Start completing challenges to build sustainable habits!")
            
            st.markdown("---")
            
            # Weekly Challenges Section
            st.subheader("🎯 Weekly Challenges")
            
            if not weekly_challenges:
                st.info("No challenges available. Generate new challenges to get started!")
            else:
                st.info(f"**This Week's Focus:** {week_focus} | **Total Challenges:** {len(weekly_challenges)}")
                
                for i, challenge in enumerate(weekly_challenges, 1):
                    challenge_completed = challenge.get('completed', False)
                    challenge_title = challenge.get('title', f'Challenge {i}')
                    challenge_difficulty = challenge.get('difficulty', challenge.get('difficulty_level', 'medium')).upper()
                    # Handle all possible CO2 savings field names from the JSON structure
                    co2_savings = challenge.get('co2_savings_kg', challenge.get('co2_savings', challenge.get('estimated_co2_savings_kg', 0)))
                    
                    # Color coding for difficulty
                    difficulty_colors = {
                        'EASY': '#4CAF50',
                        'MEDIUM': '#FF9800', 
                        'HARD': '#F44336'
                    }
                    difficulty_color = difficulty_colors.get(challenge_difficulty, '#666')
                    
                    # Status styling
                    if challenge_completed:
                        card_style = "background: #E8F5E8; border-left: 5px solid #4CAF50;"
                        status_icon = "✅"
                    else:
                        card_style = "background: white; border-left: 5px solid #2196F3;"
                        status_icon = "⏳"
                    
                    # Challenge card
                    col1, col2 = st.columns([4, 1])
                    
                    with col1:
                        # Handle both old and new data structures for description
                        description = challenge.get('description', challenge.get('action', ''))
                        category = challenge.get('category', 'General').title()
                        time_required = challenge.get('time_required', challenge.get('time', 'N/A'))
                        
                        st.markdown(f"""
                        <div style="{card_style} border-radius: 12px; padding: 1.5rem; margin: 1rem 0; 
                                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                                <h4 style="color: #2C3E50; margin: 0; flex: 1;">
                                    {status_icon} {challenge_title}
                                </h4>
                                <div style="display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap;">
                                    <span style="background: {difficulty_color}; color: white; padding: 0.3rem 0.8rem; 
                                                border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                                        {challenge_difficulty}
                                    </span>
                                    <span style="background: #E3F2FD; color: #1976D2; padding: 0.3rem 0.8rem; 
                                                border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                                        {co2_savings} kg CO₂
                                    </span>
                                    <span style="background: #F3E5F5; color: #7B1FA2; padding: 0.3rem 0.8rem; 
                                                border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                                        {category}
                                    </span>
                                </div>
                            </div>
                            <p style="color: #666; margin-bottom: 0.8rem; line-height: 1.5;">
                                {description}
                            </p>
                            <div style="display: flex; gap: 1rem; font-size: 0.85rem; color: #666;">
                                <span>⏱️ Time: {time_required}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if not challenge_completed:
                            if st.button(f"✅ Finish", key=f"complete_challenge_{i}", type="primary", use_container_width=True):
                                # Save task completion to database
                                success = False
                                if weekly_plan_id:
                                    # Use the challenge's ID if available, otherwise use index-based format
                                    task_id = challenge.get('id', f"challenge_{i}")
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
                                    st.error("❌ Cannot save completion: No valid weekly plan found.")
                                
                                if success:
                                    # Update in-memory status
                                    challenge['completed'] = True
                                    st.success(f"🎉 Challenge {i} completed!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("Failed to save completion.")
                        else:
                            st.success("✅ Done!")
                
                # Progress summary
                if len(weekly_challenges) > 0:
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Challenges Generated", len(weekly_challenges))
                    with col2:
                        st.metric("Completed", completed_count)
                    with col3:
                        progress_pct = (completed_count / len(weekly_challenges) * 100) if len(weekly_challenges) > 0 else 0
                        st.metric("Progress", f"{progress_pct:.0f}%")
                    
                    # Motivational message
                    if planner_data.get('motivation') or planner_data.get('motivation_message'):
                        motivation_msg = planner_data.get('motivation', planner_data.get('motivation_message'))
                        st.info(f"💪 **{motivation_msg}**")

            # Feedback Section after challenges
            st.markdown("---")
            st.subheader("💬 Customize Your Plan")
            
            # Display current feedback status
            current_feedback = get_current_week_feedback(user.id)
            feedback_history = get_user_feedback_history(user.id, limit=2)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Feedback input
                feedback_text = st.text_area(
                    "Share your thoughts:",
                    placeholder="Examples:\n• These challenges are too hard\n• I want more money-saving tips\n• Give me more home-based tasks\n• I don't have a car, focus on other areas",
                    height=100,
                    help="Your feedback helps our AI adapt your challenges to your preferences and constraints.",
                    key="feedback_text_area_after_challenges"
                )
                
                col_submit, col_regenerate = st.columns([1, 1])
                
                with col_submit:
                    if st.button("💾 Save Feedback", type="primary", key="save_feedback_after_challenges"):
                        if feedback_text.strip():
                            with st.spinner("Processing your feedback..."):
                                success = save_feedback_and_process(user.id, feedback_text)
                                if success:
                                    st.success("✅ Feedback saved! Use 'Regenerate Plan' to apply changes.")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to save feedback. Please try again.")
                        else:
                            st.warning("Please enter some feedback before saving.")
                
                with col_regenerate:
                    if st.button("🔄 Regenerate Plan", type="secondary", key="regenerate_plan_after_challenges"):
                        if current_feedback and current_feedback.get('feedback_summary'):
                            with st.spinner("🤖 Creating personalized plan based on your feedback..."):
                                try:
                                    ## AGENT 3 - FEEDBACK AWARE PLANNING accessed
                                    ## ==========================================
                                    # Run feedback-aware planning workflow with the saved feedback
                                    results = run_feedback_aware_planning_workflow(user.id, raw_feedback=current_feedback.get('user_feedback', ''))
                                    
                                    if results:
                                        # Parse and save the new plan
                                        from agent.utils import parse_agent3_text_output
                                        
                                        new_plan = parse_agent3_text_output(results, task_type="feedback_aware")
                                        
                                        if new_plan:
                                            # Save the new plan
                                            from data_model.database import save_weekly_plan_results, create_agent_session
                                            session_id = create_agent_session(user.id, "feedback_planning", "Feedback-aware planning")
                                            save_weekly_plan_results(user.id, session_id, new_plan)
                                            
                                            st.success("✅ Your plan has been updated based on your feedback!")
                                            st.balloons()
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to parse AI response")
                                    else:
                                        st.error("Failed to generate new plan")
                                        
                                except Exception as e:
                                    st.error(f"Error regenerating plan: {str(e)}")
                        else:
                            st.info("💡 Please provide feedback first, then regenerate your plan.")
            
            with col2:
                # Display feedback history
                if feedback_history:
                    st.markdown("""
                    <div style="background: #F3E5F5; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                        <h5 style="color: #7B1FA2; margin-bottom: 0.5rem;">📝 Recent Feedback</h5>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for i, feedback in enumerate(feedback_history[:2]):
                        st.markdown(f"""
                        <div style="background: white; border-radius: 8px; padding: 0.8rem; margin-bottom: 0.5rem; 
                                    border-left: 4px solid #9C27B0; font-size: 0.85rem;">
                            <strong style="color: #7B1FA2;">Week of {feedback['week_of']}:</strong><br>
                            <span style="color: #424242;">{feedback['summary']}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: #FFF3E0; border-radius: 10px; padding: 1rem; text-align: center;">
                        <div style="color: #E65100; font-size: 0.9rem;">
                            💡 No feedback yet<br>
                            <small>Share your thoughts to personalize your experience!</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        
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
                        from data_model.database import save_agent_results, create_agent_session, update_agent_session
                        from agent.crew import run_planner_workflow
                        
                        try:
                            
                            # Create agent session for planner
                            agent_session_id = create_agent_session(user.id, "weekly_planning", "Generate challenges workflow execution from dashboard")
                            
                            ## AGENT 3 - BASIC PLANNER (INITIAL PLANNER)
                            ## ==========================================
                            # Run the planner workflow
                            planner_results = run_planner_workflow(user.id)
                            
                            if planner_results:
                                try:
                                    # Parse JSON using existing function
                                    from agent.utils import parse_text_to_json
                                    weekly_plan_data = parse_text_to_json(planner_results)
                                    
                                    if weekly_plan_data:
                                        # Save the results
                                        save_agent_results(user.id, 'planner', weekly_plan_data, agent_session_id)
                                        save_weekly_plan_results(user.id, agent_session_id, weekly_plan_data)
                                        update_agent_session(agent_session_id, "completed", weekly_plan_data)
                                        
                                        st.success("✅ Weekly challenges generated successfully!")
                                        st.balloons()
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to parse AI response")
                                        update_agent_session(agent_session_id, "failed", {"error": "JSON parsing failed"})
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
        st.subheader("📝 Share Your Progress")
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
                        
                        ## AGENT 3 - UPDATE-PLANNER
                        ## ==========================================
                        # Run Agent 3 update workflow
                        update_results = run_update_planning_workflow(
                            user.id,
                            user_update
                        )
                        
                        if update_results:
                            try:
                                # Parse the updated plan using existing function
                                from agent.utils import parse_agent3_text_output
                                updated_plan_data = parse_agent3_text_output(update_results, task_type="update_planning", user_update_text=user_update)
                                
                                if updated_plan_data:
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
                                else:
                                    st.error("❌ Failed to parse Agent 3 response")
                            except Exception as e:
                                st.error(f"❌ Error running Agent 3 update: {str(e)}")
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
                        
                        # Run the planner workflow
                        planner_results = run_planner_workflow(user.id)
                        
                        if planner_results:
                            try:
                                # Parse JSON using existing function
                                from agent.utils import parse_text_to_json
                                weekly_plan_data = parse_text_to_json(planner_results)
                                
                                if weekly_plan_data:
                                    # Save the results
                                    save_agent_results(user.id, 'planner', weekly_plan_data, agent_session_id)
                                    save_weekly_plan_results(user.id, agent_session_id, weekly_plan_data)
                                    update_agent_session(agent_session_id, "completed", weekly_plan_data)
                                    
                                    st.success("✅ Weekly challenges generated successfully!")
                                    st.balloons()
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to parse AI response")
                                    update_agent_session(agent_session_id, "failed", {"error": "JSON parsing failed"})
                            except Exception as e:
                                st.error(f"Error processing results: {str(e)}")
                                update_agent_session(agent_session_id, "failed", {"error": str(e)})
                        else:
                            st.error("❌ Agent 3 failed to generate challenges")
                            update_agent_session(agent_session_id, "failed", {"error": "No results generated"})
                            
                    except Exception as e:
                        st.error(f"Error running Agent 3: {str(e)}")
