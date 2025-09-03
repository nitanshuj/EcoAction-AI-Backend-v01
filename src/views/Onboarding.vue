<template>
  <div class="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-2xl mx-auto">
      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-slate-600">Setup Progress</span>
          <span class="text-sm font-medium text-slate-600">{{ Math.round(progress) }}%</span>
        </div>
        <div class="w-full bg-slate-200 rounded-full h-2">
          <div 
            class="bg-gradient-to-r from-primary-500 to-green-500 h-2 rounded-full transition-all duration-500 ease-out"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <div class="card animate-slide-up">
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-slate-800 mb-2">
            Let's Personalize Your Experience
          </h1>
          <p class="text-slate-600">
            Help us understand your lifestyle to provide better recommendations
          </p>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-6">
          <!-- Location -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">
              Location
            </label>
            <input
              v-model="form.location"
              type="text"
              required
              class="input-field"
              placeholder="City, Country"
            />
          </div>

          <!-- Household Size -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">
              Household Size
            </label>
            <select v-model="form.householdSize" required class="input-field">
              <option value="">Select household size</option>
              <option value="1">1 person</option>
              <option value="2">2 people</option>
              <option value="3">3 people</option>
              <option value="4">4 people</option>
              <option value="5+">5+ people</option>
            </select>
          </div>

          <!-- Transportation -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">
              Primary Transportation
            </label>
            <div class="grid grid-cols-2 gap-3">
              <label 
                v-for="transport in transportOptions" 
                :key="transport.value"
                class="flex items-center p-3 border border-slate-300 rounded-lg cursor-pointer hover:border-primary-500 transition-colors duration-200"
                :class="{ 'border-primary-500 bg-primary-50': form.transportation === transport.value }"
              >
                <input
                  v-model="form.transportation"
                  type="radio"
                  :value="transport.value"
                  class="sr-only"
                />
                <span class="text-2xl mr-3">{{ transport.icon }}</span>
                <span class="font-medium text-slate-700">{{ transport.label }}</span>
              </label>
            </div>
          </div>

          <!-- Diet -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">
              Diet Type
            </label>
            <select v-model="form.diet" required class="input-field">
              <option value="">Select your diet</option>
              <option value="omnivore">Omnivore</option>
              <option value="vegetarian">Vegetarian</option>
              <option value="vegan">Vegan</option>
              <option value="pescatarian">Pescatarian</option>
            </select>
          </div>

          <!-- Energy Usage -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">
              Monthly Energy Bill (USD)
            </label>
            <input
              v-model.number="form.energyBill"
              type="number"
              min="0"
              required
              class="input-field"
              placeholder="150"
            />
          </div>

          <!-- Goals -->
          <div>
            <label class="block text-sm font-medium text-slate-700 mb-2">
              Sustainability Goals (select all that apply)
            </label>
            <div class="space-y-2">
              <label 
                v-for="goal in sustainabilityGoals" 
                :key="goal.value"
                class="flex items-center p-3 border border-slate-300 rounded-lg cursor-pointer hover:border-primary-500 transition-colors duration-200"
                :class="{ 'border-primary-500 bg-primary-50': form.goals.includes(goal.value) }"
              >
                <input
                  v-model="form.goals"
                  type="checkbox"
                  :value="goal.value"
                  class="sr-only"
                />
                <span class="text-xl mr-3">{{ goal.icon }}</span>
                <span class="font-medium text-slate-700">{{ goal.label }}</span>
              </label>
            </div>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Setting up your profile...
            </span>
            <span v-else>Complete Setup</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../lib/supabase'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  location: '',
  householdSize: '',
  transportation: '',
  diet: '',
  energyBill: null,
  goals: []
})

const transportOptions = [
  { value: 'car', label: 'Car', icon: '🚗' },
  { value: 'public', label: 'Public Transit', icon: '🚌' },
  { value: 'bike', label: 'Bike/Walk', icon: '🚴' },
  { value: 'mixed', label: 'Mixed', icon: '🔄' }
]

const sustainabilityGoals = [
  { value: 'reduce_emissions', label: 'Reduce Carbon Emissions', icon: '🌍' },
  { value: 'save_energy', label: 'Save Energy', icon: '⚡' },
  { value: 'sustainable_transport', label: 'Sustainable Transportation', icon: '🚲' },
  { value: 'eco_diet', label: 'Eco-Friendly Diet', icon: '🥬' },
  { value: 'waste_reduction', label: 'Reduce Waste', icon: '♻️' },
  { value: 'water_conservation', label: 'Water Conservation', icon: '💧' }
]

const progress = computed(() => {
  const fields = ['location', 'householdSize', 'transportation', 'diet', 'energyBill']
  const completed = fields.filter(field => form[field]).length
  const goalsProgress = form.goals.length > 0 ? 1 : 0
  return ((completed + goalsProgress) / (fields.length + 1)) * 100
})

const handleSubmit = async () => {
  loading.value = true
  
  try {
    const { error } = await supabase
      .from('user_profiles')
      .upsert({
        user_id: supabase.auth.user()?.id,
        location: form.location,
        household_size: parseInt(form.householdSize),
        primary_transportation: form.transportation,
        diet_type: form.diet,
        monthly_energy_bill: form.energyBill,
        sustainability_goals: form.goals,
        onboarding_completed: true,
        updated_at: new Date().toISOString()
      })

    if (error) throw error

    router.push('/dashboard')
  } catch (error) {
    console.error('Error saving profile:', error)
  } finally {
    loading.value = false
  }
}
</script>