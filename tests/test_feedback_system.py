# test_feedback_system.py
"""
Test script for the Two-Tiered Memory Feedback System
"""

import sys
import os

# Add the parent directory to Python path so we can import project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_model.database import (
    save_feedback_and_process,
    get_user_feedback_history,
    get_current_week_feedback,
    process_feedback_text
)
from agent.crew import run_feedback_aware_planning_workflow

def test_feedback_processing():
    """Test the feedback text processing function"""
    print("🧪 Testing Feedback Text Processing...")
    
    test_feedbacks = [
        "These transport challenges are impossible for me, I don't own a car. Give me easier stuff I can do at home.",
        "I want more challenges that help me save money on bills.",
        "These are too hard, make them easier please",
        "I love the diet challenges but want more variety",
        "Focus on daily tasks only, I don't have time for weekly projects"
    ]
    
    for i, feedback in enumerate(test_feedbacks, 1):
        print(f"\n--- Test {i} ---")
        print(f"Raw feedback: {feedback}")
        
        try:
            summary = process_feedback_text(feedback)
            print(f"Processed summary: {summary}")
        except Exception as e:
            print(f"Error processing feedback: {str(e)}")

def test_feedback_workflow():
    """Test the complete feedback workflow with a test user"""
    print("\n🧪 Testing Complete Feedback Workflow...")
    
    # Use a test user ID (replace with a real one from your database)
    test_user_id = "test-user-123"  # Replace this with a real user ID from your database
    
    print(f"Using test user ID: {test_user_id}")
    
    # Test saving feedback
    test_feedback = "I want easier challenges that help save money and can be done at home"
    
    print(f"\n1. Saving feedback: {test_feedback}")
    try:
        success = save_feedback_and_process(test_user_id, test_feedback)
        print(f"Feedback saved: {success}")
    except Exception as e:
        print(f"Error saving feedback: {str(e)}")
        return
    
    # Test retrieving feedback history
    print("\n2. Retrieving feedback history...")
    try:
        history = get_user_feedback_history(test_user_id)
        print(f"Feedback history entries: {len(history)}")
        for entry in history:
            print(f"  - {entry['summary']}")
    except Exception as e:
        print(f"Error retrieving feedback history: {str(e)}")
    
    # Test getting current week feedback
    print("\n3. Getting current week feedback...")
    try:
        current = get_current_week_feedback(test_user_id)
        if current:
            print(f"Current week feedback: {current.get('feedback_summary', 'No summary')}")
        else:
            print("No current week feedback found")
    except Exception as e:
        print(f"Error getting current week feedback: {str(e)}")

def test_challenges_metadata():
    """Test loading and analyzing the challenges metadata"""
    print("\n🧪 Testing Challenges Metadata...")
    
    try:
        import json
        # Get the correct path to the data directory from the project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        challenges_path = os.path.join(project_root, 'data', 'challenges_metadata.json')
        
        with open(challenges_path, 'r') as f:
            challenges = json.load(f)
        
        print(f"Total challenges loaded: {len(challenges)}")
        
        # Analyze by category
        categories = {}
        difficulties = {}
        
        for challenge in challenges:
            if isinstance(challenge, dict) and 'category' in challenge:
                cat = challenge.get('category', 'Unknown')
                diff = challenge.get('difficulty', 'Unknown')
                
                categories[cat] = categories.get(cat, 0) + 1
                difficulties[diff] = difficulties.get(diff, 0) + 1
        
        print(f"\nCategories: {categories}")
        print(f"Difficulties: {difficulties}")
        
        # Find challenges with money/savings tags
        money_challenges = []
        for challenge in challenges:
            if isinstance(challenge, dict) and 'impact_vector' in challenge:
                impact_vector = challenge.get('impact_vector', [])
                if any(keyword in str(impact_vector).lower() for keyword in ['money', 'savings', 'bills']):
                    money_challenges.append(challenge.get('description', 'No description'))
        
        print(f"\nMoney-saving challenges found: {len(money_challenges)}")
        for i, desc in enumerate(money_challenges[:3], 1):
            print(f"  {i}. {desc}")
            
    except Exception as e:
        print(f"Error analyzing challenges metadata: {str(e)}")

if __name__ == "__main__":
    print("🚀 EcoAction AI - Feedback System Test")
    print("=" * 50)
    
    # Test 1: Feedback text processing
    test_feedback_processing()
    
    # Test 2: Challenges metadata
    test_challenges_metadata()
    
    # Test 3: Complete workflow (requires valid user ID)
    print("\n" + "=" * 50)
    print("📝 To test the complete feedback workflow:")
    print("1. Find a valid user ID from your database")
    print("2. Replace 'test-user-123' in test_feedback_workflow()")
    print("3. Ensure the user has completed Agent 1 and Agent 2")
    print("4. Uncomment the line below and run again")
    
    # Uncomment the line below and provide a real user ID to test
    # test_feedback_workflow()
    
    print("\n✅ Basic tests completed!")
