<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
  modelValue: string
  options: string[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const open = ref(false)
const el = ref<HTMLElement | null>(null)

function toggle() {
  open.value = !open.value
}

function select(option: string) {
  emit('update:modelValue', option)
  open.value = false
}

function onClickOutside(e: MouseEvent) {
  if (el.value && !el.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('click', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('click', onClickOutside))
</script>

<template>
  <div class="retro-select" ref="el" :class="{ open }">
    <button type="button" class="select-trigger" @click="toggle">
      <span class="select-value">{{ modelValue }}</span>
      <span class="select-arrow">{{ open ? '▲' : '▼' }}</span>
    </button>
    <div v-if="open" class="select-dropdown">
      <button
        v-for="opt in options"
        :key="opt"
        type="button"
        class="select-option"
        :class="{ active: opt === modelValue }"
        @click="select(opt)"
      >
        <span class="option-marker">{{ opt === modelValue ? '►' : '&nbsp;' }}</span>
        {{ opt }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.retro-select {
  position: relative;
  display: inline-block;
}

.select-trigger {
  font-family: var(--font-pixel);
  font-size: 8px;
  padding: 6px 10px;
  background: var(--color-bg);
  color: var(--color-text);
  border: 2px solid var(--color-border);
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  transition: border-color 0.1s;
  width: 100%;
}

.select-trigger:hover {
  border-color: var(--color-border-hover);
}

.open .select-trigger {
  border-color: var(--color-cyan);
  box-shadow: 0 0 6px rgba(0, 221, 255, 0.3);
}

.select-arrow {
  font-size: 6px;
  color: var(--color-text-dim);
}

.select-dropdown {
  position: absolute;
  top: calc(100% + 2px);
  left: 0;
  right: 0;
  min-width: 100%;
  background: var(--color-bg);
  border: 2px solid var(--color-cyan);
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
  z-index: 100;
  display: flex;
  flex-direction: column;
}

.select-option {
  font-family: var(--font-pixel);
  font-size: 8px;
  padding: 6px 8px;
  background: none;
  color: var(--color-text);
  border: none;
  cursor: pointer;
  text-align: left;
  display: flex;
  align-items: center;
  gap: 4px;
  white-space: nowrap;
  transition: all 0.05s;
}

.select-option:hover {
  background: var(--color-bg-mute);
  color: var(--color-text-bright);
}

.select-option.active {
  color: var(--color-accent);
}

.option-marker {
  font-size: 7px;
  color: var(--color-accent);
  width: 10px;
}
</style>
