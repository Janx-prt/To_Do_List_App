<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Todo } from '@/types/todo'
import { useTodos } from '@/composables/useTodos'
import { useUsers } from '@/composables/useUsers'
import RetroSelect from '@/components/RetroSelect.vue'

const props = defineProps<{ todo: Todo }>()
const { toggleTodo, editTodo, removeTodo } = useTodos()
const { users, loadUsers } = useUsers()

const isEditing = ref(false)
const editTitle = ref('')
const editCategory = ref('')
const editPriority = ref('Low')
const editDueDate = ref('')
const editPlayer = ref('None')

const playerOptions = computed(() => ['None', ...users.value.map((u) => u.username)])

const assignedName = computed(() => {
  if (!props.todo.user_id) return null
  const user = users.value.find((u) => u.id === props.todo.user_id)
  return user ? user.username : null
})

const isOverdue = computed(() => {
  if (!props.todo.due_date || props.todo.completed) return false
  return new Date(props.todo.due_date) < new Date(new Date().toDateString())
})

const formattedDueDate = computed(() => {
  if (!props.todo.due_date) return null
  const d = new Date(props.todo.due_date)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
})

onMounted(() => {
  if (users.value.length === 0) loadUsers()
})

function startEdit() {
  editTitle.value = props.todo.title
  editCategory.value = props.todo.category
  editPriority.value = props.todo.priority || 'Low'
  editDueDate.value = props.todo.due_date ? props.todo.due_date.split('T')[0] : ''
  const user = users.value.find((u) => u.id === props.todo.user_id)
  editPlayer.value = user ? user.username : 'None'
  isEditing.value = true
}

async function saveEdit() {
  const trimmed = editTitle.value.trim()
  if (!trimmed) return
  const user = users.value.find((u) => u.username === editPlayer.value)
  await editTodo(props.todo.id, {
    title: trimmed,
    category: editCategory.value,
    priority: editPriority.value,
    due_date: editDueDate.value || null,
    user_id: user ? user.id : null,
  })
  isEditing.value = false
}

function cancelEdit() {
  isEditing.value = false
}

function categoryClass(category: string) {
  return `badge-${category.toLowerCase()}`
}

function priorityClass(priority: string) {
  return `badge-priority-${priority.toLowerCase()}`
}
</script>

<template>
  <div class="todo-item" :class="{ completed: todo.completed }">
    <template v-if="!isEditing">
      <label class="todo-main">
        <span
          class="pixel-check"
          :class="{ checked: todo.completed }"
          @click.prevent="toggleTodo(todo)"
        >
          <span v-if="todo.completed" class="check-mark">X</span>
          <span v-else class="check-empty">&nbsp;</span>
        </span>
        <span class="todo-title">{{ todo.title }}</span>
        <span class="badge" :class="categoryClass(todo.category)">{{ todo.category }}</span>
        <span class="badge" :class="priorityClass(todo.priority)">{{ todo.priority }}</span>
        <span v-if="formattedDueDate" class="due-date" :class="{ overdue: isOverdue }">{{ formattedDueDate }}</span>
        <span v-if="assignedName" class="badge badge-player">{{ assignedName }}</span>
      </label>
      <div class="todo-actions">
        <button class="btn-retro btn-edit" @click="startEdit" title="Edit">EDIT</button>
        <button class="btn-retro btn-delete" @click="removeTodo(todo.id)" title="Delete">DEL</button>
      </div>
    </template>
    <template v-else>
      <form class="edit-form" @submit.prevent="saveEdit">
        <input v-model="editTitle" class="retro-input" autofocus @keydown.esc="cancelEdit" />
        <RetroSelect v-model="editCategory" :options="['Personal', 'Work', 'Urgent']" />
        <RetroSelect v-model="editPriority" :options="['Low', 'Medium', 'High']" />
        <input v-model="editDueDate" type="date" class="retro-input retro-date" @keydown.esc="cancelEdit" />
        <RetroSelect v-model="editPlayer" :options="playerOptions" />
        <button type="submit" class="btn-retro btn-save">OK</button>
        <button type="button" class="btn-retro btn-cancel" @click="cancelEdit">ESC</button>
      </form>
    </template>
  </div>
</template>

<style scoped>
.todo-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--color-bg-card);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
  transition: border-color 0.1s;
  gap: 8px;
}

.todo-item:hover {
  border-color: var(--color-border-hover);
}

.todo-item.completed {
  opacity: 0.5;
  border-color: var(--color-border);
}

.todo-main {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  cursor: pointer;
  min-width: 0;
}

.pixel-check {
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-border-hover);
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  flex-shrink: 0;
  font-size: 10px;
  color: var(--color-accent);
  transition: all 0.1s;
}

.pixel-check.checked {
  border-color: var(--color-accent);
  background: var(--color-accent);
  color: var(--color-bg);
}

.pixel-check:hover {
  border-color: var(--color-accent);
  box-shadow: 0 0 6px var(--color-accent-glow);
}

.todo-title {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 9px;
}

.completed .todo-title {
  text-decoration: line-through;
  color: var(--color-text-dim);
}

.badge {
  font-size: 6px;
  padding: 3px 6px;
  border: 2px solid;
  text-transform: uppercase;
  letter-spacing: 1px;
  flex-shrink: 0;
}

.badge-personal {
  border-color: var(--category-personal);
  color: var(--category-personal);
}
.badge-work {
  border-color: var(--category-work);
  color: var(--category-work);
}
.badge-urgent {
  border-color: var(--category-urgent);
  color: var(--category-urgent);
  animation: blink 1.5s step-start infinite;
}
.badge-player {
  border-color: var(--color-magenta);
  color: var(--color-magenta);
}

.badge-priority-low {
  border-color: var(--priority-low);
  color: var(--priority-low);
}
.badge-priority-medium {
  border-color: var(--priority-medium);
  color: var(--priority-medium);
}
.badge-priority-high {
  border-color: var(--priority-high);
  color: var(--priority-high);
  animation: blink 1.5s step-start infinite;
}

.due-date {
  font-size: 6px;
  padding: 3px 6px;
  border: 2px solid #44dd44;
  color: #44dd44;
  text-transform: uppercase;
  letter-spacing: 1px;
  flex-shrink: 0;
}
.overdue {
  color: var(--color-danger);
  text-shadow: 0 0 6px var(--color-danger-soft);
}

@keyframes blink {
  50% { opacity: 0.4; }
}

.todo-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.btn-retro {
  font-family: var(--font-pixel);
  font-size: 7px;
  padding: 5px 8px;
  border: 2px solid;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.1s;
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
}

.btn-retro:active {
  box-shadow: none;
  transform: translate(2px, 2px);
}

.btn-edit {
  background: var(--color-bg);
  color: var(--color-cyan);
  border-color: var(--color-cyan);
}

.btn-edit:hover {
  background: var(--color-cyan);
  color: var(--color-bg);
}

.btn-delete {
  background: var(--color-bg);
  color: var(--color-danger);
  border-color: var(--color-danger);
}

.btn-delete:hover {
  background: var(--color-danger);
  color: var(--color-bg);
}

.btn-save {
  background: var(--color-accent);
  color: var(--color-bg);
  border-color: var(--color-accent-dim);
}

.btn-cancel {
  background: var(--color-bg-mute);
  color: var(--color-text);
  border-color: var(--color-border);
}

.btn-cancel:hover {
  border-color: var(--color-text-dim);
}

.edit-form {
  display: flex;
  gap: 6px;
  width: 100%;
  flex-wrap: wrap;
}

.retro-input {
  flex: 1;
  min-width: 100px;
  padding: 6px 8px;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-accent);
  font-size: 9px;
}

.retro-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 8px var(--color-accent-glow);
}

.retro-date {
  flex: 0 0 auto;
  width: 130px;
  font-family: var(--font-pixel);
  color-scheme: dark;
}
</style>
