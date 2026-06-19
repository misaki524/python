import { ref, computed } from 'vue'

// 月送りナビゲーション（複数 View で重複していた currentYM / displayMonth / changeMonth を共通化）
export function useMonthNav() {
  const today = new Date()
  const currentYM = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)

  const displayMonth = computed(() => {
    const [y, m] = currentYM.value.split('-')
    return `${y}年${parseInt(m)}月`
  })

  function changeMonth(delta) {
    const [y, m] = currentYM.value.split('-').map(Number)
    const d = new Date(y, m - 1 + delta, 1)
    currentYM.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
  }

  return { currentYM, displayMonth, changeMonth }
}
