<script setup lang="ts">
import { onMounted } from 'vue'
import { useTodos } from '@/composables/useTodos'
import AddTodo from '@/components/AddTodo.vue'
import SearchFilterBar from '@/components/SearchFilterBar.vue'
import TodoStats from '@/components/TodoStats.vue'
import TodoItem from '@/components/TodoItem.vue'

const { filteredTodos, isLoading, error, filterCategory, loadTodos } = useTodos()

onMounted(() => {
  filterCategory.value = ''
  loadTodos()
})
</script>

<template>
  <div class="home-view">
    <AddTodo />
    <SearchFilterBar />
    <TodoStats />

    <p v-if="error" class="error-msg">! ERROR: {{ error }}</p>
    <p v-if="isLoading" class="loading-msg">LOADING<span class="blink">...</span></p>

    <TransitionGroup name="list" tag="div" class="todo-list" v-if="!isLoading">
      <TodoItem v-for="todo in filteredTodos" :key="todo.id" :todo="todo" />
    </TransitionGroup>

    <p v-if="!isLoading && !error && filteredTodos.length === 0" class="empty-msg">
      NO QUESTS FOUND.<br />ADD ONE ABOVE TO BEGIN!
    </p>
  </div>
</template>

<style scoped>
.home-view {
  display: flex;
  flex-direction: column;
  gap: 8px;
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
