#!/usr/bin/env python3
"""
Quick test for dictionary validation fix
"""

from agent.models import validate_planner_output

def test_dict_validation():
    """Test that dictionary input works directly"""
    
    # Valid dictionary output (like what the agent actually returns)
    dict_output = {
        'week_focus': 'Reducing Transportation and Home Energy Usage',
        'priority_area': 'Transportation',
        'challenges': [
            {
                'id': 'easy1',
                'title': 'Bike for Short Errands',
                'description': 'Replace car trips with biking for errands within 3 miles whenever possible.',
                'difficulty': 'easy',
                'category': 'transport',
                'steps': ['Plan route', 'Check bike condition', 'Track trips'],
                'co2_savings_kg': 5.2,
                'time_required': '30 minutes',
                'deadline': 'Daily this week',
                'success_metrics': 'Number of bike trips',
                'motivation': 'Get exercise while helping environment'
            },
            {
                'id': 'easy2',
                'title': 'Turn Off Lights',
                'description': 'Turn off lights when leaving rooms',
                'difficulty': 'easy',
                'category': 'energy',
                'steps': ['Check all rooms', 'Switch off unused lights'],
                'co2_savings_kg': 2.1,
                'time_required': '2 minutes',
                'deadline': 'Daily this week',
                'success_metrics': 'Lights turned off count',
                'motivation': 'Save electricity costs'
            },
            {
                'id': 'easy3',
                'title': 'Unplug Electronics',
                'description': 'Unplug electronics when not in use',
                'difficulty': 'easy',
                'category': 'energy',
                'steps': ['Identify vampire devices', 'Unplug after use'],
                'co2_savings_kg': 1.8,
                'time_required': '5 minutes',
                'deadline': 'Daily this week',
                'success_metrics': 'Devices unplugged',
                'motivation': 'Reduce phantom power draw'
            },
            {
                'id': 'medium1',
                'title': 'Public Transit Week',
                'description': 'Use public transportation for commuting 3 days this week',
                'difficulty': 'medium',
                'category': 'transport',
                'steps': ['Research routes', 'Buy transit pass', 'Plan schedules'],
                'co2_savings_kg': 15.4,
                'time_required': '2 hours setup',
                'deadline': 'By end of week',
                'success_metrics': '3 transit commutes completed',
                'motivation': 'Explore new transportation options'
            },
            {
                'id': 'medium2',
                'title': 'Energy Audit',
                'description': 'Conduct home energy audit and identify improvement areas',
                'difficulty': 'medium',
                'category': 'energy',
                'steps': ['Download audit checklist', 'Inspect all areas', 'Document findings'],
                'co2_savings_kg': 8.7,
                'time_required': '3 hours',
                'deadline': 'By end of week',
                'success_metrics': 'Audit completed with action plan',
                'motivation': 'Identify biggest energy wasters'
            },
            {
                'id': 'hard1',
                'title': 'Smart Thermostat Installation',
                'description': 'Install programmable smart thermostat for energy optimization',
                'difficulty': 'hard',
                'category': 'energy',
                'steps': ['Research models', 'Purchase thermostat', 'Install or hire electrician', 'Program schedules'],
                'co2_savings_kg': 42.3,
                'time_required': '4-6 hours',
                'deadline': 'Within 2 weeks',
                'success_metrics': 'Smart thermostat installed and programmed',
                'motivation': 'Automated energy optimization'
            }
        ],
        'total_potential_savings': 75.5,
        'motivation_message': 'These challenges focus on your biggest impact areas - transportation and home energy!'
    }
    
    print("🧪 Testing dictionary validation...")
    print(f"Input type: {type(dict_output)}")
    print(f"Number of challenges: {len(dict_output['challenges'])}")
    
    try:
        result = validate_planner_output(dict_output)
        print("✅ Dictionary validation successful!")
        print(f"📊 Validated {len(result.challenges)} challenges")
        print(f"🎯 Week focus: {result.week_focus}")
        print(f"🚀 Total savings: {result.total_potential_savings} kg CO2")
        
        # Check difficulty distribution
        easy_count = sum(1 for c in result.challenges if c.difficulty == 'easy')
        medium_count = sum(1 for c in result.challenges if c.difficulty == 'medium')
        hard_count = sum(1 for c in result.challenges if c.difficulty == 'hard')
        
        print(f"📈 Distribution: {easy_count} easy, {medium_count} medium, {hard_count} hard")
        
        if easy_count == 3 and medium_count == 2 and hard_count == 1:
            print("✅ Perfect difficulty distribution!")
            return True
        else:
            print("❌ Wrong difficulty distribution")
            return False
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_dict_validation()
    print(f"\n🎯 Test result: {'PASSED' if success else 'FAILED'}")
    exit(0 if success else 1)
