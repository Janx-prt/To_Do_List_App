<script setup lang="ts">
import { computed } from 'vue'
import type { Todo } from '@/types/todo'
import { useTodos } from '@/composables/useTodos'

const props = defineProps<{
  todos?: Todo[]
}>()

const globalTodos = useTodos()

const totalCount = computed(() => {
  if (props.todos) return props.todos.length
  return globalTodos.totalCount.value
})

const completedCount = computed(() => {
  if (props.todos) return props.todos.filter((t) => t.completed).length
  return globalTodos.completedCount.value
})

const percentage = computed(() => {
  if (totalCount.value === 0) return 0
  return Math.round((completedCount.value / totalCount.value) * 100)
})

const segments = 20

const filledSegments = computed(() => {
  return Math.round((percentage.value / 100) * segments)
})

const barColor = computed(() => {
  if (percentage.value >= 75) return 'bar-green'
  if (percentage.value >= 40) return 'bar-yellow'
  return 'bar-red'
})
</script>

<template>
  <div class="stats-panel">
    <span class="stats-label">PROGRESS:</span>
    <div class="hp-bar">
      <span
        v-for="i in segments"
        :key="i"
        class="hp-segment"
        :class="[i <= filledSegments ? barColor : 'bar-empty']"
      ></span>
    </div>
    <span class="stats-count">{{ completedCount }}/{{ totalCount }}</span>
    <span class="stats-pct">{{ percentage }}%</span>
  </div>
</template>

<style scoped>
.stats-panel {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
}

.stats-label {
  font-size: 7px;
  color: var(--color-magenta);
  flex-shrink: 0;
}

.hp-bar {
  display: flex;
  gap: 2px;
  flex: 1;
}

.hp-segment {
  flex: 1;
  height: 12px;
  border: 1px solid rgba(0, 0, 0, 0.3);
}

.bar-green {
  background: var(--color-accent);
  box-shadow: 0 0 4px var(--color-accent-glow);
}

.bar-yellow {
  background: var(--color-yellow);
  box-shadow: 0 0 4px rgba(255, 221, 0, 0.3);
}

.bar-red {
  background: var(--color-danger);
  box-shadow: 0 0 4px rgba(255, 68, 68, 0.3);
}

.bar-empty {
  background: var(--color-bg);
  border-color: var(--color-border);
}

.stats-count {
  font-size: 8px;
  color: var(--color-text);
  flex-shrink: 0;
}

.stats-pct {
  font-size: 8px;
  color: var(--color-yellow);
  flex-shrink: 0;
}
</style>
