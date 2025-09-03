<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-primary-50 py-12">
    <div class="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-8 animate-fade-in">
        <h1 class="text-4xl font-bold text-slate-800 mb-4">
          Let's Personalize Your Experience
        </h1>
        <p class="text-xl text-slate-600">
          Help us understand your lifestyle to provide better recommendations
        </p>
        
        <!-- Progress Bar -->
        <div class="mt-8 bg-slate-200 rounded-full h-2 max-w-md mx-auto">
          <div 
            class="bg-primary-600 h-2 rounded-full transition-all duration-500 ease-out"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <p class="text-sm text-slate-500 mt-2">{{ Math.round(progress) }}% Complete</p>
      </div>

      <div class="card animate-slide-up">
        <form @submit.prevent="handleSubmit" class="space-y-8">
          <!-- Transportation -->
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-slate-800 flex items-center">
              <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7v8a2 2 0 002 2h6M8 7V5a2 2 0 012-2h4.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V15a2 2 0 01-2 2v0a2 2 0 01-2-2v-4a2 2 0 00-2-2H8z" />
              </svg>
              Transportation
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  Primary Transport
                </label>
                <select v-model="form.transport" class="input-field">
                  <option value="">Select transport</option>
                  <option value="car">Car</option>
                  <option value="public">Public Transport</option>
                  <option value="bike">Bicycle</option>
                  <option value="walk">Walking</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  Weekly Miles
                </label>
                <input
                  v-model.number="form.weeklyMiles"
                  type="number"
                  class="input-field"
                  placeholder="e.g., 100"
                />
              </div>
            </div>
          </div>

          <!-- Energy -->
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-slate-800 flex items-center">
              <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Energy Usage
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  Home Type
                </label>
                <select v-model="form.homeType" class="input-field">
                  <option value="">Select home type</option>
                  <option value="apartment">Apartment</option>
                  <option value="house">House</option>
                  <option value="condo">Condo</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  Monthly Energy (kWh)
                </label>
                <input
                  v-model.number="form.monthlyEnergy"
                  type="number"
                  class="input-field"
                  placeholder="e.g., 800"
                />
              </div>
            </div>
          </div>

          <!-- Diet -->
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-slate-800 flex items-center">
              <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16l3-1m-3 1l-3-1" />
              </svg>
              Diet & Lifestyle
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  Diet Type
                </label>
                <select v-model="form.diet" class="input-field">
                  <option value="">Select diet</option>
                  <option value="omnivore">Omnivore</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                  <option value="pescatarian">Pescatarian</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-2">
                  Household Size
                </label>
                <input
                  v-model.number="form.householdSize"
                  type="number"
                  min="1"
                  class="input-field"
                  placeholder="e.g., 3"
                />
              </div>
            </div>
          </div>

          <div class="flex justify-between pt-6">
            <RouterLink 
              to="/" 
              class="btn-secondary"
            >
              Back
            </RouterLink>
            <button
              type="submit"
              :disabled="!isFormValid || loading"
              class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading">Setting up...</span>
              <span v-else>Complete Setup</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const loading = ref(false)
const form = ref({
  transport: '',
  weeklyMiles: null,
  homeType: '',
  monthlyEnergy: null,
  diet: '',
  householdSize: null
})

const progress = computed(() => {
  const fields = Object.values(form.value)
  const filledFields = fields.filter(field => field !== '' && field !== null).length
  return (filledFields / fields.length) * 100
})

const isFormValid = computed(() => {
  return form.value.transport && 
         form.value.weeklyMiles && 
         form.value.homeType && 
         form.value.monthlyEnergy && 
         form.value.diet && 
         form.value.householdSize
})

const handleSubmit = async () => {
  if (!isFormValid.value) return

  loading.value = true
  
  try {
    // Calculate initial carbon footprint based on form data
    const carbonFootprint = calculateCarbonFootprint(form.value)
    
    // Save user profile to Supabase
    const { error } = await supabase
      .from('user_profiles')
      .insert({
        user_id: authStore.user.id,
        transport_mode: form.value.transport,
        weekly_miles: form.value.weeklyMiles,
        home_type: form.value.homeType,
        monthly_energy: form.value.monthlyEnergy,
        diet_type: form.value.diet,
        household_size: form.value.householdSize,
        carbon_footprint: carbonFootprint
      })

    if (error) throw error

    router.push('/dashboard')
  } catch (err) {
    console.error('Error saving profile:', err)
  } finally {
    loading.value = false
  }
}

const calculateCarbonFootprint = (data) => {
  // Simplified carbon footprint calculation
  let footprint = 0
  
  // Transport emissions (kg CO2 per week)
  const transportEmissions = {
    car: data.weeklyMiles * 0.4,
    public: data.weeklyMiles * 0.1,
    bike: 0,
    walk: 0
  }
  footprint += transportEmissions[data.transport] || 0
  
  // Energy emissions (kg CO2 per month)
  footprint += (data.monthlyEnergy * 0.5) / 4 // Convert to weekly
  
  // Diet emissions (kg CO2 per week)
  const dietEmissions = {
    omnivore: 70,
    pescatarian: 50,
    vegetarian: 30,
    vegan: 20
  }
  footprint += (dietEmissions[data.diet] || 50) / data.householdSize
  
  return Math.round(footprint * 52) // Annual footprint
}
</script>