<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useTodos } from '@/composables/useTodos'
import { useUsers } from '@/composables/useUsers'
import RetroSelect from '@/components/RetroSelect.vue'

const { addTodo } = useTodos()
const { users, loadUsers } = useUsers()

const title = ref('')
const category = ref('Personal')
const selectedPlayer = ref('None')

const playerOptions = computed(() => ['None', ...users.value.map((u) => u.username)])

onMounted(() => {
  if (users.value.length === 0) loadUsers()
})

async function handleSubmit() {
  const trimmed = title.value.trim()
  if (!trimmed) return
  const user = users.value.find((u) => u.username === selectedPlayer.value)
  await addTodo({ title: trimmed, category: category.value, user_id: user ? user.id : null })
  title.value = ''
}
</script>

<template>
  <form class="add-todo" @submit.prevent="handleSubmit">
    <label class="input-label">&gt; NEW QUEST:</label>
    <div class="input-row">
      <input
        v-model="title"
        class="retro-input"
        placeholder="Enter quest name..."
        autofocus
      />
      <RetroSelect v-model="category" :options="['Personal', 'Work', 'Urgent']" />
      <RetroSelect v-model="selectedPlayer" :options="playerOptions" />
      <button type="submit" class="btn-add">+ ADD</button>
    </div>
  </form>
</template>

<style scoped>
.add-todo {
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  padding: 12px;
  box-shadow: var(--shadow-pixel);
}

.input-label {
  display: block;
  font-size: 8px;
  color: var(--color-accent);
  margin-bottom: 8px;
  text-shadow: 0 0 6px var(--color-accent-glow);
}

.input-row {
  display: flex;
  gap: 6px;
}

.retro-input {
  flex: 1;
  padding: 8px 10px;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text-bright);
  font-size: 9px;
  caret-color: var(--color-accent);
}

.retro-input::placeholder {
  color: var(--color-text-dim);
}

.retro-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 8px var(--color-accent-glow);
}

.btn-add {
  font-family: var(--font-pixel);
  font-size: 8px;
  padding: 8px 14px;
  background: var(--color-accent);
  color: var(--color-bg);
  border: 2px solid var(--color-accent-dim);
  cursor: pointer;
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
  transition: all 0.1s;
  text-transform: uppercase;
}

.btn-add:hover {
  background: var(--color-yellow);
  border-color: #ccaa00;
  color: var(--color-bg);
}

.btn-add:active {
  box-shadow: none;
  transform: translate(3px, 3px);
}
</style>
