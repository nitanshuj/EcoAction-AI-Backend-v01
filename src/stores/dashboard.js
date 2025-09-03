import { defineStore } from 'pinia'
import { ref } from 'vue'
import { supabase } from '../lib/supabase'

export const useDashboardStore = defineStore('dashboard', () => {
  const carbonFootprint = ref(0)
  const challenges = ref([])
  const recommendations = ref([])
  const loading = ref(false)
  const error = ref(null)

  const fetchDashboardData = async () => {
    loading.value = true
    error.value = null
    
    try {
      // Fetch user's carbon footprint data
      const { data: footprintData, error: footprintError } = await supabase
        .from('carbon_footprint')
        .select('*')
        .eq('user_id', supabase.auth.user()?.id)
        .order('created_at', { ascending: false })
        .limit(1)
        .single()

      if (footprintError && footprintError.code !== 'PGRST116') {
        throw footprintError
      }

      carbonFootprint.value = footprintData?.total_emissions || 0

      // Fetch active challenges
      const { data: challengesData, error: challengesError } = await supabase
        .from('challenges')
        .select('*')
        .eq('user_id', supabase.auth.user()?.id)
        .eq('status', 'active')

      if (challengesError) throw challengesError
      challenges.value = challengesData || []

      // Fetch recommendations
      const { data: recommendationsData, error: recommendationsError } = await supabase
        .from('recommendations')
        .select('*')
        .eq('user_id', supabase.auth.user()?.id)
        .order('created_at', { ascending: false })
        .limit(5)

      if (recommendationsError) throw recommendationsError
      recommendations.value = recommendationsData || []

    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }

  const updateCarbonFootprint = async (footprintData) => {
    loading.value = true
    error.value = null
    
    try {
      const { data, error: updateError } = await supabase
        .from('carbon_footprint')
        .upsert({
          user_id: supabase.auth.user()?.id,
          ...footprintData,
          updated_at: new Date().toISOString()
        })

      if (updateError) throw updateError
      
      await fetchDashboardData()
      return { success: true }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  const completeChallenge = async (challengeId) => {
    loading.value = true
    
    try {
      const { error: updateError } = await supabase
        .from('challenges')
        .update({ 
          status: 'completed',
          completed_at: new Date().toISOString()
        })
        .eq('id', challengeId)

      if (updateError) throw updateError
      
      await fetchDashboardData()
      return { success: true }
    } catch (err) {
      error.value = err.message
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  return {
    carbonFootprint,
    challenges,
    recommendations,
    loading,
    error,
    fetchDashboardData,
    updateCarbonFootprint,
    completeChallenge
  }
})