export interface Todo {
  id: number
  title: string
  category: string
  priority: string
  due_date: string | null
  completed: boolean
  created_at: string
  user_id: number | null
}

export interface CreateTodoPayload {
  title: string
  category: string
  priority?: string
  due_date?: string | null
  user_id?: number | null
}

export interface UpdateTodoPayload {
  title?: string
  category?: string
  priority?: string
  due_date?: string | null
  completed?: boolean
  user_id?: number | null
}

export type SortOption = 'newest' | 'oldest' | 'title' | 'priority'
