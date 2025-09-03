<template>
  <nav class="bg-white shadow-sm border-b border-slate-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <RouterLink to="/" class="flex items-center space-x-2 group">
            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center transform group-hover:scale-110 transition-transform duration-200">
              <span class="text-white font-bold text-sm">🌱</span>
            </div>
            <span class="text-xl font-bold text-slate-800 group-hover:text-primary-600 transition-colors duration-200">
              EcoAction AI
            </span>
          </RouterLink>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-8">
          <RouterLink 
            to="/" 
            class="text-slate-600 hover:text-primary-600 font-medium transition-colors duration-200"
            :class="{ 'text-primary-600': $route.name === 'home' }"
          >
            Home
          </RouterLink>
          <RouterLink 
            v-if="authStore.isAuthenticated" 
            to="/dashboard" 
            class="text-slate-600 hover:text-primary-600 font-medium transition-colors duration-200"
            :class="{ 'text-primary-600': $route.name === 'dashboard' }"
          >
            Dashboard
          </RouterLink>
        </div>

        <!-- Auth Buttons -->
        <div class="flex items-center space-x-4">
          <template v-if="!authStore.isAuthenticated">
            <RouterLink 
              to="/auth" 
              class="text-slate-600 hover:text-primary-600 font-medium transition-colors duration-200"
            >
              Sign In
            </RouterLink>
            <RouterLink 
              to="/auth" 
              class="btn-primary"
            >
              Get Started
            </RouterLink>
          </template>
          <template v-else>
            <button 
              @click="handleSignOut"
              class="text-slate-600 hover:text-red-600 font-medium transition-colors duration-200"
            >
              Sign Out
            </button>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleSignOut = async () => {
  await authStore.signOut()
  router.push('/')
}
</script>