<template>
  <div class="min-h-screen bg-slate-50 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8 animate-fade-in">
        <h1 class="text-4xl font-bold text-slate-800 mb-2">
          Your Climate Dashboard
        </h1>
        <p class="text-xl text-slate-600">
          Track your progress and discover new ways to reduce your environmental impact
        </p>
      </div>

      <div v-if="loading" class="flex justify-center py-12">
        <LoadingSpinner />
      </div>

      <div v-else class="space-y-8">
        <!-- Carbon Footprint Overview -->
        <div class="grid md:grid-cols-3 gap-6 animate-slide-up">
          <div class="card text-center">
            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-800 mb-2">
              {{ carbonFootprint.toLocaleString() }} kg
            </h3>
            <p class="text-slate-600">Annual CO₂ Footprint</p>
            <div class="mt-4 bg-slate-100 rounded-full h-2">
              <div class="bg-red-500 h-2 rounded-full" style="width: 65%"></div>
            </div>
            <p class="text-sm text-slate-500 mt-2">65% of global average</p>
          </div>

          <div class="card text-center">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-800 mb-2">
              {{ challenges.length }}
            </h3>
            <p class="text-slate-600">Active Challenges</p>
            <div class="mt-4 bg-slate-100 rounded-full h-2">
              <div class="bg-green-500 h-2 rounded-full" style="width: 80%"></div>
            </div>
            <p class="text-sm text-slate-500 mt-2">80% completion rate</p>
          </div>

          <div class="card text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-slate-800 mb-2">
              1,250 kg
            </h3>
            <p class="text-slate-600">CO₂ Saved This Year</p>
            <div class="mt-4 bg-slate-100 rounded-full h-2">
              <div class="bg-primary-500 h-2 rounded-full" style="width: 45%"></div>
            </div>
            <p class="text-sm text-slate-500 mt-2">45% of annual goal</p>
          </div>
        </div>

        <!-- AI Recommendations -->
        <div class="animate-slide-up" style="animation-delay: 0.2s">
          <h2 class="text-2xl font-bold text-slate-800 mb-6">
            🤖 AI Recommendations for You
          </h2>
          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div 
              v-for="recommendation in recommendations" 
              :key="recommendation.id"
              class="card group hover:scale-105 transition-all duration-300 cursor-pointer"
            >
              <div class="flex items-start space-x-4">
                <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200 transition-colors duration-300">
                  <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-slate-800 mb-2">{{ recommendation.title }}</h3>
                  <p class="text-slate-600 text-sm mb-3">{{ recommendation.description }}</p>
                  <div class="flex items-center justify-between">
                    <span class="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                      {{ recommendation.impact }}
                    </span>
                    <button class="text-primary-600 hover:text-primary-700 text-sm font-medium">
                      Start →
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Active Challenges -->
        <div class="animate-slide-up" style="animation-delay: 0.4s">
          <h2 class="text-2xl font-bold text-slate-800 mb-6">
            🏆 Your Active Challenges
          </h2>
          <div class="grid md:grid-cols-2 gap-6">
            <ChallengeCard 
              v-for="challenge in mockChallenges" 
              :key="challenge.id"
              :challenge="challenge"
            />
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="animate-slide-up" style="animation-delay: 0.6s">
          <h2 class="text-2xl font-bold text-slate-800 mb-6">
            ⚡ Quick Actions
          </h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button class="card text-center hover:scale-105 transition-all duration-300 group">
              <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:bg-blue-200 transition-colors duration-300">
                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-700">Log Activity</span>
            </button>

            <button class="card text-center hover:scale-105 transition-all duration-300 group">
              <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:bg-green-200 transition-colors duration-300">
                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-700">View Report</span>
            </button>

            <button class="card text-center hover:scale-105 transition-all duration-300 group">
              <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:bg-purple-200 transition-colors duration-300">
                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-700">Join Challenge</span>
            </button>

            <button class="card text-center hover:scale-105 transition-all duration-300 group">
              <div class="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mx-auto mb-3 group-hover:bg-orange-200 transition-colors duration-300">
                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <span class="text-sm font-medium text-slate-700">Get Tips</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useDashboardStore } from '../stores/dashboard'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ChallengeCard from '../components/ChallengeCard.vue'

const authStore = useAuthStore()
const dashboardStore = useDashboardStore()

const loading = computed(() => dashboardStore.loading)
const carbonFootprint = computed(() => dashboardStore.carbonFootprint)
const challenges = computed(() => dashboardStore.challenges)
const recommendations = computed(() => dashboardStore.recommendations)

const mockChallenges = ref([
  {
    id: 1,
    title: 'Plastic-Free Week',
    description: 'Avoid single-use plastics for 7 days',
    progress: 65,
    daysLeft: 3,
    participants: 1247,
    reward: '500 EcoPoints'
  },
  {
    id: 2,
    title: 'Bike to Work',
    description: 'Use bicycle for commuting 5 times',
    progress: 40,
    daysLeft: 10,
    participants: 892,
    reward: '300 EcoPoints'
  }
])

onMounted(() => {
  if (authStore.user) {
    dashboardStore.fetchDashboardData(authStore.user.id)
  }
})
</script>