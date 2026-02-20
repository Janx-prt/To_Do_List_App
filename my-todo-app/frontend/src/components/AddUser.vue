<script setup lang="ts">
import { ref } from 'vue'
import { useUsers } from '@/composables/useUsers'

const { addUser } = useUsers()

const username = ref('')
const email = ref('')
const avatar = ref('⚔️')
const showPicker = ref(false)

const avatarOptions = ['⚔️', '🛡️', '🧙', '🧝', '🧛', '🧟', '🐉', '🎮', '👾', '🤖', '🦊', '🐺', '💀', '👑', '🔮', '🏹', '🦄', '🧚', '🦋', '🌸', '💖', '✨', '🧜', '🌙', '💎', '🎀', '🐱', '🌈', '🍓', '💫', '🪷', '🩰']

function pickAvatar(emoji: string) {
  avatar.value = emoji
  showPicker.value = false
}

async function handleSubmit() {
  const trimmedName = username.value.trim()
  const trimmedEmail = email.value.trim()
  if (!trimmedName || !trimmedEmail) return
  await addUser({ username: trimmedName, email: trimmedEmail, avatar: avatar.value })
  username.value = ''
  email.value = ''
  avatar.value = '⚔️'
}
</script>

<template>
  <form class="add-user" @submit.prevent="handleSubmit">
    <label class="input-label">&gt; NEW PLAYER:</label>
    <div class="input-row">
      <div class="avatar-picker-wrap">
        <button type="button" class="avatar-btn" @click="showPicker = !showPicker" title="Pick avatar">
          {{ avatar }}
        </button>
        <div v-if="showPicker" class="avatar-grid">
          <button
            v-for="emoji in avatarOptions"
            :key="emoji"
            type="button"
            class="avatar-option"
            :class="{ active: emoji === avatar }"
            @click="pickAvatar(emoji)"
          >{{ emoji }}</button>
        </div>
      </div>
      <input
        v-model="username"
        class="retro-input"
        placeholder="Enter username..."
      />
      <input
        v-model="email"
        class="retro-input"
        placeholder="Enter email..."
        type="email"
      />
      <button type="submit" class="btn-add">+ ADD</button>
    </div>
  </form>
</template>

<style scoped>
.add-user {
  background: var(--color-bg-soft);
  border: 2px solid var(--color-border);
  padding: 12px;
  box-shadow: var(--shadow-pixel);
}

.input-label {
  display: block;
  font-size: 8px;
  color: var(--color-accent);
  margin-bottom: 8px;
  text-shadow: 0 0 6px var(--color-accent-glow);
}

.input-row {
  display: flex;
  gap: 6px;
}

.retro-input {
  flex: 1;
  padding: 8px 10px;
  border: 2px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text-bright);
  font-size: 9px;
  caret-color: var(--color-accent);
}

.retro-input::placeholder {
  color: var(--color-text-dim);
}

.retro-input:focus {
  outline: none;
  border-color: var(--color-accent);
  box-shadow: 0 0 8px var(--color-accent-glow);
}

.avatar-picker-wrap {
  position: relative;
}

.avatar-btn {
  width: 36px;
  height: 36px;
  font-size: 18px;
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

.btn-add {
  font-family: var(--font-pixel);
  font-size: 8px;
  padding: 8px 14px;
  background: var(--color-accent);
  color: var(--color-bg);
  border: 2px solid var(--color-accent-dim);
  cursor: pointer;
  box-shadow: 3px 3px 0 rgba(0, 0, 0, 0.4);
  transition: all 0.1s;
  text-transform: uppercase;
}

.btn-add:hover {
  background: var(--color-yellow);
  border-color: #ccaa00;
  color: var(--color-bg);
}

.btn-add:active {
  box-shadow: none;
  transform: translate(3px, 3px);
}
</style>
