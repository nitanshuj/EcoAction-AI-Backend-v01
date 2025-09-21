"""
Improved Supabase client configuration with proper error handling and validation.
"""
import logging
from typing import Optional
from supabase import Client, create_client
import streamlit as st
from config.settings import get_settings

logger = logging.getLogger(__name__)

# Global client instance
_supabase_client: Optional[Client] = None

@st.cache_resource
def init_supabase() -> Client:
    """
    Initialize and return the Supabase client with proper configuration.

    Returns:
        Client: Configured Supabase client

    Raises:
        ValueError: If required environment variables are missing or invalid
        Exception: If client initialization fails
    """
    global _supabase_client

    if _supabase_client is not None:
        return _supabase_client

    try:
        settings = get_settings()

        # Validate required settings
        if not settings.supabase_url:
            error_msg = "SUPABASE_URL is required but not set"
            st.error(error_msg)
            st.stop()

        if not settings.supabase_anon_key:
            error_msg = "SUPABASE_ANON_KEY is required but not set"
            st.error(error_msg)
            st.stop()

        if settings.supabase_url == "your_supabase_url_here":
            error_msg = "Please set a valid SUPABASE_URL in your .env file"
            st.error(error_msg)
            st.stop()

        if settings.supabase_anon_key == "your_supabase_anon_key_here":
            error_msg = "Please set a valid SUPABASE_ANON_KEY in your .env file"
            st.error(error_msg)
            st.stop()

        # Create client with configuration
        _supabase_client = create_client(
            supabase_url=settings.supabase_url,
            supabase_key=settings.supabase_anon_key,
            options={
                "schema": "public",
                "auto_refresh_token": True,
                "persist_session": True,
                "detect_session_in_url": True,
                "headers": {
                    "X-Client-Info": "ecoaction-ai-backend@1.0.0"
                }
            }
        )

        logger.info("Supabase client initialized successfully")
        return _supabase_client

    except Exception as e:
        error_msg = f"Failed to initialize Supabase client: {str(e)}"
        logger.error(error_msg)
        st.error(error_msg)
        st.stop()

def get_supabase_client() -> Client:
    """
    Get the initialized Supabase client.

    Returns:
        Client: The Supabase client instance
    """
    if _supabase_client is None:
        return init_supabase()
    return _supabase_client

def reset_supabase_client():
    """Reset the global client instance (useful for testing)."""
    global _supabase_client
    _supabase_client = None

if __name__ == "__main__":
    # Check if the connection is successful or not
    try:
        supabase = init_supabase()
        print("Supabase client initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize Supabase client: {str(e)}")
