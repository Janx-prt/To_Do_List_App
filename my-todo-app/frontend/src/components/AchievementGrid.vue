<script setup lang="ts">
import type { Achievement } from '@/types/user'

defineProps<{
  achievements: Achievement[]
}>()
</script>

<template>
  <div class="achievement-grid">
    <div
      v-for="ach in achievements"
      :key="ach.key"
      class="achievement-card"
      :class="{ unlocked: ach.unlocked, locked: !ach.unlocked }"
      :title="ach.description"
    >
      <span class="ach-icon">{{ ach.icon }}</span>
      <span class="ach-name">{{ ach.name }}</span>
    </div>
  </div>
</template>

<style scoped>
.achievement-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
  gap: 6px;
}

.achievement-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 10px 6px;
  border: 2px solid var(--color-border);
  background: var(--color-bg-card);
  text-align: center;
  transition: all 0.15s;
}

.achievement-card.unlocked {
  border-color: var(--color-yellow);
  box-shadow: 0 0 10px rgba(255, 187, 119, 0.3);
}

.achievement-card.locked {
  opacity: 0.4;
  filter: grayscale(0.8);
}

.ach-icon {
  font-size: 20px;
}

.ach-name {
  font-size: 6px;
  color: var(--color-text);
  line-height: 1.6;
}

.achievement-card.unlocked .ach-name {
  color: var(--color-yellow);
}
</style>
