import { ref, computed } from 'vue'
import type { Todo, CreateTodoPayload, UpdateTodoPayload, SortOption } from '@/types/todo'
import * as api from '@/services/todoApi'
import { useGamification } from './useGamification'

const todos = ref<Todo[]>([])
const searchQuery = ref('')
const filterCategory = ref('')
const sortBy = ref<SortOption>('manual')
const isLoading = ref(false)
const error = ref('')

const filteredTodos = computed(() => {
  let result = todos.value

  if (filterCategory.value) {
    result = result.filter((t) => t.category === filterCategory.value)
  }

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter((t) => t.title.toLowerCase().includes(q))
  }

  if (sortBy.value === 'newest') {
    result = [...result].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )
  } else if (sortBy.value === 'oldest') {
    result = [...result].sort(
      (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
    )
  } else if (sortBy.value === 'title') {
    result = [...result].sort((a, b) => a.title.localeCompare(b.title))
  } else if (sortBy.value === 'priority') {
    const order: Record<string, number> = { High: 0, Medium: 1, Low: 2 }
    result = [...result].sort((a, b) => (order[a.priority] ?? 3) - (order[b.priority] ?? 3))
  } else if (sortBy.value === 'manual') {
    result = [...result].sort((a, b) => a.position - b.position)
  }

  return result
})

const totalCount = computed(() => {
  if (filterCategory.value) {
    return todos.value.filter((t) => t.category === filterCategory.value).length
  }
  return todos.value.length
})

const completedCount = computed(() => {
  if (filterCategory.value) {
    return todos.value.filter((t) => t.category === filterCategory.value && t.completed).length
  }
  return todos.value.filter((t) => t.completed).length
})

async function loadTodos() {
  isLoading.value = true
  error.value = ''
  try {
    todos.value = await api.fetchTodos()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load todos'
  } finally {
    isLoading.value = false
  }
}

async function addTodo(payload: CreateTodoPayload) {
  error.value = ''
  try {
    const todo = await api.createTodo(payload)
    todos.value.push(todo)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to add todo'
  }
}

async function toggleTodo(todo: Todo) {
  error.value = ''
  try {
    const response = await api.updateTodo(todo.id, { completed: !todo.completed })
    const { gamification, ...updated } = response
    const idx = todos.value.findIndex((t) => t.id === todo.id)
    if (idx !== -1) todos.value[idx] = updated
    if (gamification) {
      const { processGamificationResult } = useGamification()
      processGamificationResult(gamification)
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to toggle todo'
  }
}

async function editTodo(id: number, payload: UpdateTodoPayload) {
  error.value = ''
  try {
    const updated = await api.updateTodo(id, payload)
    const idx = todos.value.findIndex((t) => t.id === id)
    if (idx !== -1) todos.value[idx] = updated
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to update todo'
  }
}

async function reorderTodos(reordered: Todo[]) {
  error.value = ''
  try {
    const items = reordered.map((t, i) => ({ id: t.id, position: i }))
    await api.reorderTodos(items)
    for (const item of items) {
      const todo = todos.value.find((t) => t.id === item.id)
      if (todo) todo.position = item.position
    }
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to reorder todos'
  }
}

async function removeTodo(id: number) {
  error.value = ''
  try {
    await api.deleteTodo(id)
    todos.value = todos.value.filter((t) => t.id !== id)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to delete todo'
  }
}

export function useTodos() {
  return {
    todos,
    searchQuery,
    filterCategory,
    sortBy,
    isLoading,
    error,
    filteredTodos,
    totalCount,
    completedCount,
    loadTodos,
    addTodo,
    toggleTodo,
    editTodo,
    removeTodo,
    reorderTodos,
  }
}
