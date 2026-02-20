<script setup lang="ts">
import { onMounted } from 'vue'
import { useUsers } from '@/composables/useUsers'
import AddUser from '@/components/AddUser.vue'
import UserItem from '@/components/UserItem.vue'

const { users, isLoading, error, loadUsers } = useUsers()

onMounted(() => {
  loadUsers()
})
</script>

<template>
  <div class="users-view">
    <h2 class="section-title">&#9733; PLAYERS</h2>
    <AddUser />

    <p v-if="error" class="error-msg">! ERROR: {{ error }}</p>
    <p v-if="isLoading" class="loading-msg">LOADING<span class="blink">...</span></p>

    <TransitionGroup name="list" tag="div" class="user-list" v-if="!isLoading">
      <UserItem v-for="user in users" :key="user.id" :user="user" />
    </TransitionGroup>

    <p v-if="!isLoading && !error && users.length === 0" class="empty-msg">
      NO PLAYERS FOUND.<br />ADD ONE ABOVE TO BEGIN!
    </p>
  </div>
</template>

<style scoped>
.users-view {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.section-title {
  font-size: 11px;
  color: var(--color-cyan);
  text-shadow: 0 0 8px rgba(64, 232, 216, 0.4);
  letter-spacing: 2px;
}

.user-list {
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
