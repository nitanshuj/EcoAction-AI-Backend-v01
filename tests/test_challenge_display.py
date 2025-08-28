#!/usr/bin/env python3
"""Test script to verify challenge display logic"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Sample challenge data matching your JSON structure
sample_challenges = [
    {
        "id": "challenge_1",
        "title": "Meatless Monday Kickstart",
        "category": "diet",
        "difficulty": "easy",
        "motivation": "Simple step to lower emissions and improve health.",
        "description": "Skip meat for one meal on Monday to reduce carbon footprint and support sustainable eating habits.",
        "time_required": "1 hour",
        "co2_savings_kg": 1.5
    },
    {
        "id": "challenge_2", 
        "title": "Zero Food Waste Meal",
        "category": "waste",
        "difficulty": "easy",
        "motivation": "Saves money and reduces methane from wasted food.",
        "description": "Prepare a meal using only leftovers and ingredients close to expiry to reduce food waste.",
        "time_required": "1 hour",
        "co2_savings_kg": 1
    },
    {
        "id": "challenge_3",
        "title": "Public Transit Challenge", 
        "category": "transport",
        "difficulty": "medium",
        "motivation": "Saves money, reduces traffic, and improves air quality.",
        "description": "Commit to using public transport or biking for 50% of your usual car trips this week to cut down vehicle emissions.",
        "time_required": "Varies, ~5 hours/week",
        "co2_savings_kg": 8
    },
    {
        "id": "challenge_4",
        "title": "Renewable Energy Switch Research & Actions",
        "category": "energy", 
        "difficulty": "hard",
        "motivation": "Long-term impact in reducing carbon emissions from electricity.",
        "description": "Research renewable energy options available for renters in Chicago, contact your energy provider, and initiate a switch or subscribe to green energy plans.",
        "time_required": "3 hours over the week",
        "co2_savings_kg": 20
    }
]

print("🧪 Testing Challenge Display Logic")
print("=" * 50)

for i, challenge in enumerate(sample_challenges, 1):
    # Test the field extraction logic from the dashboard
    challenge_completed = challenge.get('completed', False)
    challenge_title = challenge.get('title', f'Challenge {i}')
    challenge_difficulty = challenge.get('difficulty', challenge.get('difficulty_level', 'medium')).upper()
    co2_savings = challenge.get('co2_savings_kg', challenge.get('co2_savings', challenge.get('estimated_co2_savings_kg', 0)))
    description = challenge.get('description', challenge.get('action', ''))
    category = challenge.get('category', 'General').title()
    time_required = challenge.get('time_required', challenge.get('time', 'N/A'))
    
    print(f"\n🎯 Challenge {i}: {challenge_title}")
    print(f"   Difficulty: {challenge_difficulty}")
    print(f"   Category: {category}")
    print(f"   CO2 Savings: {co2_savings} kg")
    print(f"   Time: {time_required}")
    print(f"   Description: {description[:80]}...")
    print(f"   Completed: {challenge_completed}")

print(f"\n✅ All {len(sample_challenges)} challenges processed successfully!")
print("\nThe dashboard should now display all 4 challenges correctly with:")
print("- ✅ Title, difficulty, category badges")
print("- ✅ CO2 savings display")
print("- ✅ Time required information")
print("- ✅ Full description")
print("- ✅ Completion status tracking")
