<p align="center">
   <img src="images/cover_image_2.jpg" alt="EcoAction AI Cover" style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.15); margin-bottom: 24px;" />
</p>

A personalized climate behavior coaching application built with Streamlit and Supabase.

### Project Structure

```
├── app.py
|
├── .env
|
├── pyproject.toml
|
├── .venv/
|
├── images/
|   ├── cover_image_1.jpg
|   └── cover_image_2.jpg
| 
├── research_notebooks/
|
├── data/
│   └── actions_db.csv
|
├── images/
│   ├── cover_image_1.jpg
│   └── cover_image_2.jpg
|
├── pages/
│   ├── 1_auth.py
│   ├── 2_onboarding.py
│   ├── 3_dashboard.py
|
├── prompts/
│   ├── onboarding.py
│   ├── recommendations.py
│   └── coaching.py
|
└── utils/
    ├── auth.py
    ├── database.py
    ├── llm_client.py
    ├── recommender.py
    ├── supabase_client.py
    ├── time_manager.py
    ├── voice_processor.py
    └── __init__.py
```

### Features

- **Authentication**: Secure user authentication with Supabase Auth
- **Dashboard**: Personalized dashboard with action recommendations
- **Progress Tracking**: Track CO2 savings and environmental impact
- **Weekly Reports**: Detailed weekly sustainability reports
- **Community Challenges**: Participate in community sustainability challenges

### Setup and Running the Project on macOS

#### 1. Prerequisites

First, ensure you have Python 3.10+ and `uv` (a Python package manager) installed.

```sh
# Install Python 3.10+ via Homebrew if you don't have it
brew install python

# Install uv
pip install uv
```

#### 2. Project Setup

Navigate to your project directory in the terminal and create a virtual environment, then install the required dependencies.

```sh
# Create a virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from pyproject.toml
uv sync
```

#### 3. Configure Environment Variables

Your application requires API keys for Supabase and an AI service. Create a `.env` file in the root of your project directory.

```
SUPABASE_URL="your_supabase_url_here"
SUPABASE_KEY="your_supabase_anon_key_here"
AI_ML_API_KEY="your_aiml_api_key_here"
```

You will need to get these credentials from your Supabase project settings and the AI/ML API provider you are using.

#### 4. Set Up the Database

The application uses Supabase for the backend. You will need to:
1.  Create a project on [Supabase](https://supabase.com/).
2.  Use the SQL scripts in your `data_model` directory, like `data_model/sql_scripts_1.sql`, to set up the necessary tables (e.g., `users`) in the Supabase SQL Editor.

#### 5. Run the Application

Once the setup is complete, you can run the Streamlit application.

```sh
streamlit run app.py
```

This will start the web server, and you can access the application in your browser at the local URL provided in the terminal output.
