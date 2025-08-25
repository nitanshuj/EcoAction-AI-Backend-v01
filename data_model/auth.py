# Handles login, signup, and session management
# utils/auth.py - backend auth helpers (no Streamlit)
from supabase import Client
from .supabase_client import init_supabase

def get_supabase() -> Client:
    """Initialize and return the Supabase client."""
    return init_supabase()

def is_authenticated() -> bool:
    """Placeholder for backend session check (handled in frontend or API)."""
    return False

def login(email: str, password: str) -> tuple[bool, str]:
    """
    Attempt to log in a user with email and password.
    
    Args:
        email (str): User's email address
        password (str): User's password
        
    Returns:
        tuple[bool, str]: (success status, message)
    """
    try:
        supabase = get_supabase()
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        if response.user:
            return True, "Login successful"
        else:
            return False, "Login failed. Please check your credentials."
            
    except Exception as e:
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            return False, "Invalid email or password."
        else:
            return False, f"An error occurred during login: {error_msg}"

def sign_up(email: str, password: str, first_name: str, last_name: str, age: int) -> tuple[bool, str]:
    """
    Create a new user account with profile information.
    
    Args:
        email (str): User's email address
        password (str): User's password
        first_name (str): User's first name
        last_name (str): User's last name
        age (int): User's age
        country (str): User's country (Removed)
        
    Returns:
        tuple[bool, str]: (success status, message)
    """
    try:
        supabase = get_supabase()
        
        # Sign up the user with Supabase Auth
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if response.user:
            # The user record is automatically created by the trigger
            # We just need to update it with additional profile information
            try:
                # Update user with additional profile information
                profile_response = supabase.table("users").update({
                    "first_name": first_name,
                    "last_name": last_name,
                    # "country": country,
                    "onboarding_status": False
                }).eq("id", response.user.id).execute()
                
                if profile_response.data:
                    return True, "Account created successfully! You can now use the app."
                else:
                    # If profile update fails, still consider signup successful
                    return True, "Account created successfully! You can now use the app."
            except Exception as db_error:
                # Even if profile update fails, the user is created, so return success
                return True, "Account created successfully! You can now use the app."
        else:
            return False, "Account creation failed."

    except Exception as e:
        error_msg = str(e)
        if "User already registered" in error_msg:
            return False, "An account with this email already exists."
        elif "Password should be at least" in error_msg:
            return False, "Password is too weak. Please choose a stronger password."
        elif "duplicate key value violates unique constraint" in error_msg:
            return False, "An account with this email already exists."
        else:
            return False, f"An error occurred during sign up: {error_msg}"

def get_current_user():
    """
    Get the current authenticated user.
    
    Returns:
        User object if authenticated, None otherwise
    """
    try:
        # Try to get user from Supabase session
        supabase = get_supabase()
        response = supabase.auth.get_user()
        
        if response.user:
            return response.user
        else:
            return None
            
    except Exception:
        # If any error occurs (like expired token), return None
        return None

def get_user_profile(user_id: str = None):
    """
    Get user profile data from the users table.
    
    Args:
        user_id (str): User UUID, if not provided will use current user
        
    Returns:
        dict: User profile data or None if not found
    """
    try:
        supabase = get_supabase()
        
        if not user_id:
            # Get current user ID
            current_user = get_current_user()
            if not current_user:
                return None
            user_id = current_user.id
        
        # Get user profile from users table
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0]
        else:
            return None
            
    except Exception:
        return None

def logout():
    """
    Log out the current user and clear session data.
    """
    supabase = get_supabase()
    supabase.auth.sign_out()

def clear_session():
    """No-op for backend-only context."""
    return

def require_auth():
    """
    Check if user is authenticated in Streamlit session.
    Redirect to auth page if not authenticated.
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    import streamlit as st
    
    # Check if user is in session state
    if 'user' in st.session_state and st.session_state.user is not None:
        return True
    
    # Try to get user from backend session
    user = get_current_user()
    if user:
        st.session_state.user = user
        return True
    
    # Not authenticated - show blank page instead of error
    st.info("Please sign in to access this page.")
    if st.button("Go to Sign In"):
        st.switch_page("pages/1_auth.py")
    return False