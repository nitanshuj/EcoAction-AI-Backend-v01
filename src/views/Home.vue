<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-br from-primary-600 via-primary-700 to-slate-800 text-white py-20">
      <div class="absolute inset-0 bg-black opacity-10"></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="text-center animate-fade-in">
          <h1 class="text-5xl md:text-6xl font-bold mb-6 leading-tight">
            Your Personal
            <span class="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-400">
              Climate Action
            </span>
            Assistant
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto leading-relaxed">
            Track your carbon footprint, get personalized recommendations, and join challenges to make a real impact on our planet.
          </p>
          <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <RouterLink 
              to="/auth" 
              class="btn-primary text-lg px-8 py-4 animate-bounce-gentle"
            >
              Start Your Journey
            </RouterLink>
            <button class="text-blue-200 hover:text-white font-semibold transition-colors duration-200 flex items-center space-x-2">
              <span>Learn More</span>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
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
            Harness the power of artificial intelligence to make meaningful environmental changes in your daily life.
          </p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
          <div class="card text-center group hover:scale-105 transition-transform duration-300">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-primary-200 transition-colors duration-300">
              <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-800 mb-3">Carbon Tracking</h3>
            <p class="text-slate-600">
              Monitor your daily carbon footprint with intelligent tracking and detailed analytics.
            </p>
          </div>

          <div class="card text-center group hover:scale-105 transition-transform duration-300">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-green-200 transition-colors duration-300">
              <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-800 mb-3">Smart Recommendations</h3>
            <p class="text-slate-600">
              Get personalized AI-powered suggestions tailored to your lifestyle and goals.
            </p>
          </div>

          <div class="card text-center group hover:scale-105 transition-transform duration-300">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6 group-hover:bg-purple-200 transition-colors duration-300">
              <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-slate-800 mb-3">Community Challenges</h3>
            <p class="text-slate-600">
              Join eco-friendly challenges and compete with others to maximize your environmental impact.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-20 bg-slate-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid md:grid-cols-3 gap-8 text-center">
          <div class="animate-slide-up">
            <div class="text-4xl font-bold text-primary-600 mb-2">10,000+</div>
            <div class="text-slate-600 font-medium">Active Users</div>
          </div>
          <div class="animate-slide-up" style="animation-delay: 0.2s">
            <div class="text-4xl font-bold text-green-600 mb-2">2.5M kg</div>
            <div class="text-slate-600 font-medium">CO₂ Saved</div>
          </div>
          <div class="animate-slide-up" style="animation-delay: 0.4s">
            <div class="text-4xl font-bold text-purple-600 mb-2">500+</div>
            <div class="text-slate-600 font-medium">Challenges Completed</div>
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
          class="inline-block bg-white text-primary-600 font-bold py-4 px-8 rounded-lg hover:bg-slate-50 transition-all duration-200 transform hover:scale-105 hover:shadow-lg"
        >
          Get Started Today
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import Navbar from '../components/Navbar.vue'
</script>