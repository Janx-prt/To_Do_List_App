<script setup lang="ts">
defineProps<{
  streak: number
}>()
</script>

<template>
  <span v-if="streak > 0" class="streak-badge" :title="`${streak}-day streak`">
    <span class="streak-flame">🔥</span>
    <span class="streak-count">{{ streak }}</span>
  </span>
</template>

<style scoped>
.streak-badge {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 2px 6px;
  background: var(--color-bg);
  border: 2px solid var(--color-streak, #ff6600);
  font-size: 8px;
}

.streak-flame {
  font-size: 10px;
  animation: flicker 0.8s ease-in-out infinite alternate;
}

.streak-count {
  color: var(--color-streak, #ff6600);
  font-size: 8px;
}

@keyframes flicker {
  from { opacity: 0.8; transform: scale(1); }
  to { opacity: 1; transform: scale(1.1); }
}
</style>
