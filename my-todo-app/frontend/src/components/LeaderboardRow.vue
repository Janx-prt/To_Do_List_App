<script setup lang="ts">
import { computed } from 'vue'
import type { LeaderboardEntry } from '@/types/user'

const props = defineProps<{
  entry: LeaderboardEntry
}>()

const rankClass = computed(() => {
  if (props.entry.rank === 1) return 'rank-gold'
  if (props.entry.rank === 2) return 'rank-silver'
  if (props.entry.rank === 3) return 'rank-bronze'
  return ''
})

const rankLabel = computed(() => {
  if (props.entry.rank === 1) return '1ST'
  if (props.entry.rank === 2) return '2ND'
  if (props.entry.rank === 3) return '3RD'
  return `${props.entry.rank}TH`
})
</script>

<template>
  <div class="lb-row" :class="rankClass">
    <span class="lb-rank">{{ rankLabel }}</span>
    <span class="lb-avatar">{{ entry.avatar }}</span>
    <span class="lb-name">{{ entry.username }}</span>
    <span class="lb-level">LV{{ entry.level }}</span>
    <span class="lb-xp">{{ entry.xp }} XP</span>
    <span class="lb-badges" v-if="entry.badge_count > 0">🏅{{ entry.badge_count }}</span>
  </div>
</template>

<style scoped>
.lb-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  background: var(--color-bg-card);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
}

.lb-row.rank-gold {
  border-color: var(--color-gold, #ffd700);
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.3);
}

.lb-row.rank-silver {
  border-color: var(--color-silver, #c0c0c0);
  box-shadow: 0 0 8px rgba(192, 192, 192, 0.25);
}

.lb-row.rank-bronze {
  border-color: var(--color-bronze, #cd7f32);
  box-shadow: 0 0 8px rgba(205, 127, 50, 0.25);
}

.lb-rank {
  font-size: 9px;
  color: var(--color-text-dim);
  min-width: 32px;
}

.rank-gold .lb-rank {
  color: var(--color-gold, #ffd700);
  text-shadow: 0 0 6px rgba(255, 215, 0, 0.5);
}

.rank-silver .lb-rank {
  color: var(--color-silver, #c0c0c0);
}

.rank-bronze .lb-rank {
  color: var(--color-bronze, #cd7f32);
}

.lb-avatar {
  font-size: 16px;
}

.lb-name {
  font-size: 9px;
  color: var(--color-text-bright);
  flex: 1;
}

.lb-level {
  font-size: 7px;
  color: var(--color-yellow);
  padding: 2px 6px;
  border: 1px solid var(--color-yellow);
}

.lb-xp {
  font-size: 8px;
  color: var(--color-cyan);
  min-width: 60px;
  text-align: right;
}

.lb-badges {
  font-size: 8px;
  color: var(--color-text-dim);
}
</style>
