<template>
  <div>
    <div class="month-nav">
      <button @click="changeMonth(-1)">&lt;</button>
      <span>{{ displayMonth }}</span>
      <button @click="changeMonth(1)">&gt;</button>
    </div>

    <div class="card">
      <h2 class="page-title">残り使える金額</h2>
      <div class="summary-row total" :class="monthRemain >= 0 ? 'amount-positive' : 'amount-negative'" style="font-size: 1.2rem">
        <span>月残額</span>
        <span>{{ monthRemain.toLocaleString() }}円</span>
      </div>
      <div class="summary-row">
        <span>週あたり</span>
        <span>{{ weekRemain.toLocaleString() }}円</span>
      </div>
      <div class="summary-row">
        <span>1日あたり</span>
        <span>{{ dayRemain.toLocaleString() }}円</span>
      </div>
    </div>

    <div class="card">
      <h2 class="page-title">予算設定</h2>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem">
        カテゴリごとに月予算を入力してください（合計が月予算になります）
      </p>
      <div v-for="cat in categories" :key="cat.name" class="budget-row">
        <label>{{ cat.icon }} {{ cat.name }}</label>
        <input type="number" v-model.number="budgets[cat.name]" inputmode="numeric" placeholder="0" />
      </div>
      <div class="summary-row total" style="margin-top: 0.75rem">
        <span>予算合計</span>
        <span>{{ totalBudget.toLocaleString() }}円</span>
      </div>
      <button class="btn btn-primary btn-block" @click="submitBudget" :disabled="saving" style="margin-top: 0.5rem">
        {{ saving ? '保存中...' : '保存' }}
      </button>
    </div>

    <div class="card">
      <h2 class="page-title">カテゴリ別 予算消化</h2>
      <div v-if="!visibleProgress.length" class="empty-state">予算・支出データがありません</div>
      <div v-for="item in visibleProgress" :key="item.category" style="margin-bottom: 0.75rem">
        <div class="summary-row" style="margin-bottom: 0.2rem">
          <span>{{ item.icon }} {{ item.category }}</span>
          <span :class="item.over ? 'amount-negative' : ''">
            {{ item.spent.toLocaleString() }} / {{ item.budget.toLocaleString() }}円
          </span>
        </div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{ width: Math.min(item.percent, 100) + '%', background: item.over ? 'var(--danger)' : 'var(--primary)' }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getExpenses, getBudget, saveBudget, isConfigured } from '../services/sheets-api'
import { getCategories } from '../utils/categories'
import { useMonthNav } from '../composables/useMonthNav'
import { useAsync } from '../composables/useAsync'

const { currentYM, displayMonth, changeMonth } = useMonthNav()
const { run } = useAsync()
const { loading: saving, run: runSave } = useAsync()

const expenses = ref([])
const categories = ref(getCategories())

// 現在のカテゴリ全てを 0 で初期化した予算オブジェクトを作る
function blankBudgets() {
  const o = {}
  for (const c of categories.value) o[c.name] = 0
  return o
}
const budgets = ref(blankBudgets())

const totalSpent = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))
const totalBudget = computed(() => Object.values(budgets.value).reduce((s, v) => s + Number(v || 0), 0))

const monthRemain = computed(() => totalBudget.value - totalSpent.value)
const daysInMonth = computed(() => {
  const [y, m] = currentYM.value.split('-').map(Number)
  return new Date(y, m, 0).getDate()
})
const daysRemaining = computed(() => {
  const [y, m] = currentYM.value.split('-').map(Number)
  const now = new Date()
  if (now.getFullYear() === y && now.getMonth() + 1 === m) {
    return Math.max(1, daysInMonth.value - now.getDate() + 1)
  }
  return daysInMonth.value
})
const weekRemain = computed(() => Math.round(monthRemain.value / Math.ceil(daysRemaining.value / 7)))
const dayRemain = computed(() => Math.round(monthRemain.value / daysRemaining.value))

const budgetProgress = computed(() => categories.value.map(c => {
  const budget = Number(budgets.value[c.name] || 0)
  const spent = expenses.value.filter(e => e.category === c.name).reduce((s, e) => s + Number(e.amount), 0)
  return {
    category: c.name,
    icon: c.icon,
    budget,
    spent,
    percent: budget ? Math.round((spent / budget) * 100) : 0,
    over: budget > 0 && spent > budget,
  }
}))
// 予算も支出も無いカテゴリは消化バーから省く
const visibleProgress = computed(() => budgetProgress.value.filter(i => i.budget > 0 || i.spent > 0))

async function fetchData() {
  if (!isConfigured()) return
  await run(async () => {
    expenses.value = await getExpenses(currentYM.value)
    const next = blankBudgets()
    const b = await getBudget(currentYM.value)
    if (b && b.budget_json) {
      try {
        const parsed = JSON.parse(b.budget_json)
        // 現在存在するカテゴリの予算のみ反映（削除済みカテゴリの値は無視）
        for (const k of Object.keys(parsed)) {
          if (k in next) next[k] = Number(parsed[k]) || 0
        }
      } catch (e) {
        console.warn('budget_json の解析に失敗（旧スキーマの可能性）:', e)
      }
    }
    budgets.value = next
  }, { errorMessage: 'データの取得に失敗しました' })
}

async function submitBudget() {
  await runSave(async () => {
    await saveBudget(currentYM.value, { total: totalBudget.value, budgets: budgets.value })
  }, { errorMessage: '保存に失敗しました', successMessage: '予算を保存しました' })
}

watch(currentYM, fetchData)
onMounted(fetchData)
</script>

<style scoped>
.budget-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}
.budget-row label {
  flex: 1;
  font-size: 0.9rem;
}
.budget-row input {
  width: 9rem;
}
</style>
