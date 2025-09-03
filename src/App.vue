<template>
  <div id="app" class="min-h-screen bg-slate-50">
    <Navbar />
    <main class="flex-1">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/Navbar.vue'
</script>