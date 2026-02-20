<script setup lang="ts">
import { onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useTodos } from '@/composables/useTodos'
import AddTodo from '@/components/AddTodo.vue'
import SearchFilterBar from '@/components/SearchFilterBar.vue'
import TodoStats from '@/components/TodoStats.vue'
import TodoItem from '@/components/TodoItem.vue'
import draggable from 'vuedraggable'

const route = useRoute()
const { filteredTodos, isLoading, error, filterCategory, sortBy, loadTodos, reorderTodos } =
  useTodos()

const dragEnabled = computed(() => sortBy.value === 'manual')

async function onDragEnd() {
  await reorderTodos(filteredTodos.value)
}

function syncCategory() {
  filterCategory.value = route.params.category as string
}

onMounted(() => {
  syncCategory()
  loadTodos()
})

watch(() => route.params.category, syncCategory)
</script>

<template>
  <div class="category-view">
    <AddTodo />
    <SearchFilterBar />
    <TodoStats />

    <p v-if="error" class="error-msg">! ERROR: {{ error }}</p>
    <p v-if="isLoading" class="loading-msg">LOADING<span class="blink">...</span></p>

    <draggable
      v-if="!isLoading && dragEnabled"
      :list="filteredTodos"
      item-key="id"
      handle=".drag-handle"
      class="todo-list"
      ghost-class="drag-ghost"
      @end="onDragEnd"
    >
      <template #item="{ element }">
        <TodoItem :todo="element" :show-handle="true" />
      </template>
    </draggable>

    <TransitionGroup
      v-else-if="!isLoading"
      name="list"
      tag="div"
      class="todo-list"
    >
      <TodoItem v-for="todo in filteredTodos" :key="todo.id" :todo="todo" :show-handle="false" />
    </TransitionGroup>

    <p v-if="!isLoading && !error && filteredTodos.length === 0" class="empty-msg">
      NO {{ (route.params.category as string).toUpperCase() }} QUESTS YET.
    </p>
  </div>
</template>

<style scoped>
.category-view {
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

.drag-ghost {
  opacity: 0.4;
  border-color: var(--color-cyan) !important;
  box-shadow: 0 0 8px rgba(0, 221, 255, 0.3);
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
