# app.py
# =================================
import streamlit as st
import sys
import os


# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_model.auth import get_current_user, is_authenticated

# Page configuration - this is the first command that must be run
st.set_page_config(
    page_title="EcoAction AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# from chromadb.config import Settings
# import chromadb

# client = chromadb.Client(
#     Settings(
#       chroma_db_impl="duckdb+parquet",
#       persist_directory=".chromadb"  # or wherever you want to persist
#     )
# )

def main():
    """Main application entry point with front page or routing"""
    
    # Initialize essential session state variables if they don't exist
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    
    # Get the current user (checks session state first, then Supabase)
    user = get_current_user()
    
    # If user is authenticated, redirect to dashboard
    if user:
        st.switch_page("pages/3_dashboard.py")
        return
    
    # Show front page for non-authenticated users
    show_front_page()

def show_front_page():
    """Display the front page with cover image and auth buttons"""
    
    # Custom CSS for front page styling
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
        max-width: 1200px !important;
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
    
    /* Cover image container */
    .cover-container {
        text-align: center;
        margin-bottom: 3rem;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(100, 149, 237, 0.2);
    }
    
    .cover-image {
        width: 100%;
        height: auto;
        object-fit: contain;
        border-radius: 20px;
        max-height: 500px;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center !important;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.9);
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(100, 149, 237, 0.15);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6495ED 0%, #4169E1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        line-height: 1.2;
        text-align: center !important;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #2d3748 !important;
        margin-bottom: 2rem;
        line-height: 1.6;
        max-width: 800px;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        display: block !important;
    }
    
    /* Override any global text alignment */
    .hero-section * {
        text-align: center !important;
    }
    
    /* Button styling */
    .auth-buttons {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 3rem;
        flex-wrap: wrap;
    }
    
    .stButton > button {
        background: #2c3e50 !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 16px 32px !important;
        font-weight: 600 !important;
        font-size: 18px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(44, 62, 80, 0.3) !important;
        min-width: 200px !important;
        height: 60px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 8px 25px rgba(44, 62, 80, 0.4) !important;
        background: #34495e !important;
        color: white !important;
    }
    
    /* Features section */
    .features-section {
        margin: 4rem 0;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(100, 149, 237, 0.1);
    }
    
    .features-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 3rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 16px rgba(100, 149, 237, 0.1);
        text-align: center;
        border: 2px solid #e6f3ff;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(100, 149, 237, 0.2);
        border-color: #6495ED;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 1rem;
    }
    
    .feature-desc {
        color: #2d3748;
        line-height: 1.6;
    }
    
    /* Global text override - but preserve centering for hero section */
    * {
        color: #2d3748 !important;
    }
    
    /* Override global alignment for hero section */
    .hero-section, .hero-section *, .hero-section p, .hero-section h1 {
        text-align: center !important;
    }
    
    /* Bright sidebar styling - light blue background with dark text */
    .stSidebar {
        background: linear-gradient(135deg, #e6f3ff 0%, #b3d9ff 100%) !important;
    }
    
    .stSidebar *, .stSidebar p, .stSidebar span, .stSidebar div, .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar label {
        color: #2d3748 !important;
        font-weight: 500 !important;
    }
    
    /* Sidebar navigation links - dark text on bright background */
    .stSidebar a, .stSidebar [data-testid="stPageLink"], .stSidebar [data-testid="stPageLink"] * {
        color: #2d3748 !important;
        text-decoration: none !important;
    }
    
    .stSidebar a:hover, .stSidebar [data-testid="stPageLink"]:hover {
        background: rgba(100, 149, 237, 0.1) !important;
        border-radius: 8px !important;
    }
    
    /* Only buttons get white text */
    .stButton > button, .stButton > button * {
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Cover image section
    try:
        st.markdown("""
        <div class="cover-container">
            <img src="data:image/jpeg;base64,{}" class="cover-image" alt="EcoAction AI Cover">
        </div>
        """.format(get_image_base64("images/cover_image_1.jpg")), unsafe_allow_html=True)
    except:
        # Fallback if image not found
        st.markdown("""
        <div class="cover-container" style="background: linear-gradient(135deg, #6495ED 0%, #4169E1 100%); height: 400px; display: flex; align-items: center; justify-content: center;">
            <h1 style="color: white; font-size: 4rem; margin: 0;">🌱</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Hero section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Welcome to EcoAction AI</h1>
        <p class="hero-subtitle">
            Transform your lifestyle with AI-powered sustainability insights. Track your environmental impact, get personalized recommendations, and join the movement towards a greener future.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Auth buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_col1, auth_col2 = st.columns(2)
        
        with auth_col1:
            if st.button("🔐 Sign In", key="signin_btn", use_container_width=True):
                st.switch_page("pages/1_auth.py")
        
        with auth_col2:
            if st.button("🌍 Sign Up", key="signup_btn", use_container_width=True):
                st.switch_page("pages/1_auth.py")
    
    # Features section
    st.markdown("""
    <div class="features-section">
        <h2 class="features-title">Why Choose EcoAction AI?</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🌱</div>
                <h3 class="feature-title">Smart Tracking</h3>
                <p class="feature-desc">AI-powered analysis of your daily activities to calculate environmental impact with precision.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Personalized Insights</h3>
                <p class="feature-desc">Get tailored recommendations based on your lifestyle and sustainability goals.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3 class="feature-title">Goal Setting</h3>
                <p class="feature-desc">Set and track meaningful environmental goals with AI guidance and progress monitoring.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_image_base64(image_path):
    """Convert image to base64 for embedding"""
    import base64
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return ""

# Run the main function
if __name__ == "__main__":
    main()