export interface User {
  id: number
  username: string
  email: string
  avatar: string
  xp: number
  level: number
  current_streak: number
  max_streak: number
  total_completed: number
}

export interface CreateUserPayload {
  username: string
  email: string
  avatar: string
}

export interface Achievement {
  key: string
  name: string
  description: string
  icon: string
  unlocked: boolean
  unlocked_at: string | null
}

export interface UserStats {
  xp: number
  level: number
  xp_in_level: number
  xp_for_level: number
  current_streak: number
  max_streak: number
  total_completed: number
  achievements: Achievement[]
}

export interface LeaderboardEntry {
  rank: number
  id: number
  username: string
  avatar: string
  xp: number
  level: number
  current_streak: number
  total_completed: number
  badge_count: number
}
