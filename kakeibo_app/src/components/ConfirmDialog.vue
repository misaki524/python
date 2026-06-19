<template>
  <Teleport to="body">
    <Transition name="confirm">
      <div v-if="confirmState.open" class="confirm-overlay" @click.self="settleConfirm(false)">
        <div class="card confirm-box" role="alertdialog" aria-modal="true">
          <p class="confirm-message">{{ confirmState.message }}</p>
          <div class="confirm-actions">
            <button class="btn confirm-cancel" @click="settleConfirm(false)">
              {{ confirmState.cancelText }}
            </button>
            <button
              class="btn"
              :class="confirmState.danger ? 'btn-danger' : 'btn-primary'"
              @click="settleConfirm(true)"
            >
              {{ confirmState.confirmText }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { confirmState, settleConfirm } from '../composables/useConfirm'
</script>

<style scoped>
.confirm-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 900;
  padding: 1rem;
}
.confirm-box {
  max-width: 400px;
  width: 100%;
  margin: 0;
}
.confirm-message {
  font-size: 0.95rem;
  line-height: 1.6;
  white-space: pre-line; /* メッセージ中の \n を改行として表示 */
  margin-bottom: 1.1rem;
}
.confirm-actions {
  display: flex;
  gap: 0.5rem;
}
.confirm-actions .btn {
  flex: 1;
}
.confirm-cancel {
  background: var(--border);
  color: var(--text);
}

.confirm-enter-active,
.confirm-leave-active {
  transition: opacity 0.2s ease;
}
.confirm-enter-from,
.confirm-leave-to {
  opacity: 0;
}
</style>
