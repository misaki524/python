<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="toast-host">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast"
        :class="`toast-${t.type}`"
        role="status"
        @click="dismiss(t.id)"
      >
        <span class="toast-icon">{{ icon(t.type) }}</span>
        <span class="toast-msg">{{ t.message }}</span>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
import { toasts, dismiss } from '../composables/useToast'

function icon(type) {
  if (type === 'success') return '✓'
  if (type === 'error') return '✕'
  return 'ℹ'
}
</script>

<style scoped>
.toast-host {
  position: fixed;
  top: max(1rem, env(safe-area-inset-top));
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  width: calc(100% - 2rem);
  max-width: 420px;
  pointer-events: none;
}
.toast {
  pointer-events: auto;
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.7rem 0.9rem;
  border-radius: 10px;
  background: var(--surface);
  color: var(--text);
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.18);
  border-left: 4px solid var(--text-muted);
  font-size: 0.9rem;
  cursor: pointer;
}
.toast-success { border-left-color: var(--success); }
.toast-error { border-left-color: var(--danger); }
.toast-info { border-left-color: var(--primary); }
.toast-icon {
  flex-shrink: 0;
  width: 1.25rem;
  height: 1.25rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #fff;
  font-size: 0.75rem;
  background: var(--text-muted);
}
.toast-success .toast-icon { background: var(--success); }
.toast-error .toast-icon { background: var(--danger); }
.toast-info .toast-icon { background: var(--primary); }
.toast-msg { flex: 1; word-break: break-word; }

.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateY(-12px);
}
.toast-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
