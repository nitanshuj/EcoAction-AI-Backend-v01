# Initializes the Supabase connection
import os
from dotenv import load_dotenv
load_dotenv()
from supabase import create_client, Client
import streamlit as st

@st.cache_resource
def init_supabase():
    """Initialize Supabase client with environment variables"""
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_ANON_KEY")
    
    if not url or not key:
        st.error("Missing Supabase credentials. Please check your .env file.")
        st.stop()
    
    try:
        supabase: Client = create_client(url, key)
        return supabase
    except Exception as e:
        st.error(f"Failed to initialize Supabase client: {str(e)}")
        st.stop()


if __name__ == "__main__":
    # Check if the connection is successful or not
    supabase = init_supabase()
    if supabase:
        print("Supabase client initialized successfully.")
    else:
        print("Failed to initialize Supabase client.")
