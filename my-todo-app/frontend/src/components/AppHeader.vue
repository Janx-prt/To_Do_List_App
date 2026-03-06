<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <header class="app-header">
    <h1 class="app-title">
MY QUESTS
    </h1>
    <nav class="nav-links">
      <RouterLink to="/" exact-active-class="active">ALL</RouterLink>
      <RouterLink to="/category/Personal" active-class="active">PERSONAL</RouterLink>
      <RouterLink to="/category/Work" active-class="active">WORK</RouterLink>
      <RouterLink to="/category/Urgent" active-class="active">URGENT</RouterLink>
      <span class="nav-sep">|</span>
      <RouterLink to="/users" active-class="active">PLAYERS</RouterLink>
      <RouterLink to="/leaderboard" active-class="active">SCORES</RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 1rem;
  background: var(--color-bg-soft);
  border: var(--pixel) solid var(--color-border);
  box-shadow: var(--shadow-pixel);
}

.app-title {
  font-size: 14px;
  color: var(--color-yellow);
  text-shadow: 2px 2px 0 rgba(255, 187, 119, 0.3);
  letter-spacing: 2px;
}

.title-icon {
  margin-right: 0.5rem;
}

.nav-links {
  display: flex;
  gap: 4px;
}

.nav-links a {
  padding: 6px 10px;
  font-size: 8px;
  color: var(--color-text-dim);
  border: 2px solid transparent;
  transition: all 0.1s;
  text-transform: uppercase;
}

.nav-links a:hover {
  color: var(--color-text-bright);
  border-color: var(--color-border-hover);
  text-shadow: 0 0 6px var(--color-cyan);
  background: none;
}

.nav-sep {
  color: var(--color-border);
  font-size: 8px;
  align-self: center;
}

.nav-links a.active {
  color: var(--color-bg);
  background: var(--color-accent);
  border-color: var(--color-accent);
  box-shadow: 2px 2px 0 rgba(0, 0, 0, 0.4);
  text-shadow: none;
}
</style>
