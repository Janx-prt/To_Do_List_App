<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  xp: number
  xpInLevel: number
  xpForLevel: number
  level: number
}>()

const segments = 20

const percentage = computed(() => {
  if (props.xpForLevel <= 0) return 100
  return Math.round((props.xpInLevel / props.xpForLevel) * 100)
})

const filledSegments = computed(() => {
  return Math.round((percentage.value / 100) * segments)
})
</script>

<template>
  <div class="xp-bar-wrap">
    <span class="xp-level">LV {{ level }}</span>
    <div class="xp-bar">
      <span
        v-for="i in segments"
        :key="i"
        class="xp-segment"
        :class="i <= filledSegments ? 'filled' : 'empty'"
      ></span>
    </div>
    <span class="xp-text">{{ xpInLevel }}/{{ xpForLevel }} XP</span>
  </div>
</template>

<style scoped>
.xp-bar-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--color-bg-soft);
  border: 2px solid var(--color-yellow);
  box-shadow: var(--shadow-pixel);
}

.xp-level {
  font-size: 9px;
  color: var(--color-yellow);
  text-shadow: 0 0 8px rgba(255, 187, 119, 0.4);
  flex-shrink: 0;
  min-width: 48px;
}

.xp-bar {
  display: flex;
  gap: 2px;
  flex: 1;
}

.xp-segment {
  flex: 1;
  height: 12px;
  border: 1px solid rgba(0, 0, 0, 0.3);
}

.xp-segment.filled {
  background: var(--color-yellow);
  box-shadow: 0 0 4px rgba(255, 187, 119, 0.4);
}

.xp-segment.empty {
  background: var(--color-bg);
  border-color: var(--color-border);
}

.xp-text {
  font-size: 7px;
  color: var(--color-text-dim);
  flex-shrink: 0;
  min-width: 64px;
  text-align: right;
}
</style>
