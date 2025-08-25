# pages/1_auth.py
import streamlit as st
import sys
import os

# Add the parent directory to the path so we can import from utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_model.auth import login, sign_up, get_current_user, logout, get_user_profile
from data_model.database import check_onboarding_status

# Check if user is already logged in
current_user = get_current_user()
if current_user:
    # Get user profile for display name
    user_profile = get_user_profile(current_user.id)
    display_name = current_user.email
    if user_profile and user_profile.get('first_name'):
        display_name = f"{user_profile['first_name']}"
    
    # Check onboarding status
    onboarding_completed = check_onboarding_status(current_user.id)
    
    # User is already authenticated, show logout option
    st.markdown(f"""
    <div style="background-color: #6495ED; color: white; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; text-align: center;">
        <h3 style="color: white; margin: 0;">👋 You are already logged in as <strong>{display_name}</strong></h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if onboarding_completed:
            # User has completed onboarding, show dashboard button
            if st.button("📊 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/3_dashboard.py")
        else:
            st.info("💡 It looks like you have not completed the onboarding process!!")
            # User hasn't completed onboarding, show onboarding button
            if st.button("🌟 Complete Onboarding", use_container_width=True):
                st.switch_page("pages/2_onboarding.py")
            # User has completed onboarding, show dashboard button
            if st.button("📊 Go to Dashboard", use_container_width=True):
                st.switch_page("pages/3_dashboard.py")
            
            
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.success("✅ You have been logged out successfully!")
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()  # Don't show login/signup forms if already logged in

# Page configuration
st.set_page_config(
    page_title="EcoAction AI - Login",
    page_icon="🔐",
    layout="centered"
)

# Auth page specific CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    /* Remove default padding and set background */
    .stApp {
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 50%, #ffffff 100%) !important;
        font-family: 'Poppins', sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 800px !important;
    }
    
    /* Hide Streamlit menu and footer but keep deploy button */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Show deploy button */
    .stDeployButton {
        visibility: visible !important;
        display: block !important;
    }
    
    [data-testid="stToolbar"] {
        visibility: visible !important;
        display: block !important;
    }
    
    /* Global text styling */
    * {
        color: #2d3748 !important;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(100, 149, 237, 0.15);
    }
    
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6495ED 0%, #4169E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #2d3748 !important;
        margin-bottom: 0;
        line-height: 1.6;
    }
    
    /* Auth page tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        color: #2d3748 !important;
        font-weight: 600;
        padding: 0 30px;
        border: 2px solid #e6f3ff;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6495ED 0%, #4169E1 100%);
        color: white !important;
        border-color: #4169E1;
        box-shadow: 0 4px 16px rgba(100, 149, 237, 0.3);
    }
    
    /* Form styling */
    .stForm {
        background: rgba(255, 255, 255, 0.95);
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(100, 149, 237, 0.15);
        border: 1px solid #e6f3ff;
        margin: 1rem 0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #6495ED !important;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #6495ED;
        text-align: left;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border: 2px solid #e6f3ff !important;
        border-radius: 12px !important;
        padding: 0.75rem !important;
        background-color: rgba(240, 248, 255, 0.5) !important;
        color: #2d3748 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #6495ED !important;
        background-color: white !important;
        box-shadow: 0 0 0 3px rgba(100, 149, 237, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #6495ED 0%, #4169E1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(100, 149, 237, 0.3) !important;
        min-height: 48px !important;
    }
    
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #4169E1 0%, #6495ED 100%) !important;
        box-shadow: 0 6px 20px rgba(100, 149, 237, 0.4) !important;
        transform: translateY(-2px) !important;
        color: white !important;
    }
    
    /* Alert styling */
    [data-testid="stAlert"] {
        background-color: rgba(100, 149, 237, 0.1);
        border: 1px solid #6495ED;
        border-radius: 12px;
        color: #2d3748 !important;
    }
    
    /* Success alert */
    [data-testid="stAlert"][data-baseweb="notification"] {
        background-color: rgba(76, 175, 80, 0.1);
        border-color: #4CAF50;
    }
    
    /* Error alert */
    .stAlert[data-baseweb="notification"] {
        border-radius: 12px;
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    
    p, span, label {
        color: #2d3748 !important;
    }
    
    /* Bright sidebar styling */
    .stSidebar {
        background: linear-gradient(135deg, #e6f3ff 0%, #b3d9ff 100%) !important;
    }
    
    .stSidebar *, .stSidebar p, .stSidebar span, .stSidebar div, .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar label {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
</style>
""", unsafe_allow_html=True)

# Add auth page container class
# st.markdown('<div class="auth-page-container">', unsafe_allow_html=True)

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🌱 EcoAction </h1>
        <p class="subtitle">Your Personalized Climate Behavior Coach</p>
    </div>
""", unsafe_allow_html=True)

# Create tabs for Login and Sign Up
tab1, tab2 = st.tabs(["🚀 **Login**", "🌍 **Sign Up**"])

with tab1:
    st.markdown("### Welcome Back!")
    st.markdown("Sign in to continue your sustainability journey")
    
    with st.form("login_form"):
        email = st.text_input(
            "Email Address", 
            placeholder="your.email@example.com"
        )
        password = st.text_input(
            "Password", 
            type="password", 
            placeholder="Enter your password"
        )
        
        submitted = st.form_submit_button("Sign In", use_container_width=True)
        
        if submitted:
            if not email or not password:
                st.error("Please fill in all fields")
            else:
                with st.spinner("Signing you in..."):
                    success, message = login(email, password)
                    if success:
                        st.success("Login successful!")
                        # Store user in session state
                        from data_model.auth import get_current_user
                        user = get_current_user()
                        if user:
                            st.session_state.user = user
                        # Redirect to onboarding page
                        st.switch_page("pages/2_onboarding.py")
                    else:
                        st.error(f"{message}")

with tab2:
    st.markdown("### Join the Movement!")
    st.markdown("Create your account and start making a difference")
    
    with st.form("signup_form"):
        # Personal Information
        st.markdown('<div class="section-header">Personal Information</div>', 
                    unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name", placeholder="e.g., John")
        with col2:
            last_name = st.text_input("Last Name", placeholder="e.g., Doe")
        
        col3, col4 = st.columns(2)
        with col3:
            age = st.number_input("Age", min_value=13, max_value=120, value=25)
        # with col4:            
        #     country = st.text_input("Country", placeholder="e.g., United States")

        # Account Details
        st.markdown('<div class="section-header">Account Details</div>', unsafe_allow_html=True)
        
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        
        col5, col6 = st.columns(2)
        with col5:
            password = st.text_input("Password", type="password", placeholder="Create a password")
        with col6:
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        # Password strength check
        if password:
            if len(password) < 6:
                st.warning("Password should be at least 6 characters")
            elif not any(char.isdigit() for char in password):
                st.warning("Consider adding numbers for strength")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)
        
        if submitted:
            if not all([first_name, last_name, email, password, confirm_password]):
                st.error("Please fill in all fields")
            elif password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            else:
                with st.spinner("Creating your account..."):
                    success, message = sign_up(
                        email=email.strip(), 
                        password=password,
                        first_name=first_name.strip(),
                        last_name=last_name.strip(),
                        age=age,
                       #  country=country
                    )
                    if success:
                        st.success("Account created successfully!")
                        st.info("You can now sign in with your credentials")
                    else:
                        st.error(f"{message}")

# st.markdown('</div>', unsafe_allow_html=True)

# # Footer
# st.markdown("---")
# st.markdown(
#     "<div style='text-align: center; color: #222222; font-weight: 500;'>"
#     "By signing up, you agree to our Terms of Service and Privacy Policy<br>"
#     "Need help? Contact us at support@ecoaction.ai"
#     "</div>", 
#     unsafe_allow_html=True
# )