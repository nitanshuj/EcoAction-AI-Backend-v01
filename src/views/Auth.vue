<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-slate-50 to-primary-50">
    <div class="max-w-md w-full space-y-8 animate-fade-in">
      <div class="text-center">
        <h2 class="text-3xl font-bold text-slate-800 mb-2">
          {{ isSignUp ? 'Join EcoAction AI' : 'Welcome Back' }}
        </h2>
        <p class="text-slate-600">
          {{ isSignUp ? 'Start your climate action journey today' : 'Continue your environmental impact' }}
        </p>
      </div>

      <div class="card">
        <form @submit.prevent="handleSubmit" class="space-y-6">
          <div v-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {{ error }}
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-slate-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="input-field"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-slate-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              class="input-field"
              placeholder="Enter your password"
            />
          </div>

          <div v-if="isSignUp">
            <label for="name" class="block text-sm font-medium text-slate-700 mb-2">
              Full Name
            </label>
            <input
              id="name"
              v-model="form.name"
              type="text"
              required
              class="input-field"
              placeholder="Enter your full name"
            />
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
              Processing...
            </span>
            <span v-else>
              {{ isSignUp ? 'Create Account' : 'Sign In' }}
            </span>
          </button>
        </form>

        <div class="mt-6 text-center">
          <button
            @click="toggleMode"
            class="text-primary-600 hover:text-primary-700 font-medium transition-colors duration-200"
          >
            {{ isSignUp ? 'Already have an account? Sign in' : "Don't have an account? Sign up" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const isSignUp = ref(false)
const form = ref({
  email: '',
  password: '',
  name: ''
})

const loading = computed(() => authStore.loading)
const error = computed(() => authStore.error)

const toggleMode = () => {
  isSignUp.value = !isSignUp.value
  authStore.error = null
}

const handleSubmit = async () => {
  let result

  if (isSignUp.value) {
    result = await authStore.signUp(form.value.email, form.value.password, {
      full_name: form.value.name
    })
  } else {
    result = await authStore.signIn(form.value.email, form.value.password)
  }

  if (result.success) {
    if (isSignUp.value) {
      router.push('/onboarding')
    } else {
      router.push('/dashboard')
    }
  }
}
</script>