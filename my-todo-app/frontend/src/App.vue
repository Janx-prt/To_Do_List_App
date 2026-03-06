<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import GamificationToast from './components/GamificationToast.vue'
</script>

<template>
  <AppHeader />
  <main>
    <RouterView />
  </main>
  <GamificationToast />
</template>

<style scoped>
main {
  padding-top: 1rem;
}
</style>
