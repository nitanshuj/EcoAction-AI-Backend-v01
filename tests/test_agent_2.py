# test_agent_2.py
"""Test script for Agent 2 (Analyst) functionality"""

import sys, os, json

# Add the project root to the path so imports work
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from agent.crew import run_analyst_workflow
from agent.models import validate_analyst_output

def test_analyst_agent():
    """Test the analyst agent with sample enriched profile data"""
    
    # Sample enriched profile data (output from Agent 1)
    sample_enriched_profile = {
        "demographics": {
            "location": "San Francisco, United States",
            "climate": "Mediterranean",
            "household_size": 2,
            "home_type": "Apartment",
            "ownership": "Rent"
        },
        "lifestyle_habits": {
            "diet": {
                "type": "Omnivore",
                "meat_frequency": "A few times a week",
                "food_waste": "Sometimes"
            },
            "transportation": {
                "primary_mode": "Personal Car",
                "car_type": "Sedan",
                "commute_details": "20 miles; Occasionally uses rideshare; Weekly public transport"
            },
            "energy_usage": {
                "heating_source": "Natural Gas",
                "ac_usage": "Sometimes",
                "energy_conservation_habits": "Often"
            }
        },
        "consumption_patterns": {
            "shopping_frequency": "Weekly",
            "plastic_usage": "Sometimes",
            "recycling_habit": "Recycles everything possible"
        },
        "psychographic_insights": {
            "motivations": ["Protecting the environment"],
            "barriers": ["Not knowing what to do"],
            "goals": ["Reducing carbon footprint", "Start composting", "Reduce energy bills"]
        },
        "key_levers": [
            "Start composting to reduce organic waste",
            "Increase use of public transportation and ridesharing to cut car emissions by 30%",
            "Switch to renewable energy options or improve energy efficiency to lower energy bills",
            "Reduce meat intake further to minimize associated emissions"
        ],
        "narrative_text": "Living in San Francisco in a rented apartment, this environmentally motivated user works from home, driving a hybrid sedan for daily commutes. They enjoy cooking and gaming, with moderate digital device use. Their primary goal is reducing their carbon footprint and energy bills, motivated by protecting the environment but unsure of specific actions. They are eager to start composting and cut back on car usage and meat consumption to make a meaningful impact."
    }
    
    try:
        print("🧪 Testing Analyst Agent (Agent 2)...")
        print(f"📋 Input enriched profile: {json.dumps(sample_enriched_profile, indent=2)}")
        
        # For testing, we'll create a temporary test that directly uses the task
        from agent.agents import create_analyst_agent
        from agent.tasks import create_analyst_task
        from crewai import Crew, Process
        
        print("\n🚀 Running analyst workflow...")
        
        # Create analyst agent
        analyst_agent = create_analyst_agent()
        
        # Create analyst task with enriched profile
        analyst_task = create_analyst_task(analyst_agent, sample_enriched_profile)
        
        # Form the crew
        crew = Crew(
            agents=[analyst_agent],
            tasks=[analyst_task],
            process=Process.sequential,
            verbose=False,
            memory=False
        )
        
        # Execute workflow
        results = crew.kickoff()
        
        if results:
            print("✅ Analyst workflow completed!")
            
            # Parse results
            try:
                if hasattr(results, 'json') and results.json:
                    if isinstance(results.json, str):
                        parsed_results = json.loads(results.json)
                    else:
                        parsed_results = results.json
                elif hasattr(results, 'raw') and results.raw:
                    parsed_results = json.loads(results.raw)
                else:
                    result_str = str(results)
                    parsed_results = json.loads(result_str)
                    
            except (json.JSONDecodeError, AttributeError) as e:
                print(f"❌ Failed to parse results as JSON: {e}")
                print(f"Raw results: {results}")
                return False
            
            print(f"\n📊 Raw Results: {json.dumps(parsed_results, indent=2)}")
            
            # Validate with Pydantic
            try:
                validated_output = validate_analyst_output(parsed_results)
                print("\n✅ Pydantic validation successful!")
                
                # Display key insights using new model structure
                print(f"\n🌍 Carbon Footprint: {validated_output.total_carbon_footprint_tonnes:.2f} tonnes CO₂/year")
                print(f"📊 Sustainability Score: {validated_output.sustainability_score}/10 ({validated_output.score_category})")
                print(f"🎯 Top Impact Areas: {', '.join(validated_output.top_impact_categories)}")
                print(f"📍 Compared to {validated_output.regional_comparison.user_location}: {validated_output.regional_comparison.comparison_status} average")
                
                # Display key lever validations
                print("\n🔧 Key Lever Validations:")
                for i, validation in enumerate(validated_output.key_lever_validations, 1):
                    status = "✅ Validated" if validation.validated else "❌ Not validated"
                    print(f"  {i}. {validation.lever}")
                    print(f"     {status} - Potential reduction: {validation.potential_reduction_kg}kg CO₂/year")
                    print(f"     Reason: {validation.validation_reason}")
                
                # Display psychographic insights
                print("\n💭 Psychographic Insights:")
                for i, insight in enumerate(validated_output.psychographic_insights, 1):
                    print(f"  {i}. {insight.insight_text}")
                    print(f"     Addresses: {insight.addresses_barrier} | Motivation: {insight.related_motivation}")
                    print(f"     Next step: {insight.actionable_next_step}")
                
                return True
                
            except ValueError as e:
                print(f"❌ Pydantic validation failed: {str(e)}")
                return False
                
        else:
            print("❌ Analyst workflow returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Error testing analyst agent: {str(e)}")
        import traceback
        print(f"🔍 Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_analyst_agent()
    print(f"\n{'🎉 Test PASSED' if success else '💥 Test FAILED'}")
