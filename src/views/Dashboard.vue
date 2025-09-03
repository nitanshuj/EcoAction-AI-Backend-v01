<template>
  <div class="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="mb-8 animate-fade-in">
        <h1 class="text-3xl font-bold text-slate-800 mb-2">
          Welcome back, {{ authStore.user?.user_metadata?.first_name || 'there' }}! 👋
        </h1>
        <p class="text-slate-600">
          Here's your sustainability dashboard and personalized recommendations.
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="dashboardStore.loading" class="flex items-center justify-center py-12">
        <LoadingSpinner />
      </div>

      <!-- Dashboard Content -->
      <div v-else class="space-y-8">
        <!-- Carbon Footprint Overview -->
        <section class="animate-slide-up">
          <h2 class="text-2xl font-bold text-slate-800 mb-6">Carbon Footprint Overview</h2>
          <div class="grid md:grid-cols-3 gap-6">
            <div class="card text-center group hover:shadow-lg transition-all duration-300">
              <div class="w-16 h-16 bg-gradient-to-br from-red-500 to-red-700 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
                <span class="text-2xl">🏭</span>
              </div>
              <h3 class="text-lg font-semibold text-slate-800 mb-2">Total Emissions</h3>
              <p class="text-3xl font-bold text-red-600 mb-1">{{ dashboardStore.carbonFootprint.toFixed(1) }}</p>
              <p class="text-sm text-slate-500">tons CO₂/year</p>
            </div>

            <div class="card text-center group hover:shadow-lg transition-all duration-300">
              <div class="w-16 h-16 bg-gradient-to-br from-yellow-500 to-yellow-700 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
                <span class="text-2xl">📊</span>
              </div>
              <h3 class="text-lg font-semibold text-slate-800 mb-2">vs. Average</h3>
              <p class="text-3xl font-bold text-yellow-600 mb-1">-15%</p>
              <p class="text-sm text-slate-500">below national avg</p>
            </div>

            <div class="card text-center group hover:shadow-lg transition-all duration-300">
              <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-green-700 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-200">
                <span class="text-2xl">🎯</span>
              </div>
              <h3 class="text-lg font-semibold text-slate-800 mb-2">Goal Progress</h3>
              <p class="text-3xl font-bold text-green-600 mb-1">68%</p>
              <p class="text-sm text-slate-500">to 2030 target</p>
            </div>
          </div>
        </section>

        <!-- Active Challenges -->
        <section class="animate-slide-up" style="animation-delay: 0.1s">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-bold text-slate-800">Active Challenges</h2>
            <button class="btn-secondary">
              Browse All
            </button>
          </div>
          
          <div v-if="dashboardStore.challenges.length === 0" class="card text-center py-12">
            <div class="w-16 h-16 bg-gradient-to-br from-slate-400 to-slate-600 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl">🎯</span>
            </div>
            <h3 class="text-lg font-semibold text-slate-800 mb-2">No Active Challenges</h3>
            <p class="text-slate-600 mb-4">Start a challenge to begin your sustainability journey!</p>
            <button class="btn-primary">Browse Challenges</button>
          </div>

          <div v-else class="grid md:grid-cols-2 gap-6">
            <ChallengeCard 
              v-for="challenge in dashboardStore.challenges" 
              :key="challenge.id"
              :challenge="challenge"
              @complete="handleCompleteChallenge"
            />
          </div>
        </section>

        <!-- AI Recommendations -->
        <section class="animate-slide-up" style="animation-delay: 0.2s">
          <h2 class="text-2xl font-bold text-slate-800 mb-6">AI Recommendations</h2>
          
          <div v-if="dashboardStore.recommendations.length === 0" class="card text-center py-12">
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-700 rounded-full flex items-center justify-center mx-auto mb-4">
              <span class="text-2xl">🤖</span>
            </div>
            <h3 class="text-lg font-semibold text-slate-800 mb-2">Generating Recommendations</h3>
            <p class="text-slate-600 mb-4">Our AI is analyzing your data to provide personalized suggestions.</p>
            <button @click="generateRecommendations" class="btn-primary">
              Generate Now
            </button>
          </div>

          <div v-else class="space-y-4">
            <div 
              v-for="(recommendation, index) in dashboardStore.recommendations" 
              :key="recommendation.id"
              class="card group hover:shadow-lg transition-all duration-300 animate-slide-up"
              :style="{ animationDelay: `${index * 0.1}s` }"
            >
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform duration-200">
                  <span class="text-xl">💡</span>
                </div>
                <div class="flex-1">
                  <h3 class="text-lg font-semibold text-slate-800 mb-2">
                    {{ recommendation.title }}
                  </h3>
                  <p class="text-slate-600 mb-3">
                    {{ recommendation.description }}
                  </p>
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium text-green-600">
                      Potential savings: {{ recommendation.potential_savings }} kg CO₂/month
                    </span>
                    <button class="btn-secondary text-sm">
                      Learn More
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Quick Actions -->
        <section class="animate-slide-up" style="animation-delay: 0.3s">
          <h2 class="text-2xl font-bold text-slate-800 mb-6">Quick Actions</h2>
          <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <button 
              v-for="action in quickActions" 
              :key="action.label"
              class="card text-center group hover:shadow-lg transition-all duration-300 hover:scale-105"
            >
              <div class="w-12 h-12 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform duration-200">
                <span class="text-xl">{{ action.icon }}</span>
              </div>
              <span class="font-medium text-slate-700">{{ action.label }}</span>
            </button>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useDashboardStore } from '../stores/dashboard'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ChallengeCard from '../components/ChallengeCard.vue'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const quickActions = [
  { icon: '📱', label: 'Log Activity' },
  { icon: '🎯', label: 'New Challenge' },
  { icon: '📈', label: 'View Reports' },
  { icon: '🤝', label: 'Share Progress' }
]

const handleCompleteChallenge = async (challengeId) => {
  await dashboardStore.completeChallenge(challengeId)
}

const generateRecommendations = async () => {
  // This would typically call an AI service
  console.log('Generating AI recommendations...')
}

onMounted(() => {
  dashboardStore.fetchDashboardData()
})
</script>