export interface Todo {
  id: number
  title: string
  category: string
  priority: string
  due_date: string | null
  completed: boolean
  created_at: string
  user_id: number | null
  position: number
  completed_at: string | null
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
  position?: number
}

export interface GamificationResult {
  xp_earned: number
  total_xp: number
  level_up: boolean
  new_level: number
  new_achievements: { key: string; name: string; description: string; icon: string }[]
}

export interface TodoUpdateResponse extends Todo {
  gamification?: GamificationResult
}

export type SortOption = 'newest' | 'oldest' | 'title' | 'priority' | 'manual'
