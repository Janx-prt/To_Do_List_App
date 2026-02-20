<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import type { User } from '@/types/user'
import { useUsers } from '@/composables/useUsers'

const props = defineProps<{ user: User }>()
const { editUser, removeUser } = useUsers()

const showPicker = ref(false)

const avatarOptions = ['⚔️', '🛡️', '🧙', '🧝', '🧛', '🧟', '🐉', '🎮', '👾', '🤖', '🦊', '🐺', '💀', '👑', '🔮', '🏹', '🦄', '🧚', '🦋', '🌸', '💖', '✨', '🧜', '🌙', '💎', '🎀', '🐱', '🌈', '🍓', '💫', '🪷', '🩰']

async function pickAvatar(emoji: string) {
  showPicker.value = false
  await editUser(props.user.id, { avatar: emoji })
}
</script>

<template>
  <div class="user-item">
    <div class="avatar-wrap">
      <button class="avatar-btn" @click.stop="showPicker = !showPicker" title="Change avatar">
        {{ user.avatar || '☺' }}
      </button>
      <div v-if="showPicker" class="avatar-grid">
        <button
          v-for="emoji in avatarOptions"
          :key="emoji"
          type="button"
          class="avatar-option"
          :class="{ active: emoji === user.avatar }"
          @click.stop="pickAvatar(emoji)"
        >{{ emoji }}</button>
      </div>
    </div>
    <RouterLink :to="`/users/${user.id}`" class="user-main">
      <span class="user-name">{{ user.username }}</span>
      <span class="user-email">{{ user.email }}</span>
    </RouterLink>
    <div class="user-actions">
      <button class="btn-retro btn-delete" @click="removeUser(user.id)" title="Delete">DEL</button>
    </div>
  </div>
</template>

<style scoped>
.user-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  background: var(--color-bg-card);
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-pixel);
  transition: border-color 0.1s;
  gap: 8px;
}

.user-item:hover {
  border-color: var(--color-border-hover);
}

.avatar-wrap {
  position: relative;
  flex-shrink: 0;
}

.avatar-btn {
  width: 28px;
  height: 28px;
  font-size: 16px;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color 0.1s;
}

.avatar-btn:hover {
  border-color: var(--color-accent);
  box-shadow: 0 0 6px var(--color-accent-glow);
}

.avatar-grid {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2px;
  padding: 6px;
  background: var(--color-bg);
  border: 2px solid var(--color-cyan);
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.5);
  z-index: 100;
}

.avatar-option {
  width: 32px;
  height: 32px;
  font-size: 16px;
  border: 2px solid transparent;
  background: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.05s;
}

.avatar-option:hover {
  background: var(--color-bg-mute);
  border-color: var(--color-border-hover);
}

.avatar-option.active {
  border-color: var(--color-accent);
  background: var(--color-bg-soft);
}

.user-main {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
  min-width: 0;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}

.user-main:hover .user-name {
  color: var(--color-accent);
  text-shadow: 0 0 6px var(--color-accent-glow);
}

.user-name {
  font-size: 9px;
  color: var(--color-text-bright);
  transition: all 0.1s;
}

.user-email {
  font-size: 7px;
  color: var(--color-text-dim);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-actions {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.btn-retro {
  font-family: var(--font-pixel);
  font-size: 7px;
  padding: 5px 8px;
  border: 2px solid;
  cursor: pointer;
  text-transform: uppercase;
  transition: all 0.1s;
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
}

.btn-retro:active {
  box-shadow: none;
  transform: translate(2px, 2px);
}

.btn-delete {
  background: var(--color-bg);
  color: var(--color-danger);
  border-color: var(--color-danger);
}

.btn-delete:hover {
  background: var(--color-danger);
  color: var(--color-bg);
}
</style>
