# pages/2_onboarding.py
import streamlit as st
import sys
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
    get_supabase
)

def trigger_agent_workflow(user_id: str):
    """Trigger Agent 2 (Analyst) workflow after onboarding completion"""
    try:
        # Import agent workflows
        from agent.crew import run_analyst_workflow
        
        # Create agent session for this workflow
        agent_session_id = create_agent_session(user_id, "scoring", "Agent 2 (Analyst) workflow execution")
        
        if not agent_session_id:
            st.error("Failed to create agent session")
            return False
        
        # Get user data for agents
        user_data = get_user_onboarding_data(user_id)
        
        if user_data:
            # Run the agent workflow
            results = run_analyst_workflow(user_data)
            
            if results:
                # Parse the results - expecting combined calculation and benchmark data
                if hasattr(results, 'json'):
                    parsed_results = json.loads(results.json)
                elif hasattr(results, 'raw'):
                    parsed_results = json.loads(results.raw)
                else:
                    parsed_results = results
                
                # Save results to database
                save_success = save_agent_results(user_id, "analyst", parsed_results, agent_session_id)
                
                if save_success:
                    # Update agent session as completed
                    update_agent_session(agent_session_id, "completed", parsed_results)
                    return True
                else:
                    update_agent_session(agent_session_id, "failed")
                    return False
            else:
                update_agent_session(agent_session_id, "failed")
                return False
        else:
            st.error("No user data found for analysis")
            update_agent_session(agent_session_id, "failed")
            return False
            
    except Exception as e:
        st.error(f"Error triggering agent workflow: {str(e)}")
        if 'agent_session_id' in locals():
            update_agent_session(agent_session_id, "failed")
        return False

# Page configuration
st.set_page_config(
    page_title="EcoAction - Onboarding",
    page_icon="🌱",
    layout="wide"
)

# Check authentication status
current_user = get_current_user()

if not current_user:
    # Independent page styling - comprehensive visual theme
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
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom welcome card styling */
    .welcome-card {
        background: linear-gradient(135deg, #5CE65C 0%, #45B745 100%) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        margin: 2rem auto !important;
        max-width: 800px !important;
        box-shadow: 0 10px 30px rgba(92, 230, 92, 0.3) !important;
        text-align: center !important;
        color: #2C3E50 !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .welcome-card h1 {
        color: #2C3E50 !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        font-size: 2.5rem !important;
    }
    
    .welcome-card p {
        color: #2C3E50 !important;
        font-size: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
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
    
    st.stop()  # Don't show the rest of the onboarding page

# User is authenticated, continue with normal onboarding
user = current_user
user_profile = get_user_profile(user.id)

# Check if onboarding is already completed
onboarding_completed = check_onboarding_status(user.id)
if onboarding_completed:
    # Apply simple styles for completed onboarding
    st.markdown("""
    <style>
    /* Import Poppins font family */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #ffffff 100%) !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1200px !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
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
    </style>
    """, unsafe_allow_html=True)
    
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
                        
                        # Delete from user_profiles table
                        supabase.table('user_profiles').delete().eq('user_id', user.id).execute()
                        
                        # Delete from user_scores table
                        supabase.table('user_scores').delete().eq('user_id', user.id).execute()
                        
                        # Delete from weekly_plans table
                        supabase.table('weekly_plans').delete().eq('user_id', user.id).execute()
                        
                        # Delete from agent_sessions table
                        supabase.table('agent_sessions').delete().eq('user_id', user.id).execute()
                        
                        # Update onboarding status to false
                        update_onboarding_status(user.id, False)
                        
                        st.success("✅ Your profile has been reset! You can now start onboarding again.")
                        st.session_state.confirm_restart = False
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error resetting profile: {str(e)}")
                else:
                    # First click - ask for confirmation
                    st.session_state.confirm_restart = True
                    st.rerun()
    
    if st.session_state.get('confirm_restart', False):
        st.warning("⚠️ **Restarting onboarding will permanently delete:**")
        st.markdown("""
        - Your complete user profile
        - Carbon footprint analysis results  
        - Weekly sustainability plans
        - All agent session data
        
        **Click 'Restart Onboarding' again to confirm this action.**
        """)
        
        # Add a cancel button
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.confirm_restart = False
            st.rerun()
    
    st.stop()  # Don't show the onboarding form

# Get display name
if user_profile and user_profile.get('first_name'):
    display_name = user_profile['first_name']
    full_name = f"{user_profile['first_name']} {user_profile['last_name']}"
else:
    display_name = user.first_name if hasattr(user, 'first_name') and user.first_name else user.email
    full_name = f"{user.first_name} {user.last_name}" if hasattr(user, 'first_name') and hasattr(user, 'last_name') and user.first_name and user.last_name else user.email

# Independent page styling - comprehensive visual theme
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

/* Form styling */
.stForm {
    background: rgba(255, 255, 255, 0.95) !important;
    padding: 2rem !important;
    border-radius: 20px !important;
    border: 1px solid rgba(100, 149, 237, 0.2) !important;
    box-shadow: 0 8px 32px rgba(100, 149, 237, 0.1) !important;
    backdrop-filter: blur(10px) !important;
    margin: 1rem 0 !important;
}

/* Input field styling */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 2px solid #E8F4FD !important;
    border-radius: 12px !important;
    padding: 0.75rem 1rem !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 16px !important;
    background: rgba(255, 255, 255, 0.9) !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6495ED !important;
    box-shadow: 0 0 0 3px rgba(100, 149, 237, 0.1) !important;
    outline: none !important;
}

/* Label styling */
.stTextInput > label,
.stSelectbox > label,
.stNumberInput > label,
.stTextArea > label,
.stRadio > label,
.stCheckbox > label {
    font-family: 'Poppins', sans-serif !important;
    font-weight: 500 !important;
    color: #2C3E50 !important;
    font-size: 16px !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Form intro styling */
.form-intro {
    background: #f8f9fa !important;
    padding: 1.5rem !important;
    border-radius: 10px !important;
    margin-bottom: 2rem !important;
    border-left: 4px solid #6495ED !important;
    font-family: 'Poppins', sans-serif !important;
}

.form-intro h3 {
    color: #2C3E50 !important;
    margin-bottom: 1rem !important;
}

.form-intro p {
    color: #2C3E50 !important;
    margin-bottom: 0 !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar with navigation and user info
with st.sidebar:
    st.title(f"🌱 {display_name}")
    st.markdown("---")
    
    # Navigation
    st.page_link("pages/3_dashboard.py", label="Dashboard", icon="📊")
    st.page_link("pages/2_onboarding.py", label="Onboarding", icon="🌟")
    st.page_link("pages/1_auth.py", label="Account", icon="🔐")
    
    st.markdown("---")
    
    # Onboarding progress
    st.info("🚀 Complete your profile to get personalized recommendations!")
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        from data_model.auth import logout
        logout()
        st.rerun()
    
    st.markdown("---")
    st.caption("EcoAction AI v1.0")

# Header
st.title("🌱 Welcome to EcoAction AI!")
st.markdown(f"Hello **{display_name}**! Let's set up your personalized sustainability journey.")
st.markdown("")

# Form introduction
st.markdown("""
<div class="form-intro">
    <h3>📝 Complete Your Sustainability Profile</h3>
    <p>Help us understand your lifestyle to provide personalized sustainability insights and recommendations. Our AI will analyze your responses and may ask follow-up questions to better understand your unique situation.</p>
</div>
""", unsafe_allow_html=True)

with st.form("onboarding_form"):
    # Location & Climate
    st.subheader("🌍 Location & Climate")
    
    col1, col2 = st.columns(2)
    with col1:
        city = st.text_input("City")
    with col2:
        climate = st.pills("Climate", 
            ["Tropical", "Arid", "Temperate", "Continental", "Polar", "Mediterranean", "Subtropical", "Monsoon", "Savanna", "Tundra", "Highland"], 
            selection_mode="multi")
    
    # Household
    st.subheader("🏠 Household Information")
    
    col1, col2 = st.columns(2)
    with col1:
        household_size = st.number_input("Number of people in the house", min_value=1, max_value=20, value=1)
        home_type = st.pills("Type of Home", ["House", "Apartment", "Condo"], selection_mode="multi")
        home_size = st.text_input("Approx Size of Home (square feet / m²)")
        ownership = st.pills("Do you own or rent your home?", ["Own", "Rent"], selection_mode="single")
    
    with col2:
        heating_source = st.pills("Primary Heating Source", 
            ["Natural Gas", "Electricity", "Oil", "Other", "Solar", "Petrol-based"], selection_mode="multi")
        
        air_conditioning = st.pills("Use Air Conditioning?", 
            ["Never", "Rarely", "Sometimes", "Often", "Always"], selection_mode="single")
        
        energy_provider = st.text_input("Energy Provider (e.g., PG&E, EDF, etc.)")
        
        appliances = st.pills("Key Appliances & Devices", [
                            "Refrigerator", "Washing Machine", "Microwave", "Oven", "Dishwasher",
                            "Air Conditioner", "Heater", "Ceiling Fan", "Vacuum Cleaner", "Toaster",
                            "Electric Kettle", "Blender", "Coffee Maker", "Juicer", "Rice Cooker",
                            "Iron", "Hair Dryer", "Television", "Personal Computer", "Water Purifier",
                            "Printer", "Space Heater", "Sewing Machine", "Speaker", "Lamp", "Gaming PC (1000 Watts)",
                            "Old Refrigerator (>5 years), Old Washing Machine (>5 years)", "Geyser"
                        ], 
            selection_mode="multi")
    
    energy_conservation = st.pills("Do you make an effort to turn off lights and unplug devices when not in use?", 
                                   ["Rarely", "Often", "All the time"], 
                                   selection_mode="single")
    
    # Transport
    st.subheader("🚗 Transportation")
    
    col1, col2 = st.columns(2)
    with col1:
        primary_transport = st.pills("Primary Mode of Transport", 
                                     ["Personal Car", "Public Bus", "Public Train", "Public Ferry",
                                      "Walking", "Ride-sharing", "Bicycle","Electric Scooter", "Taxi Car"
                                      "Motorcycle", "Other low fuel options"], 
                                   selection_mode="multi")
        car_type = st.pills("Type of Car", ["Sedan", "SUV", "Truck", "Coupe", "Hatchback"], 
                            selection_mode="multi")
        vehicle_fuel = st.pills("Fuel in the vehicle you use", 
                               ["Electric", "Hybrid", "Petrol", "Diesel", "None"], selection_mode="multi")
        commute_distance = st.text_input("Daily commute distance (Total) in miles or km")
    
    with col2:
        rideshare_usage = st.pills("Use ride-sharing (Uber/Lyft) or taxis?", 
                            ["Never", "Occasionally", "Weekly", "Daily"], selection_mode="single")
        public_transport_usage = st.pills("Use public transportation?", 
                            ["Never", "Occasionally", "Weekly", "Daily"], selection_mode="single")
    
    # Diet & Habits
    st.subheader("🍽️ Diet & Food Habits")
    
    col1, col2 = st.columns(2)
    with col1:
        diet_type = st.pills("Diet Type", 
            ["Vegan", "Vegetarian", "Pescatarian", "Omnivore", "Carnivore",
                "Paleo", "Keto", "Low-Carb", "Low-Fat", "Mediterranean",
                "Dash", "Raw Food", "Gluten-Free", "Lactose-Free", "Diabetic",
                "High-Protein", "Low-Sodium", "Whole30", "Fruititarian", "Flexitarian",
                "Zone Diet", "South Beach", "Atkins", "Macros Diet", "Intermittent Fasting", "Other"
            ], selection_mode="single")
        meat_frequency = st.pills("Meat consumption frequency", 
            ["Never", "Once a Month", "A few times a week", "Once a day", "Multiple times a day"], selection_mode="single")
    
    with col2:
        food_waste = st.pills("Food waste habits", 
            ["Rarely/Never", "Sometimes", "Often"], selection_mode="single")
        shopping_frequency = st.pills("Shopping Frequency", 
            ["Daily", "A few times a week", "Weekly", "Less than weekly"], selection_mode="single")
    
    # Consumption & Shopping
    st.subheader("🛍️ Consumption & Shopping")
    
    col1, col2 = st.columns(2)
    with col1:
        clothes_shopping = st.pills("New Clothes Shopping Frequency", 
                ["Rarely", "Seasonally", "Monthly", "Weekly"], 
                selection_mode="single")
        
        new_vs_secondhand = st.pills("Preference for New vs. Second-hand", 
                ["Primarily new", "A mix of both", "Primarily second-hand"], 
                selection_mode="single")
        
        eco_importance = st.pills("Importance of Eco-Friendly Products", 
                ["Not important", "Somewhat important", "Very important"], 
                selection_mode="single")
    
    with col2:
        recycling_habits = st.pills("Recycling Habits", 
            ["I don't recycle", "I recycle sometimes", "I recycle everything I can"], 
            selection_mode="single")
        
        composting = st.pills("Do you compost food waste?", 
            ["Yes", "No", "I'd like to start"], 
            selection_mode="single")
        
        plastic_usage = st.pills("Single-Use Plastics Usage", 
            ["Never", "Rarely", "Sometimes", "Often"], 
            selection_mode="single")
    
    # Travel & Lifestyle
    st.subheader("✈️ Travel & Lifestyle")
    
    col1, col2 = st.columns(2)
    with col1:        
        flights_per_year = st.pills("Flights per year", 
            ["0", "1-2 short-haul", "3+ short-haul", "1-2 long-haul", "3+ long-haul"], 
            selection_mode="single")
        
        flight_reason = st.pills("Main reason for flights", 
            ["Vacation", "Work", "Family", "Other reasons", "N/A"], selection_mode="single")
    
    with col2:
        lifestyle = st.pills("Describe your overall lifestyle", 
            ["Minimalist", "Average consumer", "High consumer"], selection_mode="single")
        hobbies = st.pills("Select your common hobbies", 
            ["Gardening", "Gaming", "Travel", "Sports", "Cooking", "DIY"], selection_mode="multi")
    
    # AI Usage & Digital Footprint
    st.subheader("🤖 AI Usage & Digital Footprint")
    
    col1, col2 = st.columns(2)
    with col1:
        ai_queries_daily = st.pills("ChatGPT/AI queries per day", 
            ["0", "1-5", "6-20", "21-50", "50+"], selection_mode="single")
        
        image_generation_monthly = st.pills("AI image generation per month (DALL-E, Midjourney, etc.)", 
            ["0", "1-10", "11-50", "51-100", "100+"], selection_mode="single")
        
        video_streaming_daily = st.pills("Video streaming hours per day (YouTube, Netflix, etc.)", 
            ["0-1", "1-3", "3-5", "5-8", "8+"], selection_mode="single")
    
    with col2:
        cloud_storage_usage = st.pills("Cloud storage usage (Google Drive, iCloud, etc.)", 
            ["None", "Light (< 50GB)", "Moderate (50-500GB)", "Heavy (500GB-2TB)", "Very Heavy (2TB+)"], 
            selection_mode="single")
        
        device_usage = st.pills("Primary devices used daily", 
            ["Smartphone", "Laptop", "Desktop PC", "Tablet", "Smart TV", "Gaming Console", "Smart Watch"], 
            selection_mode="multi")
        
        online_meetings_weekly = st.pills("Video calls/meetings per week", 
            ["0", "1-5", "6-15", "16-30", "30+"], selection_mode="single")
    
    # Goals & Motivation
    st.subheader("🎯 Goals & Motivation")
    
    col1, col2 = st.columns(2)
    with col1:
        main_motivation = st.pills("Main Motivation", 
            ["Saving money", "Protecting the environment", "Social responsibility", "Health reasons"], selection_mode="multi")
        biggest_challenge = st.pills("Biggest Challenge", 
            ["Cost", "Convenience", "Not knowing what to do", "Lack of time"], selection_mode="multi")
    
    with col2:
        improvement_area = st.pills("Area you most want to improve", 
            ["Reducing carbon footprint", "Saving money on bills", "Reducing waste", "Eating healthier"], selection_mode="multi")
    
    # Additional Information
    st.subheader("💭 Tell Us More")
    additional_info = st.text_area(
        "In about 100 words, tell me anything else about your lifestyle, " \
        "routines, or challenges you face when trying to be sustainable that wasn't " \
        "covered in the form. What does a typical day look like for you?",
        height=120,
        placeholder="Share any additional insights about your daily routine, " \
        "sustainability goals, or specific challenges you face..."
    )
    
    # Submit button
    submitted = st.form_submit_button("🌟 Complete Profile & Get Analysis")

if submitted:
    # Validate required fields
    if not city or not climate or household_size < 1:
        st.error("⚠️ Please fill in all required fields: City, Climate, and Household Size.")
    else:
        # Prepare user data
        user_data = {
            "user_id": user.id,
            "location": {
                "city": city,
                "climate": climate
            },
            "household": {
                "size": household_size,
                "home_type": home_type,
                "home_size": home_size,
                "ownership": ownership,
                "heating_source": heating_source,
                "air_conditioning": air_conditioning,
                "energy_provider": energy_provider,
                "appliances": appliances,
                "energy_conservation": energy_conservation
            },
            "transportation": {
                "primary_transport": primary_transport,
                "car_type": car_type,
                "vehicle_fuel": vehicle_fuel,
                "commute_distance": commute_distance,
                "rideshare_usage": rideshare_usage,
                "public_transport_usage": public_transport_usage
            },
            "diet": {
                "diet_type": diet_type,
                "meat_frequency": meat_frequency,
                "food_waste": food_waste,
                "shopping_frequency": shopping_frequency
            },
            "consumption": {
                "clothes_shopping": clothes_shopping,
                "new_vs_secondhand": new_vs_secondhand,
                "eco_importance": eco_importance,
                "recycling_habits": recycling_habits,
                "composting": composting,
                "plastic_usage": plastic_usage
            },
            "travel": {
                "flights_per_year": flights_per_year,
                "flight_reason": flight_reason,
                "lifestyle": lifestyle,
                "hobbies": hobbies
            },
            "digital": {
                "ai_queries_daily": ai_queries_daily,
                "image_generation_monthly": image_generation_monthly,
                "video_streaming_daily": video_streaming_daily,
                "cloud_storage_usage": cloud_storage_usage,
                "device_usage": device_usage,
                "online_meetings_weekly": online_meetings_weekly
            },
            "goals": {
                "main_motivation": main_motivation,
                "biggest_challenge": biggest_challenge,
                "improvement_area": improvement_area
            },
            "additional_info": additional_info
        }

        # Save to database
        with st.spinner("💾 Saving your profile..."):
            save_success = save_onboarding_data(user.id, user_data)
        
        if save_success:
            update_onboarding_status(user.id, True)
            st.success("✅ Profile saved successfully!")
            
            # Automatically trigger Agent 2 after onboarding completion
            with st.spinner("🤖 Agent 2 is analyzing your carbon footprint..."):
                agent_success = trigger_agent_workflow(user.id)
                
            if agent_success:
                st.success("🎉 **Carbon analysis complete!** Your dashboard is ready with personalized recommendations.")
                st.balloons()
                
                # Redirect to dashboard
                if st.button("📊 Go to Dashboard", use_container_width=True, type="primary"):
                    st.switch_page("pages/3_dashboard.py")
            else:
                st.error("❌ There was an error running the analysis. Please try again from the dashboard.")
                if st.button("📊 Go to Dashboard Anyway", use_container_width=True):
                    st.switch_page("pages/3_dashboard.py")
        else:
            st.error("❌ Error saving your profile. Please try again.")


