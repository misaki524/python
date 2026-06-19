import { ref } from 'vue'
import { useToast } from './useToast'

// 各 View で重複していた「loading 切り替え + try/catch + 失敗時の通知」を集約する。
//
// 使い方:
//   const { loading, run } = useAsync()
//   await run(async () => { ... }, { errorMessage: '保存に失敗しました', successMessage: '保存しました' })
//
// - run() は fn 実行中 loading を true にする
// - fn が throw した場合は errorMessage（+ 例外メッセージ）をトースト表示し、例外は握りつぶす
//   → 成功時のみ後続処理を行いたい場合は、その処理を fn の中に書けば throw 時にスキップされる
// - successMessage 指定時は成功後にトースト表示
//
// 独立した複数の loading が必要な場合は useAsync() を複数回呼ぶ（例: 一覧用と保存用）。
export function useAsync() {
  const loading = ref(false)
  const toast = useToast()

  async function run(fn, { errorMessage, successMessage } = {}) {
    loading.value = true
    try {
      const result = await fn()
      if (successMessage) toast.success(successMessage)
      return result
    } catch (e) {
      console.error(e)
      const detail = e?.message || String(e)
      toast.error(errorMessage ? `${errorMessage}: ${detail}` : detail)
      return undefined
    } finally {
      loading.value = false
    }
  }

  return { loading, run }
}
