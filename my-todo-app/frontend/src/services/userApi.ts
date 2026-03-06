import type { User, CreateUserPayload, UserStats, LeaderboardEntry } from '@/types/user'
import type { Todo } from '@/types/todo'

const API_BASE = 'http://localhost:8002'

export async function fetchUsers(): Promise<User[]> {
  const res = await fetch(`${API_BASE}/users`)
  if (!res.ok) throw new Error('Failed to fetch users')
  return res.json()
}

export async function fetchUser(id: number): Promise<User> {
  const res = await fetch(`${API_BASE}/users/${id}`)
  if (!res.ok) throw new Error('Failed to fetch user')
  return res.json()
}

export async function fetchUserTodos(id: number): Promise<Todo[]> {
  const res = await fetch(`${API_BASE}/users/${id}/todos`)
  if (!res.ok) throw new Error('Failed to fetch user todos')
  return res.json()
}

export async function createUser(payload: CreateUserPayload): Promise<User> {
  const res = await fetch(`${API_BASE}/users`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to create user')
  return res.json()
}

export async function updateUser(id: number, payload: { avatar: string }): Promise<User> {
  const res = await fetch(`${API_BASE}/users/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to update user')
  return res.json()
}

export async function deleteUser(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/users/${id}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Failed to delete user')
}

export async function fetchUserStats(id: number): Promise<UserStats> {
  const res = await fetch(`${API_BASE}/users/${id}/stats`)
  if (!res.ok) throw new Error('Failed to fetch user stats')
  return res.json()
}

export async function fetchLeaderboard(): Promise<LeaderboardEntry[]> {
  const res = await fetch(`${API_BASE}/leaderboard`)
  if (!res.ok) throw new Error('Failed to fetch leaderboard')
  return res.json()
}

export async function fetchAchievements(): Promise<{ key: string; name: string; description: string; icon: string }[]> {
  const res = await fetch(`${API_BASE}/achievements`)
  if (!res.ok) throw new Error('Failed to fetch achievements')
  return res.json()
}
