# pages/2_onboarding.py

import sys

try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    # This will fail on Windows, which is fine, as it will use the system's sqlite3
    pass
# --- END FIX ---

import streamlit as st
# import sys
import os
import json

# Add the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_model.auth import get_current_user, get_user_profile
from data_model.database import (
    check_onboarding_status,
    update_onboarding_status,
    save_onboarding_data,
    get_user_onboarding_data,
    save_agent_results,
    create_agent_session,
    update_agent_session,
    check_agents_status,
    get_agent_results,
    get_supabase,
    save_profiler_results,
    get_profiler_results
)

# ======================================================================================

def run_profiler_agent(user_id: str, user_data: dict):
    """Run Agent 1 (Profiler) to analyze data and generate enriched profile"""
    try:
        from agent.crew import run_profiler_workflow
        
        # Run the profiler workflow
        results = run_profiler_workflow(user_data)
        
        if results:
            # Parse the results
            if hasattr(results, 'json') and results.json:
                # If results.json is a string, parse it
                if isinstance(results.json, str):
                    parsed_results = json.loads(results.json)
                else:
                    parsed_results = results.json
            elif hasattr(results, 'raw'):
                parsed_results = json.loads(results.raw)
            else:
                parsed_results = results
            
            # Save to database in onboarding_final column
            save_success = save_profiler_results(user_id, parsed_results)
            
            if save_success:
                return parsed_results
            else:
                st.error("Failed to save profiler results")
                return None
        else:
            st.error("Profiler agent returned no results")
            return None
            
    except Exception as e:
        st.error(f"Error running profiler agent: {str(e)}")
        return None

def display_enriched_profile(profiler_results: dict):
    """Display the enriched profile results"""
    
    if not profiler_results:
        st.error("No profiler results available")
        return False
    
    st.markdown("---")
    st.subheader("🎯 Your Enriched Sustainability Profile")
    
    # Display key levers
    if 'key_levers' in profiler_results:
        st.markdown("### 🔧 Key Impact Areas")
        for i, lever in enumerate(profiler_results['key_levers'], 1):
            st.write(f"{i}. {lever}")
    
    # Display narrative
    if 'narrative_text' in profiler_results:
        st.markdown("### 📖 Your Profile Summary")
        st.info(profiler_results['narrative_text'])
    
    # Display demographics
    if 'demographics' in profiler_results:
        demo = profiler_results['demographics']
        st.markdown("### 🏠 Demographics")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Location:** {demo.get('location', 'N/A')}")
            st.write(f"**Climate:** {demo.get('climate', 'N/A')}")
        with col2:
            st.write(f"**Household Size:** {demo.get('household_size', 'N/A')}")
            st.write(f"**Home Type:** {demo.get('home_type', 'N/A')}")
    
    # Show continue button
    if st.button("🚀 Continue to Carbon Analysis", use_container_width=True, type="primary"):
        return True
    
    return False

# ======================================================================================

def run_analyst_agent(user_id: str):
    """
    Trigger Agent 2 (Analyst) workflow after onboarding completion
    """
    try:
        # Import agent workflows
        from agent.crew import run_analyst_workflow
        
        # Create agent session for this workflow
        agent_session_id = create_agent_session(user_id, "scoring", "Agent 2 (Analyst) workflow execution")
        
        if not agent_session_id:
            st.error("Failed to create agent session")
            return False
        
        # Run the analyst workflow with user_id (it will get enriched profile internally)
        results = run_analyst_workflow(user_id)
        
        if results:
            # Parse the results
            if hasattr(results, 'json') and results.json:
                # If results.json is a string, parse it
                if isinstance(results.json, str):
                    parsed_results = json.loads(results.json)
                else:
                    parsed_results = results.json
            elif hasattr(results, 'raw'):
                parsed_results = json.loads(results.raw)
            else:
                parsed_results = results
            
            # Validate results with Pydantic
            try:
                from agent.models import validate_analyst_output
                validated_results = validate_analyst_output(parsed_results)
                st.success("✅ Analyst output validation successful!")
            except ValueError as e:
                st.warning(f"⚠️ Analyst output validation failed: {str(e)}")
                # Continue anyway with unvalidated results
                validated_results = None
            
            # Save results to database
            save_success = save_agent_results(user_id, "analyst", parsed_results, agent_session_id)
            
            if save_success:
                # Update agent session as completed
                update_agent_session(agent_session_id, "completed", parsed_results)
                
                # ---------------------------------------------------------------------------
                # 🔄 AUTOMATIC PROFILE MERGING - Trigger when Agent 2 completes successfully
                # ---------------------------------------------------------------------------
                try:
                    from data_model.data_merge_json import merge_json
                    
                    # Call the complete workflow function that handles everything
                    merge_success = merge_json(user_id)
                    
                    if merge_success:
                        st.success("🎉 Complete profile with scores saved successfully!")
                    else:
                        st.warning("⚠️ Profile merging failed - check logs for details")
                        
                except Exception as merge_error:
                    st.error(f"❌ Error during profile merging: {str(merge_error)}")
                    # Don't fail the whole process if merging fails
                # ---------------------------------------------------------------------------
                return True
            else:
                update_agent_session(agent_session_id, "failed")
                return False
        else:
            st.error("Analyst agent returned no results")
            update_agent_session(agent_session_id, "failed")
            return False
            
    except Exception as e:
        st.error(f"Error triggering analyst workflow: {str(e)}")
        if 'agent_session_id' in locals():
            update_agent_session(agent_session_id, "failed")
        return False

# =========================== End of agents function calls ===========================

# Page configuration
st.set_page_config(
    page_title="EcoAction - Onboarding",
    page_icon="🌱",
    layout="wide"
)

# Check authentication status
current_user = get_current_user()

if not current_user:
       
    # Simple authentication message for onboarding
    st.markdown("""
    <div class="welcome-card">
        <h1>🌱 Welcome to EcoAction AI Onboarding!</h1>
        <p>Complete your sustainability profile to get personalized climate action recommendations.</p>
        <p><strong>Please sign in to your account or create a new one to continue with onboarding.</strong></p>
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
            if st.button("📝 Sign Up", use_container_width=True):
                st.switch_page("pages/1_auth.py")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center;">
        <p><strong>🌱 New to EcoAction AI?</strong></p>
        <p>Create your account to start tracking your environmental impact and get personalized sustainability recommendations!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.stop()

# User is authenticated, continue with normal onboarding
user = current_user
user_profile = get_user_profile(user.id)

# Check if onboarding is already completed
onboarding_completed = check_onboarding_status(user.id)
if onboarding_completed:
    
    # Display completion message
    user_name = user_profile.get('first_name', 'User')
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #5CE65C 0%, #45B745 100%); 
                border-radius: 20px; padding: 3rem; margin: 2rem auto; max-width: 800px; 
                box-shadow: 0 10px 30px rgba(92, 230, 92, 0.3); text-align: center; 
                color: #2C3E50; font-family: 'Poppins', sans-serif;">
        <h1 style="color: #2C3E50; font-weight: 700; margin-bottom: 1rem; font-size: 2.5rem;">
            ✅ Onboarding Already Completed!
        </h1>
        <p style="color: #2C3E50; font-size: 1.3rem; margin-bottom: 1rem;">
            Great job, {user_name}! You've already completed your sustainability onboarding.
        </p>
        <p style="color: #2C3E50; font-size: 1.1rem; margin-bottom: 2rem;">
            Your carbon footprint analysis should be ready. Check your dashboard to see your personalized insights and weekly challenges!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📊 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/3_dashboard.py")
        
        with col_b:
            if st.button("🔄 Restart Onboarding", use_container_width=True):
                if st.session_state.get('confirm_restart', False):
                    # User confirmed restart - delete their data
                    try:
                        supabase = get_supabase()
                        
                        supabase.table('user_profiles').delete().eq('user_id', user.id).execute()
                        supabase.table('user_scores').delete().eq('user_id', user.id).execute()
                        supabase.table('weekly_plans').delete().eq('user_id', user.id).execute()
                        supabase.table('agent_sessions').delete().eq('user_id', user.id).execute()
                        
                        update_onboarding_status(user.id, False)
                        
                        st.success("✅ Your profile has been reset! You can now start onboarding again.")
                        st.session_state.confirm_restart = False
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error resetting profile: {str(e)}")
                else:
                    st.session_state.confirm_restart = True
                    st.rerun()
    
    # Add Carbon Footprint Generation button
    st.markdown("---")
    st.markdown("### 🌱 Generate Your Carbon Footprint Analysis")
    st.info("💡 **Haven't generated your carbon footprint score yet?** Click below to run our AI analysis and get personalized insights!")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧮 Generate Carbon Footprint Score", use_container_width=True, type="primary"):
            with st.spinner("🤖 Our AI is analyzing your carbon footprint... This may take a moment."):
                agent_success = run_analyst_agent(user.id)
                
            if agent_success:
                st.success("🎉 **Carbon analysis complete!** Your dashboard is ready with personalized recommendations.")
                
                # Display carbon footprint result
                try:
                    agent_results = get_agent_results(user.id)
                    if agent_results:
                        footprint = agent_results.get("carbon_footprint_data", {}).get("calculation_data", {}).get("total_carbon_footprint_tonnes")
                        if footprint is not None:
                            st.metric(
                                label="Your Estimated Annual Carbon Footprint",
                                value=f"{footprint:.2f} tonnes CO₂e"
                            )
                except Exception as e:
                    st.warning(f"Could not display footprint analysis results: {e}")

                st.balloons()
                
                if st.button("📊 View Your Dashboard", use_container_width=True, type="secondary"):
                    st.switch_page("pages/3_dashboard.py")
            else:
                st.error("❌ There was an error running the analysis. Please try again.")
    
    if st.session_state.get('confirm_restart', False):
        st.warning("⚠️ **Restarting onboarding will permanently delete:**")
        st.markdown("""
        - Your complete user profile
        - Carbon footprint analysis results  
        - Weekly sustainability plans
        - All agent session data
        
        **Click 'Restart Onboarding' again to confirm this action.**
        """)
        
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.confirm_restart = False
            st.rerun()
    
    st.stop()

# Get display name
display_name = user_profile.get('first_name', user.email)

# Sidebar
with st.sidebar:
    st.title(f"🌱 {display_name}")
    st.markdown("---")
    st.page_link("pages/1_auth.py", label="Account", icon="🔐")
    st.page_link("pages/2_onboarding.py", label="Onboarding", icon="🌟")
    st.page_link("pages/3_dashboard.py", label="Dashboard", icon="📊")
    st.markdown("---")
    st.info("🚀 Complete your profile to get personalized recommendations!")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        from data_model.auth import logout
        logout()
        st.rerun()
    st.markdown("---")
    st.caption("EcoAction AI v1.0")
    
    # # Logout button
    # if st.button("🚪 Logout", type="primary", use_container_width=True):
    #     # Clear the session state for authentication
    #     if 'authenticated' in st.session_state:
    #         del st.session_state['authenticated']
    #     if 'user' in st.session_state:
    #         del st.session_state['user']
        
    #     st.success("✅ Successfully logged out!")
    #     st.rerun()


# Header
st.title("🌱 Welcome to EcoAction AI!")
st.markdown(f"Hello **{display_name}**! Let's set up your personalized sustainability journey.")
st.markdown("")

# Form introduction
st.markdown("""
<div class="form-intro">
    <h3>📝 Complete Your Sustainability Profile</h3>
    <p>Help us understand your lifestyle to provide personalized sustainability insights and recommendations. Our AI will analyze your responses to create your personalized profile.</p>
</div>
""", unsafe_allow_html=True)

# Define form keys for state management
form_keys = [
    "country", "city", "climate", "household_size", "home_type", "home_size", "ownership",
    "appliances", "heating_source", "air_conditioning", "energy_conservation",
    "primary_transport","other_transport", "car_type", "vehicle_fuel", "commute_distance",
    "rideshare_usage", "public_transport_usage", "diet_type", "meat_frequency",
    "food_waste", "shopping_frequency", "clothes_shopping", "new_vs_secondhand",
    "eco_importance", "recycling_habits", "composting", "plastic_usage",
    "flights_per_year", "flight_reason", "lifestyle", "hobbies", "ai_queries_daily",
    "image_generation_monthly", "video_streaming_daily", "cloud_storage_usage",
    "device_usage", "online_meetings_weekly", "main_motivation", "biggest_challenge",
    "improvement_area", "additional_info"
]

with st.form("onboarding_form"):
    # Location & Climate
    st.subheader("🌍 Location & Climate")
    col1, col2 = st.columns(2)
    with col1:
        country = st.text_input("Country", key="country")
        city = st.text_input("City", key="city")        
    with col2:
        climate = st.pills("Climate", 
            ["Tropical", "Arid", "Temperate", "Continental", "Polar", "Mediterranean", "Subtropical", "Monsoon", "Savanna", "Tundra", "Highland"], 
            key="climate")
    
    st.info("💡 Please fill out at least 15 fields, in order to save profile and generate your Carbon !!")

    # Household
    st.subheader("🏠 Household Information")
    col1, col2 = st.columns(2)
    with col1:
        household_size = st.number_input("Number of people in the house", min_value=1, max_value=20, value=1, key="household_size")
        home_type = st.pills("Type of Home", ["House", "Apartment", "Condo"], key="home_type", selection_mode="multi")
        home_size = st.text_input("Approx Size of Home (square feet / m²)", key="home_size")
        ownership = st.pills("Do you own or rent your home?", ["Own", "Rent"], key="ownership", selection_mode="multi")
    with col2:
        appliances = st.pills("Key Appliances & Devices", ["Refrigerator", "Washing Machine", "Microwave", "Oven", "Dishwasher", "Air Conditioner", "Heater", "Ceiling Fan", "Vacuum Cleaner", "Toaster", "Electric Kettle", "Blender", "Coffee Maker", "Juicer", "Rice Cooker", "Iron", "Hair Dryer", "Television", "Personal Computer", "Water Purifier", "Printer", "Space Heater", "Sewing Machine", "Speaker", "Lamp", "Gaming PC (1000 Watts)", "Old Refrigerator (>5 years), Old Washing Machine (>5 years)", "Geyser"], key="appliances", selection_mode="multi")
        heating_source = st.pills("Primary Heating Source", ["Natural Gas", "Electricity", "Oil", "Other", "Solar", "Petrol", "Coal", "Kerosene"], key="heating_source", selection_mode="multi")
        air_conditioning = st.pills("Use Air Conditioning?", ["Never", "Rarely", "Sometimes", "Often", "Always"], key="air_conditioning", selection_mode="single")
        energy_conservation = st.pills("Do you make an effort to turn off lights and unplug devices when not in use?", ["Rarely", "Often", "All the time"], key="energy_conservation", selection_mode="single")

    # Transport
    st.subheader("🚗 Transportation")
    col1, col2 = st.columns(2)
    with col1:
        primary_transport = st.pills("Primary Mode of Transport", ["Personal Car", "Public Bus", "Public Train", 
                                                                   "Public Ferry", "Walking", "Ride-sharing", "Bicycle",
                                                                   "Electric Scooter", "Taxi Car", "Motorcycle", "Other low fuel options"], 
                                                                   key="primary_transport", 
                                                                   selection_mode="single")
        other_transport = st.pills("Other Modes of Transport", ["Personal Car", "Public Bus", "Public Train", 
                                                                   "Public Ferry", "Walking", "Ride-sharing", "Bicycle",
                                                                   "Electric Scooter", "Taxi Car", "Motorcycle", "Other low fuel options"], 
                                        key="other_transport", 
                                        selection_mode="multi")
        
        car_type = st.pills("Type of Car", ["Sedan", "SUV", "Truck", "Coupe", "Hatchback"], 
                            key="car_type", selection_mode="multi")
        
        vehicle_fuel = st.pills("Fuel in the vehicle you use", ["Electric", "Hybrid", "Petrol", "Diesel", "None"], 
                                key="vehicle_fuel",
                                selection_mode="multi")
        
        commute_distance = st.text_input("Daily commute distance (Total) in miles or km", 
                                         key="commute_distance")
    
    with col2:
        rideshare_usage = st.pills("Use ride-sharing (Uber/Lyft) or taxis?", ["Never", "Occasionally", "Weekly", "Daily"], 
                                   key="rideshare_usage", 
                                   selection_mode="single")
        public_transport_usage = st.pills("Use public transportation?", ["Never", "Occasionally", "Weekly", "Daily"], 
                                          key="public_transport_usage", 
                                          selection_mode="single")
    
    # Diet & Habits
    st.subheader("🍽️ Diet & Food Habits")
    col1, col2 = st.columns(2)
    with col1:
        diet_type = st.pills("Diet Type", ["Vegan", "Vegetarian", "Pescatarian", "Omnivore", "Non-Vegetarian", 
                                           "Paleo", "Keto", "Low-Carb", "Low-Fat", "Mediterranean", "Dash", 
                                           "Raw Food", "Gluten-Free", "Lactose-Free", "Diabetic", "High-Protein", 
                                           "Low-Sodium", "Whole30", "Fruititarian", "Flexitarian", "Zone Diet", 
                                           "South Beach", "Atkins", "Macros Diet"], 
                                           key="diet_type", 
                                           selection_mode="multi")
        meat_frequency = st.pills("Meat consumption frequency", ["Never", "Once a Month", "A few times a week", "Once a day", "Multiple times a day"], 
                                  key="meat_frequency", 
                                  selection_mode="single")
    with col2:
        food_waste = st.pills("Food waste habits", ["Rarely/Never", "Sometimes", "Often"], 
                              key="food_waste", 
                              selection_mode="single")
        shopping_frequency = st.pills("Shopping Frequency", ["Daily", "A few times a week", "Weekly", "Less than weekly"], 
                                       key="shopping_frequency", 
                                       selection_mode="single")

    # Consumption & Shopping
    st.subheader("🛍️ Consumption & Shopping")
    col1, col2 = st.columns(2)
    with col1:
        clothes_shopping = st.pills("New Clothes Shopping Frequency", 
                                    ["Rarely", "Seasonally", "Monthly", "Weekly"], 
                                    key="clothes_shopping", 
                                    selection_mode="single")
        new_vs_secondhand = st.pills("Preference for New vs. Second-hand", 
                                     ["Primarily new", "A mix of both", "Primarily second-hand"], 
                                     key="new_vs_secondhand", 
                                     selection_mode="single")
        eco_importance = st.pills("Importance of Eco-Friendly Products", 
                                  ["Not important", "Somewhat important", "Very important"], 
                                  key="eco_importance", selection_mode="single")
    with col2:
        recycling_habits = st.pills("Recycling Habits", 
                                    ["I don't recycle", "I recycle sometimes", "I recycle everything I can"], 
                                    key="recycling_habits", selection_mode="single")
        composting = st.pills("Do you compost food waste?", 
                              ["Yes", "No", "I'd like to start"], 
                              key="composting", selection_mode="single")
        plastic_usage = st.pills("Single-Use Plastics Usage", 
                                 ["Never", "Rarely", "Sometimes", "Often"], 
                                 key="plastic_usage", selection_mode="single")
    
    # Travel & Lifestyle
    st.subheader("✈️ Travel & Lifestyle")
    col1, col2 = st.columns(2)
    with col1:        
        flights_per_year = st.pills("Flights per year", 
                                    ["0", "1-2 short-haul", "3+ short-haul", "1-2 long-haul", "3+ long-haul"], 
                                    key="flights_per_year", selection_mode="single")
        flight_reason = st.pills("Main reason for flights", 
                                 ["Vacation", "Work", "Family", "Other reasons", "N/A"], 
                                 key="flight_reason", selection_mode="multi")
    with col2:
        lifestyle = st.pills("Describe your overall lifestyle", 
                             ["Minimalist", "Average consumer", "High consumer"], 
                             key="lifestyle", selection_mode="single")
        hobbies = st.pills("Select your common hobbies", 
                           ["Gardening", "Gaming", "Travel", "Sports", "Cooking", "DIY"], 
                           key="hobbies", selection_mode="multi")

    # AI Usage & Digital Footprint
    st.subheader("🤖 AI Usage & Digital Footprint")
    col1, col2 = st.columns(2)
    with col1:
        ai_queries_daily = st.pills("ChatGPT/AI queries per day", ["0", "1-5", "6-20", "21-50", "50+"], 
                                    key="ai_queries_daily", selection_mode="single")
        image_generation_monthly = st.pills("AI image generation per month (DALL-E, Midjourney, etc.)", ["0", "1-10", "11-50", "51-100", "100+"], key="image_generation_monthly", selection_mode="single")
        video_streaming_daily = st.pills("Video streaming hours per day (YouTube, Netflix, etc.)", ["0-1", "1-3", "3-5", "5-8", "8+"], key="video_streaming_daily", selection_mode="single")
    with col2:
        cloud_storage_usage = st.pills("Cloud storage usage (Google Drive, iCloud, etc.)", ["None", "Light (< 50GB)", "Moderate (50-500GB)", "Heavy (500GB-2TB)", "Very Heavy (2TB+)"], key="cloud_storage_usage", selection_mode="single")
        device_usage = st.pills("Primary devices used daily", ["Smartphone", "Laptop", "Desktop PC", "Tablet", "Smart TV", "Gaming Console", "Smart Watch"], key="device_usage", selection_mode="single")
        online_meetings_weekly = st.pills("Video calls/meetings per week", ["0", "1-5", "6-15", "16-30", "30+"], key="online_meetings_weekly", selection_mode="single")

    # Goals & Motivation
    st.subheader("🎯 Goals & Motivation")
    col1, col2 = st.columns(2)
    with col1:
        main_motivation = st.pills("Main Motivation", 
                                   ["Saving money", "Protecting the environment", 
                                    "Social responsibility", "Health reasons"], 
                                   key="main_motivation", selection_mode="multi")
        
        biggest_challenge = st.pills("Biggest Challenge", 
                                     ["Cost", "Convenience", "Not knowing what to do", 
                                      "Lack of time", "Laziness", "Bad Tips on how to help"], 
                                     key="biggest_challenge", selection_mode="multi")
    with col2:
        improvement_area = st.pills("Area you most want to improve", 
                                    ["Reducing carbon footprint", "Saving money on bills", 
                                     "Reducing waste", "Eating healthier"], 
                                     key="improvement_area", 
                                     selection_mode="multi")
        
        improvement_area_other = st.text_input("If you have other areas as well", key="improvement_area_other")

    # Additional Information
    st.subheader("💭 Tell Us More")
    additional_info = st.text_area("In about 100 words, tell me anything else...", 
                                   height=120, 
                                   placeholder="Share any additional insights...", 
                                   key="additional_info")
    
    
    submitted = st.form_submit_button("🌟 Save Profile")

if submitted:
    filled_count = sum(1 for key in form_keys if st.session_state.get(key))

    if not st.session_state.get('city') or not st.session_state.get('climate') or st.session_state.get('household_size', 0) < 1:
        st.error("⚠️ Please fill in all required fields: **City**, **Climate**, and **Household Size**.")
    elif filled_count < 15:
        st.error(f"⚠️ Please fill in at least **15 fields** to get an accurate analysis. You have filled **{filled_count}**.")
    else:
        user_data = {key: st.session_state.get(key) for key in form_keys}
        user_data["user_id"] = user.id
        
        # Re-nest the dictionary to match the agent's expected input structure
        nested_user_data = {
            "user_id": user.id,
            "location": {"city": user_data["city"], "country": user_data["country"], "climate": user_data["climate"]},
            "household": {"size": user_data["household_size"], "home_type": user_data["home_type"], "home_size": user_data["home_size"], "ownership": user_data["ownership"], "heating_source": user_data["heating_source"], "air_conditioning": user_data["air_conditioning"], "appliances": user_data["appliances"], "energy_conservation": user_data["energy_conservation"]},
            "transportation": {"primary_transport": user_data["primary_transport"], 
                               "car_type": user_data["car_type"], 
                               "vehicle_fuel": user_data["vehicle_fuel"], 
                               "commute_distance": user_data["commute_distance"], 
                               "rideshare_usage": user_data["rideshare_usage"], 
                               "public_transport_usage": user_data["public_transport_usage"]},
            "diet": {"diet_type": user_data["diet_type"], "meat_frequency": user_data["meat_frequency"], "food_waste": user_data["food_waste"], "shopping_frequency": user_data["shopping_frequency"]},
            "consumption": {"clothes_shopping": user_data["clothes_shopping"], "new_vs_secondhand": user_data["new_vs_secondhand"], "eco_importance": user_data["eco_importance"], "recycling_habits": user_data["recycling_habits"], "composting": user_data["composting"], "plastic_usage": user_data["plastic_usage"]},
            "travel": {"flights_per_year": user_data["flights_per_year"], "flight_reason": user_data["flight_reason"], "lifestyle": user_data["lifestyle"], "hobbies": user_data["hobbies"]},
            "digital": {"ai_queries_daily": user_data["ai_queries_daily"], "image_generation_monthly": user_data["image_generation_monthly"], "video_streaming_daily": user_data["video_streaming_daily"], "cloud_storage_usage": user_data["cloud_storage_usage"], "device_usage": user_data["device_usage"], "online_meetings_weekly": user_data["online_meetings_weekly"]},
            "goals": {"main_motivation": user_data["main_motivation"], "biggest_challenge": user_data["biggest_challenge"], "improvement_area": user_data["improvement_area"], "other_improvement_area": user_data.get("improvement_area_other")},
            "additional_info": user_data["additional_info"]
        }

        with st.spinner("💾 Saving your profile..."):
            save_success = save_onboarding_data(user.id, nested_user_data)
        
        if save_success:
            st.success("✅ Profile saved successfully!")
            
            # Running Agent 1 - Profiler Directly
            with st.spinner("🧠 AI is analyzing your profile..."):
                profiler_results = run_profiler_agent(user.id, nested_user_data)
            
            if profiler_results:
                update_onboarding_status(user.id, True)
                st.info("ℹ️ Profile enriched successfully!")
                st.info("Onboarding complete!")
                
                # Show enriched profile
                profile_completed = display_enriched_profile(profiler_results)
                
                if profile_completed:
                    # Continue to analyst workflow
                    with st.spinner("🤖 Our AI is analyzing your carbon footprint... This may take a moment."):
                        agent_success = run_analyst_agent(user.id)

                    if agent_success:                        
                        st.success("🎉 **Carbon analysis complete!** Your dashboard is ready with personalized recommendations.")
                        
                        # Display carbon footprint result
                        try:
                            agent_results = get_agent_results(user.id)
                            if agent_results:
                                footprint = agent_results.get("carbon_footprint_data", {}).get("calculation_data", {}).get("total_carbon_footprint_tonnes")
                                if footprint is not None:
                                    st.metric(
                                        label="Your Estimated Annual Carbon Footprint",
                                        value=f"{footprint:.2f} tonnes CO₂e"
                                    )
                        except Exception as e:
                            st.warning(f"Could not display footprint analysis results: {e}")

                        st.balloons()
                        
                        if st.button("📊 Go to Dashboard", use_container_width=True, type="primary"):
                            st.switch_page("pages/3_dashboard.py")
                            
                        # Clear form state
                        for key in form_keys:
                            if key in st.session_state:
                                del st.session_state[key]
                    else:
                        st.error("❌ There was an error running the analysis. Please try again from the dashboard.")
            else:
                st.error("❌ Error running AI analysis.")
                
                # # Continue to analyst workflow even if profiler fails
                # with st.spinner("🤖 Our AI is analyzing your carbon footprint..."):
                #     agent_success = run_analyst_agent(user.id)
                # if agent_success:
                #     st.success("🎉 **Carbon analysis complete!**")
                #     if st.button("📊 Go to Dashboard", use_container_width=True, type="primary"):
                #         st.switch_page("pages/3_dashboard.py")
        else:
            st.error("❌ Error saving your profile. Please try again.")
