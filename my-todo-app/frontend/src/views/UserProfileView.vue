<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import type { User, UserStats } from '@/types/user'
import type { Todo } from '@/types/todo'
import { fetchUser, fetchUserTodos, fetchUserStats } from '@/services/userApi'
import TodoItem from '@/components/TodoItem.vue'
import TodoStats from '@/components/TodoStats.vue'
import XpBar from '@/components/XpBar.vue'
import StreakBadge from '@/components/StreakBadge.vue'
import AchievementGrid from '@/components/AchievementGrid.vue'

const route = useRoute()

const user = ref<User | null>(null)
const todos = ref<Todo[]>([])
const stats = ref<UserStats | null>(null)
const isLoading = ref(false)
const error = ref('')

async function loadProfile(id: number) {
  isLoading.value = true
  error.value = ''
  try {
    const [userData, todosData, statsData] = await Promise.all([
      fetchUser(id),
      fetchUserTodos(id),
      fetchUserStats(id),
    ])
    user.value = userData
    todos.value = todosData
    stats.value = statsData
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load profile'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadProfile(Number(route.params.id))
})

watch(() => route.params.id, (newId) => {
  if (newId) loadProfile(Number(newId))
})
</script>

<template>
  <div class="profile-view">
    <p v-if="error" class="error-msg">! ERROR: {{ error }}</p>
    <p v-if="isLoading" class="loading-msg">LOADING<span class="blink">...</span></p>

    <template v-if="!isLoading && user">
      <div class="profile-card">
        <div class="profile-header">
          <span class="profile-icon">{{ user.avatar || '☺' }}</span>
          <div class="profile-info">
            <h2 class="profile-name">{{ user.username }}</h2>
            <p class="profile-email">{{ user.email }}</p>
          </div>
        </div>
        <div class="profile-id">ID: {{ user.id }}</div>
      </div>

      <template v-if="stats">
        <XpBar
          :xp="stats.xp"
          :xp-in-level="stats.xp_in_level"
          :xp-for-level="stats.xp_for_level"
          :level="stats.level"
        />
        <div class="stats-row">
          <StreakBadge :streak="stats.current_streak" />
          <span class="stat-item">COMPLETED: {{ stats.total_completed }}</span>
          <span class="stat-item">MAX STREAK: {{ stats.max_streak }}</span>
        </div>
        <h3 class="section-title">ACHIEVEMENTS</h3>
        <AchievementGrid :achievements="stats.achievements" />
      </template>

      <h3 class="section-title">&#9876; ASSIGNED QUESTS</h3>
      <TodoStats :todos="todos" />

      <TransitionGroup name="list" tag="div" class="todo-list" v-if="todos.length > 0">
        <TodoItem v-for="todo in todos" :key="todo.id" :todo="todo" />
      </TransitionGroup>

      <p v-if="todos.length === 0" class="empty-msg">
        NO QUESTS ASSIGNED TO THIS PLAYER.
      </p>
    </template>
  </div>
</template>

<style scoped>
.profile-view {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.profile-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 12px;
}

.profile-icon {
  font-size: 24px;
  color: var(--color-cyan);
}

.profile-name {
  font-size: 12px;
  color: var(--color-accent);
  text-shadow: 2px 2px 0 rgba(255, 95, 160, 0.3);
  letter-spacing: 2px;
}

.profile-email {
  font-size: 8px;
  color: var(--color-text-dim);
  margin-top: 4px;
}

.profile-id {
  font-size: 7px;
  color: var(--color-text-dim);
  border: 2px solid var(--color-border);
  padding: 4px 8px;
  background: var(--color-bg);
}

.stats-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
}

.stat-item {
  font-size: 7px;
  color: var(--color-text-dim);
}

.section-title {
  font-size: 10px;
  color: var(--color-yellow);
  text-shadow: 0 0 8px rgba(255, 187, 119, 0.4);
  letter-spacing: 2px;
  margin-top: 8px;
}

.todo-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  position: relative;
}

.error-msg {
  color: var(--color-danger);
  font-size: 8px;
  padding: 8px;
  border: 2px solid var(--color-danger);
  background: var(--color-danger-soft);
  animation: blink-anim 1s step-start infinite;
}

@keyframes blink-anim {
  50% { opacity: 0.5; }
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

.empty-msg {
  color: var(--color-yellow);
  border: 2px dashed var(--color-border);
  padding: 1.5rem;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.15s steps(3);
}

.list-enter-from {
  opacity: 0;
  transform: translateY(-8px);
}

.list-leave-to {
  opacity: 0;
  transform: translateX(16px);
}

.list-leave-active {
  position: absolute;
  width: 100%;
}
</style>
