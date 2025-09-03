<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-br from-primary-600 via-primary-700 to-slate-800 text-white">
      <div class="absolute inset-0 bg-black opacity-10"></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center animate-fade-in">
          <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Your Personal
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-400">
              Climate Action
            </span>
            Assistant
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto leading-relaxed">
            Track your carbon footprint, get personalized sustainability recommendations, 
            and join challenges to make a real environmental impact.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <RouterLink 
              to="/auth" 
              class="bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all duration-200 transform hover:scale-105 hover:shadow-xl animate-bounce-gentle"
            >
              Start Your Journey
            </RouterLink>
            <button class="text-blue-100 hover:text-white font-medium py-4 px-8 rounded-xl border-2 border-blue-200 hover:border-white transition-all duration-200 transform hover:scale-105">
              Learn More
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-20 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16 animate-slide-up">
          <h2 class="text-4xl font-bold text-slate-800 mb-4">
            AI-Powered Climate Action
          </h2>
          <p class="text-xl text-slate-600 max-w-2xl mx-auto">
            Leverage artificial intelligence to understand and reduce your environmental impact
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div 
            v-for="(feature, index) in features" 
            :key="index"
            class="card text-center group hover:shadow-xl transition-all duration-300 animate-slide-up"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-700 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-200">
              <span class="text-2xl">{{ feature.icon }}</span>
            </div>
            <h3 class="text-xl font-bold text-slate-800 mb-4">{{ feature.title }}</h3>
            <p class="text-slate-600 leading-relaxed">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 bg-slate-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center mb-16">
          <h2 class="text-4xl font-bold text-slate-800 mb-4">
            Making a Real Impact
          </h2>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div 
            v-for="(stat, index) in stats" 
            :key="index"
            class="text-center animate-slide-up"
            :style="{ animationDelay: `${index * 0.1}s` }"
          >
            <div class="text-4xl font-bold text-primary-600 mb-2">{{ stat.value }}</div>
            <div class="text-slate-600 font-medium">{{ stat.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-20 bg-gradient-to-r from-primary-600 to-primary-800 text-white">
      <div class="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h2 class="text-4xl font-bold mb-6">Ready to Make a Difference?</h2>
        <p class="text-xl text-blue-100 mb-8">
          Join thousands of users who are already reducing their carbon footprint with AI-powered insights.
        </p>
        <RouterLink 
          to="/auth" 
          class="bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-xl text-lg transition-all duration-200 transform hover:scale-105 hover:shadow-xl inline-block"
        >
          Get Started Free
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'

const features = [
  {
    icon: '📊',
    title: 'Carbon Tracking',
    description: 'Monitor your daily carbon footprint across transportation, energy, and consumption with AI-powered analysis.'
  },
  {
    icon: '🎯',
    title: 'Smart Challenges',
    description: 'Participate in personalized sustainability challenges designed to fit your lifestyle and maximize impact.'
  },
  {
    icon: '💡',
    title: 'AI Recommendations',
    description: 'Get intelligent, actionable suggestions to reduce your environmental impact based on your unique patterns.'
  }
]

const stats = [
  { value: '10K+', label: 'Active Users' },
  { value: '2.5M', label: 'CO₂ Tons Saved' },
  { value: '50K+', label: 'Challenges Completed' }
]
</script>