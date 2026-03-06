import { ref } from 'vue'
import type { GamificationResult } from '@/types/todo'

export interface GamificationNotification {
  id: number
  type: 'xp' | 'level_up' | 'achievement'
  message: string
  icon?: string
}

const notifications = ref<GamificationNotification[]>([])
let nextId = 0

function addNotification(notif: Omit<GamificationNotification, 'id'>) {
  const id = nextId++
  notifications.value.push({ ...notif, id })
  setTimeout(() => {
    notifications.value = notifications.value.filter((n) => n.id !== id)
  }, 4000)
}

function processGamificationResult(result: GamificationResult) {
  addNotification({
    type: 'xp',
    message: `+${result.xp_earned} XP`,
    icon: '⭐',
  })

  if (result.level_up) {
    setTimeout(() => {
      addNotification({
        type: 'level_up',
        message: `LEVEL UP! LV ${result.new_level}`,
        icon: '🎉',
      })
    }, 500)
  }

  result.new_achievements.forEach((ach, i) => {
    setTimeout(() => {
      addNotification({
        type: 'achievement',
        message: `${ach.name} unlocked!`,
        icon: ach.icon,
      })
    }, 1000 + i * 500)
  })
}

function dismissNotification(id: number) {
  notifications.value = notifications.value.filter((n) => n.id !== id)
}

export function useGamification() {
  return {
    notifications,
    processGamificationResult,
    dismissNotification,
  }
}
