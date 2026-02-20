import { ref } from 'vue'
import type { User, CreateUserPayload } from '@/types/user'
import * as api from '@/services/userApi'

const users = ref<User[]>([])
const isLoading = ref(false)
const error = ref('')

async function loadUsers() {
  isLoading.value = true
  error.value = ''
  try {
    users.value = await api.fetchUsers()
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to load users'
  } finally {
    isLoading.value = false
  }
}

async function addUser(payload: CreateUserPayload) {
  error.value = ''
  try {
    const user = await api.createUser(payload)
    users.value.push(user)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to add user'
  }
}

async function editUser(id: number, payload: { avatar: string }) {
  error.value = ''
  try {
    const updated = await api.updateUser(id, payload)
    const idx = users.value.findIndex((u) => u.id === id)
    if (idx !== -1) users.value[idx] = updated
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to update user'
  }
}

async function removeUser(id: number) {
  error.value = ''
  try {
    await api.deleteUser(id)
    users.value = users.value.filter((u) => u.id !== id)
  } catch (e) {
    error.value = e instanceof Error ? e.message : 'Failed to delete user'
  }
}

export function useUsers() {
  return {
    users,
    isLoading,
    error,
    loadUsers,
    addUser,
    editUser,
    removeUser,
  }
}
