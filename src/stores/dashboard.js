import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export const useDashboardStore = defineStore('dashboard', () => {
  const carbonFootprint = ref(0)
  const challenges = ref([])
  const recommendations = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchDashboardData = async (userId) => {
    loading.value = true
    error.value = null
    
    try {
      // Fetch user profile and carbon footprint
      const { data: profile } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('user_id', userId)
        .single()

      if (profile) {
        carbonFootprint.value = profile.carbon_footprint || 0
      }

      // Fetch active challenges
      const { data: userChallenges } = await supabase
        .from('user_challenges')
        .select(`
          *,
          challenges (*)
        `)
        .eq('user_id', userId)
        .eq('status', 'active')

      challenges.value = userChallenges || []

      // Mock recommendations for now
      recommendations.value = [
        {
          id: 1,
          title: 'Switch to LED Bulbs',
          description: 'Replace incandescent bulbs with LED alternatives',
          impact: 'Save 75% energy on lighting',
          category: 'energy'
        },
        {
          id: 2,
          title: 'Use Public Transport',
          description: 'Take public transport 2 days per week',
          impact: 'Reduce transport emissions by 30%',
          category: 'transport'
        },
        {
          id: 3,
          title: 'Reduce Meat Consumption',
          description: 'Try plant-based meals 3 times per week',
          impact: 'Lower food carbon footprint by 20%',
          category: 'food'
        }
      ]

    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const updateCarbonFootprint = async (userId, newFootprint) => {
    try {
      const { error: updateError } = await supabase
        .from('user_profiles')
        .update({ carbon_footprint: newFootprint })
        .eq('user_id', userId)

      if (updateError) throw updateError
      
      carbonFootprint.value = newFootprint
    } catch (err) {
      error.value = err.message
    }
  }

  return {
    carbonFootprint,
    challenges,
    recommendations,
    loading,
    error,
    fetchDashboardData,
    updateCarbonFootprint
  }
})