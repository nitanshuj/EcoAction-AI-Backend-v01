# data_model/data_merge_json.py
"""
JSON merging functions for combining Agent 1 (Profiler) and Agent 2 (Analyst) outputs
into a single comprehensive user profile with scores.
"""

import json
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field, ValidationError
from datetime import datetime

# Pydantic model for the merged profile validation
class MergedUserProfile(BaseModel):
    """Complete user profile with demographics, lifestyle, and carbon analysis"""
    
    # From Agent 1 (Enhanced Profile)
    narrative_text: str = Field(..., description="User lifestyle narrative")
    demographics: Dict[str, Any] = Field(..., description="User demographic information")
    lifestyle_habits: Dict[str, Any] = Field(..., description="User lifestyle and habits")
    consumption_patterns: Dict[str, Any] = Field(..., description="User consumption patterns")
    psychographic_insights: Dict[str, Any] = Field(..., description="User motivations and barriers")
    key_levers: list = Field(..., description="Key carbon reduction opportunities")
    
    # From Agent 2 (Score Agent)
    total_carbon_footprint_kg: float = Field(..., description="Total annual footprint in kg")
    total_carbon_footprint_tonnes: float = Field(..., description="Total annual footprint in tonnes")
    category_breakdown: Dict[str, float] = Field(..., description="Emissions by category")
    sustainability_score: float = Field(..., description="Overall sustainability score")
    score_category: str = Field(..., description="Score category description")
    regional_comparison: Dict[str, Any] = Field(..., description="Regional comparison data")
    key_lever_validations: list = Field(..., description="Validated reduction opportunities")
    psychographic_insights_analyst: Optional[list] = Field(default=[], description="Analyst insights")
    top_impact_categories: list = Field(..., description="Highest impact emission categories")
    priority_reduction_areas: list = Field(..., description="Priority areas for reduction")
    fun_comparison_facts: list = Field(..., description="Engaging comparison facts")
    
    # Metadata
    calculation_method: str = Field(..., description="How calculations were performed")
    data_confidence: str = Field(..., description="Confidence level of data")
    
    class Config:
        extra = "allow"  # Allow additional fields


def merge_agent_outputs(agent1_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merge Agent 1 (Enhanced Profile) and Agent 2 (Score Agent) outputs into a single profile.
    
    Args:
        agent1_output (dict): Output from Agent 1 (Profiler) - enhanced profile
        agent2_output (dict): Output from Agent 2 (Analyst) - carbon analysis with scores
    
    Returns:
        dict: Merged profile with all relevant data
    
    Raises:
        ValueError: If required fields are missing or validation fails
    """
    
    if not agent1_output or not agent2_output:
        raise ValueError("Both agent outputs are required for merging")
    
    # Extract key components from Agent 1 (Enhanced Profile)
    merged_profile = {
        # Core profile data from Agent 1
        "narrative_text": agent1_output.get("narrative_text", ""),
        "demographics": agent1_output.get("demographics", {}),
        "lifestyle_habits": agent1_output.get("lifestyle_habits", {}),
        "consumption_patterns": agent1_output.get("consumption_patterns", {}),
        "psychographic_insights": agent1_output.get("psychographic_insights", {}),
        "key_levers": agent1_output.get("key_levers", []),
        
        # Carbon analysis data from Agent 2
        "total_carbon_footprint_kg": agent2_output.get("total_carbon_footprint_kg", 0.0),
        "total_carbon_footprint_tonnes": agent2_output.get("total_carbon_footprint_tonnes", 0.0),
        "category_breakdown": agent2_output.get("category_breakdown", {}),
        "sustainability_score": agent2_output.get("sustainability_score", 0.0),
        "score_category": agent2_output.get("score_category", "unknown"),
        "regional_comparison": agent2_output.get("regional_comparison", {}),
        "key_lever_validations": agent2_output.get("key_lever_validations", []),
        "top_impact_categories": agent2_output.get("top_impact_categories", []),
        "priority_reduction_areas": agent2_output.get("priority_reduction_areas", []),
        "fun_comparison_facts": agent2_output.get("fun_comparison_facts", []),
        
        # Metadata from Agent 2
        "calculation_method": agent2_output.get("calculation_method", "Standard emission factors applied"),
        "data_confidence": agent2_output.get("data_confidence", "medium"),
    }
    
    # Add psychographic insights from Agent 2 if available (different from Agent 1's insights)
    if "psychographic_insights" in agent2_output and agent2_output["psychographic_insights"]:
        merged_profile["psychographic_insights_analyst"] = agent2_output["psychographic_insights"]
    
    return merged_profile


def validate_merged_profile(merged_data: Dict[str, Any]) -> MergedUserProfile:
    """
    Validate the merged profile data using Pydantic.
    
    Args:
        merged_data (dict): The merged profile data
    
    Returns:
        MergedUserProfile: Validated profile object
    
    Raises:
        ValidationError: If validation fails
    """
    try:
        validated_profile = MergedUserProfile.model_validate(merged_data)
        return validated_profile
    except ValidationError as e:
        raise ValueError(f"Profile validation failed: {str(e)}")


def create_complete_profile_with_scores(agent1_output: Dict[str, Any], agent2_output: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to create a complete user profile by merging Agent 1 and Agent 2 outputs.
    Includes validation and error handling.
    
    Args:
        agent1_output (dict): Agent 1 (Profiler) enhanced profile output
        agent2_output (dict): Agent 2 (Analyst) carbon analysis output
    
    Returns:
        dict: Complete validated user profile with scores
    
    Raises:
        ValueError: If merging or validation fails
    """
    try:
        # Step 1: Merge the outputs
        merged_profile = merge_agent_outputs(agent1_output, agent2_output)
        
        # Step 2: Validate with Pydantic
        validated_profile = validate_merged_profile(merged_profile)
        
        # Step 3: Convert back to dict for database storage
        complete_profile = validated_profile.model_dump()
        
        # Step 4: Add metadata
        complete_profile["profile_created_at"] = datetime.now().isoformat()
        complete_profile["profile_version"] = "1.0"
        complete_profile["agents_used"] = ["profiler", "analyst"]
        
        return complete_profile
        
    except Exception as e:
        raise ValueError(f"Failed to create complete profile: {str(e)}")


def save_complete_profile_to_users_table(user_id: str, complete_profile: Dict[str, Any]) -> bool:
    """
    Save the complete profile with scores to the users table in the complete_profile_w_scores column.
    
    Args:
        user_id (str): User's UUID
        complete_profile (dict): Complete validated profile with scores
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from .supabase_client import init_supabase
        
        supabase = init_supabase()
        
        # Update the users table with the complete profile
        response = supabase.table('users').update({
            'complete_profile_w_scores': complete_profile,
            'last_active_at': datetime.now().isoformat()
        }).eq('id', user_id).execute()
        
        if response.data:
            print(f"✅ Complete profile saved to users table for user {user_id}")
            return True
        else:
            print(f"❌ Failed to save complete profile for user {user_id}")
            return False
            
    except Exception as e:
        print(f"❌ Error saving complete profile to users table: {str(e)}")
        return False


def get_complete_profile_from_users_table(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve the complete profile with scores from the users table.
    
    Args:
        user_id (str): User's UUID
    
    Returns:
        dict or None: Complete profile data or None if not found
    """
    try:
        from .supabase_client import init_supabase
        
        supabase = init_supabase()
        
        response = supabase.table('users').select('complete_profile_w_scores').eq('id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            return response.data[0].get('complete_profile_w_scores')
        
        return None
        
    except Exception as e:
        print(f"❌ Error retrieving complete profile from users table: {str(e)}")
        return None


def get_agent1_data_from_database(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get Agent 1 (Profiler) data from user_profiles.onboarding_final column.
    
    Args:
        user_id (str): User's UUID
    
    Returns:
        dict or None: Agent 1 data or None if not found
    """
    try:
        from .supabase_client import init_supabase
        
        supabase = init_supabase()
        
        # Get Agent 1 data from user_profiles table
        response = supabase.table('user_profiles').select('onboarding_final').eq('user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            onboarding_final = response.data[0].get('onboarding_final')
            if onboarding_final:
                print(f"✅ Found Agent 1 data in user_profiles.onboarding_final for user {user_id}")
                return onboarding_final
        
        print(f"❌ No Agent 1 data found in user_profiles.onboarding_final for user {user_id}")
        return None
        
    except Exception as e:
        print(f"❌ Error retrieving Agent 1 data from database: {str(e)}")
        return None


def get_agent2_data_from_database(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Get Agent 2 (Analyst) data from user_scores.scores column.
    
    Args:
        user_id (str): User's UUID
    
    Returns:
        dict or None: Agent 2 data or None if not found
    """
    try:
        from .supabase_client import init_supabase
        
        supabase = init_supabase()
        
        # Get Agent 2 data from user_scores table
        response = supabase.table('user_scores').select('scores').eq('user_id', user_id).execute()
        
        if response.data and len(response.data) > 0:
            scores = response.data[0].get('scores')
            if scores:
                print(f"✅ Found Agent 2 data in user_scores.scores for user {user_id}")
                return scores
        
        print(f"❌ No Agent 2 data found in user_scores.scores for user {user_id}")
        return None
        
    except Exception as e:
        print(f"❌ Error retrieving Agent 2 data from database: {str(e)}")
        return None


def merge_json(user_id: str) -> bool:
    """
    Complete workflow function that:
    1. Gets Agent 1 data from user_profiles.onboarding_final
    2. Gets Agent 2 data from user_scores.scores  
    3. Merges and validates the data
    4. Saves to users.complete_profile_w_scores
    
    Args:
        user_id (str): User's UUID
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        print(f"🔄 Starting complete JSON merge workflow for user {user_id}")
        
        # Step 1: Get Agent 1 data from database
        agent1_data = get_agent1_data_from_database(user_id)
        if not agent1_data:
            print("❌ Cannot proceed: Agent 1 data not found")
            return False
        
        # Step 2: Get Agent 2 data from database  
        agent2_data = get_agent2_data_from_database(user_id)
        if not agent2_data:
            print("❌ Cannot proceed: Agent 2 data not found")
            return False
        
        # Step 3: Check if complete profile already exists to avoid overwriting
        existing_profile = get_complete_profile_from_users_table(user_id)
        if existing_profile:
            print(f"⚠️ Complete profile already exists for user {user_id}. Updating with latest data...")
        
        # Step 4: Merge and validate the data
        print("🔄 Merging Agent 1 and Agent 2 data...")
        complete_profile = create_complete_profile_with_scores(agent1_data, agent2_data)
        
        print("✅ Profile merging and validation successful!")
        
        # Step 5: Save to users table
        print("🔄 Saving complete profile to users table...")
        success = save_complete_profile_to_users_table(user_id, complete_profile)
        
        if success:
            print(f"🎉 Complete JSON merge workflow successful for user {user_id}")
            print(f"📊 Profile saved with {complete_profile['total_carbon_footprint_tonnes']} tonnes CO₂ footprint")
            return True
        else:
            print(f"❌ Failed to save complete profile for user {user_id}")
            return False
            
    except Exception as e:
        print(f"❌ Error in complete JSON merge workflow: {str(e)}")
        return False


# Test function for development
def test_merge_function():
    """Test the merge function with sample data that matches the database structure"""
    
    # Sample Agent 1 output (Enhanced Profile) - from user_profiles.onboarding_final
    agent1_sample = {
        "key_levers": [
            "Increase recycling efforts consistently",
            "Reduce car usage by 30% and shift to more public transport or biking",
            "Implement home insulation to cut electricity usage"
        ],
        "demographics": {
            "climate": "Temperate",
            "location": "Bloomington, Indiana, United States",
            "home_type": "Apartment",
            "ownership": "Rent",
            "household_size": 2
        },
        "narrative_text": "Living in a modest apartment in Bloomington, Indiana, this user is environmentally motivated yet faces challenges like time and knowledge gaps.",
        "lifestyle_habits": {
            "diet": {
                "type": "Omnivore",
                "food_waste": "Sometimes",
                "meat_frequency": "Once a month"
            },
            "energy_usage": {
                "ac_usage": "Sometimes",
                "heating_source": "Electricity",
                "energy_conservation_habits": "Often"
            },
            "transportation": {
                "car_type": "Sedan",
                "primary_mode": "Personal Car",
                "commute_details": "10 miles, weekly public transport, occasional rideshare"
            }
        },
        "consumption_patterns": {
            "plastic_usage": "Sometimes",
            "recycling_habit": "Sometimes",
            "shopping_frequency": "A few times a week"
        },
        "psychographic_insights": {
            "goals": ["Reducing carbon footprint", "Saving money on bills"],
            "barriers": ["Not knowing what to do", "Lack of time", "Laziness"],
            "motivations": ["Protecting the environment"]
        }
    }
    
    # Sample Agent 2 output (Score Agent) - from user_scores.scores
    agent2_sample = {
        "score_category": "moderate",
        "data_confidence": "medium",
        "calculation_method": "Data was collected from user inputs, energy bills, transportation logs, and regional averages to estimate annual emissions.",
        "category_breakdown": {
            "diet_kg": 4.66,
            "other_kg": 0.0,
            "shopping_kg": 60.0,
            "home_energy_kg": 576.0,
            "transportation_kg": 1194.0,
            "digital_footprint_kg": 0.144
        },
        "sustainability_score": 6.5,
        "total_carbon_footprint_kg": 2784.0,
        "total_carbon_footprint_tonnes": 2.784,
        "top_impact_categories": ["Transportation", "Home Energy", "Diet"],
        "priority_reduction_areas": ["Transportation", "Home Energy", "Shopping"],
        "regional_comparison": {
            "user_location": "Bloomington, Indiana, United States",
            "local_average_kg": 3300.0,
            "comparison_status": "below",
            "percentage_difference": 15.8
        },
        "fun_comparison_facts": [
            "Your current footprint is equivalent to approximately 600 pounds of coal burned."
        ],
        "key_lever_validations": [
            {
                "lever": "Increase recycling efforts consistently",
                "validated": True,
                "impact_category": "Shopping",
                "validation_reason": "Enhanced recycling directly reduces waste and associated embodied emissions.",
                "potential_reduction_kg": 12.0
            }
        ]
    }
    
    try:
        # Test the merge function with sample data
        merged = create_complete_profile_with_scores(agent1_sample, agent2_sample)
        print("✅ Test merge successful!")
        print(f"📊 Total footprint: {merged['total_carbon_footprint_tonnes']} tonnes")
        print(f"🏠 Location: {merged['demographics']['location']}")
        print(f"🎯 Top category: {merged['top_impact_categories'][0]}")
        print(f"🔧 Key levers: {len(merged['key_levers'])} identified")
        print(f"📈 Sustainability score: {merged['sustainability_score']}/10")
        
        # Validate the structure matches target JSON
        expected_keys = [
            'narrative_text', 'demographics', 'lifestyle_habits', 'consumption_patterns',
            'psychographic_insights', 'key_levers', 'total_carbon_footprint_kg',
            'total_carbon_footprint_tonnes', 'category_breakdown', 'sustainability_score',
            'score_category', 'regional_comparison', 'key_lever_validations',
            'top_impact_categories', 'priority_reduction_areas', 'fun_comparison_facts'
        ]
        
        missing_keys = [key for key in expected_keys if key not in merged]
        if missing_keys:
            print(f"⚠️ Missing keys: {missing_keys}")
        else:
            print("✅ All expected keys present in merged profile")
        
        return True
        
    except Exception as e:
        print(f"❌ Test merge failed: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False


def test_with_real_files():
    """Test with the actual JSON files from experimentation folder"""
    import os
    
    try:
        # Get the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # Load Agent 1 data (Enhanced Profile)
        agent1_file = os.path.join(project_root, "experimentation", "test-json-3-enhanced-profile.json")
        with open(agent1_file, 'r') as f:
            agent1_data = json.load(f)
        
        # Load Agent 2 data (Score Agent)  
        agent2_file = os.path.join(project_root, "experimentation", "test-json-2-score-agent.json")
        with open(agent2_file, 'r') as f:
            agent2_data = json.load(f)
        
        print("✅ Loaded real JSON files for testing")
        print(f"📋 Agent 1 keys: {list(agent1_data.keys())}")
        print(f"📋 Agent 2 keys: {list(agent2_data.keys())}")
        
        # Test the merge
        merged = create_complete_profile_with_scores(agent1_data, agent2_data)
        
        print("✅ Real file merge successful!")
        print(f"📊 Total footprint: {merged.get('total_carbon_footprint_tonnes', 'N/A')} tonnes")
        print(f"🏠 Location: {merged.get('demographics', {}).get('location', 'N/A')}")
        
        # Save test result
        output_file = os.path.join(project_root, "experimentation", "test-merged-output.json")
        with open(output_file, 'w') as f:
            json.dump(merged, f, indent=2)
        
        print(f"💾 Test result saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Real file test failed: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False


if __name__ == "__main__":
    # Run tests when script is executed directly
    print("🧪 Running JSON merge tests...")
    print("\n1. Testing with sample data:")
    test1_success = test_merge_function()
    
    print("\n2. Testing with real JSON files:")
    test2_success = test_with_real_files()
    
    if test1_success and test2_success:
        print("\n🎉 All tests passed! merge_json() function is ready for use.")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
