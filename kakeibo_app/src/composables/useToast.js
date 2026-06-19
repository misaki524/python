import { reactive } from 'vue'

// アプリ全体で共有するトースト一覧（シングルトン）。ToastHost.vue が描画する。
export const toasts = reactive([])
let nextId = 1

function push(message, type = 'info', duration = 3200) {
  const id = nextId++
  toasts.push({ id, message, type })
  if (duration > 0) setTimeout(() => dismiss(id), duration)
  return id
}

export function dismiss(id) {
  const i = toasts.findIndex((t) => t.id === id)
  if (i !== -1) toasts.splice(i, 1)
}

// どこからでも `const toast = useToast()` で通知を出せる
export function useToast() {
  return {
    show: (message, type = 'info') => push(message, type),
    success: (message) => push(message, 'success'),
    error: (message) => push(message, 'error', 5000), // エラーは少し長めに表示
    info: (message) => push(message, 'info'),
    dismiss,
  }
}
