export interface Todo {
  id: number
  title: string
  category: string
  completed: boolean
  created_at: string
  user_id: number | null
}

export interface CreateTodoPayload {
  title: string
  category: string
  user_id?: number | null
}

export interface UpdateTodoPayload {
  title?: string
  category?: string
  completed?: boolean
  user_id?: number | null
}

export type SortOption = 'newest' | 'oldest' | 'title'
