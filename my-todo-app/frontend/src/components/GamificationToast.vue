<script setup lang="ts">
import { useGamification } from '@/composables/useGamification'

const { notifications, dismissNotification } = useGamification()
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div
        v-for="notif in notifications"
        :key="notif.id"
        class="toast-item"
        :class="`toast-${notif.type}`"
        @click="dismissNotification(notif.id)"
      >
        <span class="toast-icon">{{ notif.icon }}</span>
        <span class="toast-msg">{{ notif.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 6px;
  pointer-events: none;
}

.toast-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
  cursor: pointer;
  pointer-events: auto;
  animation: toast-pulse 0.3s steps(3);
}

.toast-xp {
  border-color: var(--color-yellow);
}

.toast-level_up {
  border-color: var(--color-magenta);
  box-shadow: 0 0 12px rgba(255, 68, 204, 0.4);
}

.toast-achievement {
  border-color: var(--color-cyan);
  box-shadow: 0 0 12px rgba(64, 232, 216, 0.3);
}

.toast-icon {
  font-size: 14px;
}

.toast-msg {
  font-size: 8px;
  color: var(--color-text-bright);
  letter-spacing: 1px;
}

.toast-xp .toast-msg {
  color: var(--color-yellow);
}

.toast-level_up .toast-msg {
  color: var(--color-magenta);
  text-shadow: 0 0 6px rgba(255, 68, 204, 0.5);
}

.toast-achievement .toast-msg {
  color: var(--color-cyan);
}

@keyframes toast-pulse {
  0% { transform: translateX(20px); opacity: 0; }
  50% { transform: translateX(-4px); }
  100% { transform: translateX(0); opacity: 1; }
}

.toast-enter-active {
  animation: toast-pulse 0.3s steps(3);
}

.toast-leave-active {
  transition: all 0.2s steps(3);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(20px);
}
</style>
