<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { LeaderboardEntry } from '@/types/user'
import { fetchLeaderboard } from '@/services/userApi'
import LeaderboardRow from '@/components/LeaderboardRow.vue'

const entries = ref<LeaderboardEntry[]>([])
const isLoading = ref(false)
const error = ref('')

async function load() {
  isLoading.value = true
  error.value = ''
  try {
    entries.value = await fetchLeaderboard()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load leaderboard'
  } finally {
    isLoading.value = false
  }
}

onMounted(load)
</script>

<template>
  <div class="leaderboard-view">
    <h2 class="lb-title">HIGH SCORES</h2>

    <p v-if="error" class="error-msg">! ERROR: {{ error }}</p>
    <p v-if="isLoading" class="loading-msg">LOADING<span class="blink">...</span></p>

    <div v-if="!isLoading && entries.length > 0" class="lb-list">
      <LeaderboardRow v-for="entry in entries" :key="entry.id" :entry="entry" />
    </div>

    <p v-if="!isLoading && entries.length === 0 && !error" class="empty-msg">
      NO PLAYERS YET. CREATE A USER TO BEGIN!
    </p>
  </div>
</template>

<style scoped>
.leaderboard-view {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.lb-title {
  font-size: 14px;
  color: var(--color-yellow);
  text-shadow: 2px 2px 0 rgba(255, 187, 119, 0.3);
  letter-spacing: 3px;
  text-align: center;
  padding: 12px;
  border: 2px solid var(--color-yellow);
  background: var(--color-bg-soft);
  box-shadow: var(--shadow-pixel);
}

.lb-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.error-msg {
  color: var(--color-danger);
  font-size: 8px;
  padding: 8px;
  border: 2px solid var(--color-danger);
  background: var(--color-danger-soft);
}

.loading-msg,
.empty-msg {
  text-align: center;
  color: var(--color-text-dim);
  font-size: 9px;
  padding: 2rem 0;
}

.blink {
  animation: blink-anim 1s step-start infinite;
}

@keyframes blink-anim {
  50% { opacity: 0.5; }
}

.empty-msg {
  color: var(--color-yellow);
  border: 2px dashed var(--color-border);
  padding: 1.5rem;
}
</style>
