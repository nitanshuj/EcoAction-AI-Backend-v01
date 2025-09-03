<template>
  <div class="card group hover:scale-105 transition-all duration-300">
    <div class="flex items-start justify-between mb-4">
      <div>
        <h3 class="text-lg font-semibold text-slate-800 mb-2">{{ challenge.title }}</h3>
        <p class="text-slate-600 text-sm">{{ challenge.description }}</p>
      </div>
      <div class="text-right">
        <div class="text-sm text-slate-500">{{ challenge.daysLeft }} days left</div>
        <div class="text-xs text-primary-600 font-medium">{{ challenge.participants }} participants</div>
      </div>
    </div>

    <div class="mb-4">
      <div class="flex justify-between text-sm mb-2">
        <span class="text-slate-600">Progress</span>
        <span class="font-medium text-slate-800">{{ challenge.progress }}%</span>
      </div>
      <div class="bg-slate-200 rounded-full h-2">
        <div 
          class="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full transition-all duration-500"
          :style="{ width: `${challenge.progress}%` }"
        ></div>
      </div>
    </div>

    <div class="flex items-center justify-between">
      <div class="text-sm">
        <span class="text-slate-500">Reward: </span>
        <span class="font-medium text-green-600">{{ challenge.reward }}</span>
      </div>
      <button class="text-primary-600 hover:text-primary-700 font-medium text-sm transition-colors duration-200">
        View Details →
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
</script>