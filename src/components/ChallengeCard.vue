<template>
  <div class="card group hover:shadow-lg transition-all duration-300">
    <div class="flex items-start justify-between mb-4">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-green-700 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200">
          <span class="text-xl">{{ challenge.icon || '🎯' }}</span>
        </div>
        <div>
          <h3 class="text-lg font-semibold text-slate-800">{{ challenge.title }}</h3>
          <p class="text-sm text-slate-500">{{ challenge.category }}</p>
        </div>
      </div>
      <span class="text-xs font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">
        {{ challenge.difficulty || 'Medium' }}
      </span>
    </div>

    <p class="text-slate-600 mb-4">{{ challenge.description }}</p>

    <!-- Progress Bar -->
    <div class="mb-4">
      <div class="flex items-center justify-between mb-2">
        <span class="text-sm font-medium text-slate-600">Progress</span>
        <span class="text-sm font-medium text-slate-600">{{ challenge.progress || 0 }}%</span>
      </div>
      <div class="w-full bg-slate-200 rounded-full h-2">
        <div 
          class="bg-gradient-to-r from-green-500 to-green-600 h-2 rounded-full transition-all duration-500"
          :style="{ width: `${challenge.progress || 0}%` }"
        ></div>
      </div>
    </div>

    <!-- Reward -->
    <div class="flex items-center justify-between">
      <div class="flex items-center space-x-2">
        <span class="text-sm text-slate-500">Reward:</span>
        <span class="text-sm font-medium text-primary-600">{{ challenge.reward || '50 EcoPoints' }}</span>
      </div>
      <button 
        @click="$emit('complete', challenge.id)"
        class="btn-primary text-sm"
        :disabled="(challenge.progress || 0) < 100"
      >
        {{ (challenge.progress || 0) >= 100 ? 'Complete' : 'Continue' }}
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  challenge: {
    type: Object,
    required: true
  }
})

defineEmits(['complete'])
</script>