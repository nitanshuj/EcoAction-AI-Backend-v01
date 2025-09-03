<template>
  <nav class="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <RouterLink to="/" class="flex items-center space-x-2 group">
            <div class="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
              <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
              </svg>
            </div>
            <span class="text-xl font-bold text-slate-800 group-hover:text-primary-600 transition-colors duration-200">
              EcoAction AI
            </span>
          </RouterLink>
        </div>

        <!-- Navigation Links -->
        <div class="hidden md:flex items-center space-x-8">
          <RouterLink 
            v-if="!isAuthenticated" 
            to="/" 
            class="text-slate-600 hover:text-primary-600 font-medium transition-colors duration-200"
          >
            Home
          </RouterLink>
          <RouterLink 
            v-if="isAuthenticated" 
            to="/dashboard" 
            class="text-slate-600 hover:text-primary-600 font-medium transition-colors duration-200"
          >
            Dashboard
          </RouterLink>
        </div>

        <!-- Auth Buttons -->
        <div class="flex items-center space-x-4">
          <template v-if="!isAuthenticated">
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
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
                <span class="text-primary-700 font-semibold text-sm">
                  {{ user?.email?.charAt(0).toUpperCase() }}
                </span>
              </div>
              <button 
                @click="handleSignOut"
                class="text-slate-600 hover:text-red-600 font-medium transition-colors duration-200"
              >
                Sign Out
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isAuthenticated = computed(() => authStore.isAuthenticated)
const user = computed(() => authStore.user)

const handleSignOut = async () => {
  await authStore.signOut()
  router.push('/')
}
</script>