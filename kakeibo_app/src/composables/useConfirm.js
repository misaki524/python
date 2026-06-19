import { reactive } from 'vue'

// 標準の window.confirm() を置き換える Promise ベースの確認ダイアログ。
// ConfirmDialog.vue が confirmState を描画し、ボタン押下で settleConfirm() を呼ぶ。
export const confirmState = reactive({
  open: false,
  message: '',
  confirmText: 'OK',
  cancelText: 'キャンセル',
  danger: false,
})

let resolver = null

export function useConfirm() {
  // confirm('本当に削除しますか？', { danger: true }) → Promise<boolean>
  function confirm(message, options = {}) {
    confirmState.message = message
    confirmState.confirmText = options.confirmText ?? 'OK'
    confirmState.cancelText = options.cancelText ?? 'キャンセル'
    confirmState.danger = options.danger ?? false
    confirmState.open = true
    return new Promise((resolve) => {
      resolver = resolve
    })
  }
  return { confirm }
}

// ConfirmDialog.vue 専用
export function settleConfirm(result) {
  confirmState.open = false
  if (resolver) {
    resolver(result)
    resolver = null
  }
}
