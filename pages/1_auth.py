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