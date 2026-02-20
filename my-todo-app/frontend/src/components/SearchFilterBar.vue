<script setup lang="ts">
import { useTodos } from '@/composables/useTodos'
import RetroSelect from '@/components/RetroSelect.vue'

const { searchQuery, sortBy } = useTodos()
</script>

<template>
  <div class="search-bar">
    <label class="search-label">SEARCH:</label>
    <input
      v-model="searchQuery"
      class="retro-input"
      placeholder="Type to filter..."
      type="search"
    />
    <label class="sort-label">SORT:</label>
    <RetroSelect v-model="sortBy" :options="['newest', 'oldest', 'title', 'priority']" />
  </div>
</template>

<style scoped>
.search-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
}

.search-label,
.sort-label {
  font-size: 7px;
  color: var(--color-cyan);
  flex-shrink: 0;
}

.retro-input {
  flex: 1;
  padding: 6px 8px;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text-bright);
  font-size: 8px;
  caret-color: var(--color-accent);
}

.retro-input::placeholder {
  color: var(--color-text-dim);
}

.retro-input:focus {
  outline: none;
  border-color: var(--color-cyan);
  box-shadow: 0 0 6px rgba(0, 221, 255, 0.3);
}

/* Remove default search cancel button */
.retro-input::-webkit-search-cancel-button {
  display: none;
}

</style>
