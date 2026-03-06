import type { Todo, CreateTodoPayload, UpdateTodoPayload, TodoUpdateResponse } from '@/types/todo'

const API_BASE = 'http://localhost:8002'

export async function fetchTodos(): Promise<Todo[]> {
  const res = await fetch(`${API_BASE}/todos`)
  if (!res.ok) throw new Error('Failed to fetch todos')
  return res.json()
}

export async function createTodo(payload: CreateTodoPayload): Promise<Todo> {
  const res = await fetch(`${API_BASE}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to create todo')
  return res.json()
}

export async function updateTodo(id: number, payload: UpdateTodoPayload): Promise<TodoUpdateResponse> {
  const res = await fetch(`${API_BASE}/todos/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
  if (!res.ok) throw new Error('Failed to update todo')
  return res.json()
}

export async function deleteTodo(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/todos/${id}`, {
    method: 'DELETE',
  })
  if (!res.ok) throw new Error('Failed to delete todo')
}

export async function reorderTodos(items: { id: number; position: number }[]): Promise<void> {
  const res = await fetch(`${API_BASE}/todos/reorder`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(items),
  })
  if (!res.ok) throw new Error('Failed to reorder todos')
}
