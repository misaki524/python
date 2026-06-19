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
      <div class="form-group">
        <label>月予算合計</label>
        <input type="number" v-model.number="budgetForm.total" inputmode="numeric" />
      </div>
      <div class="form-group">
        <label>食費</label>
        <input type="number" v-model.number="budgetForm.food" inputmode="numeric" />
      </div>
      <div class="form-group">
        <label>日用品</label>
        <input type="number" v-model.number="budgetForm.daily" inputmode="numeric" />
      </div>
      <div class="form-group">
        <label>交通費</label>
        <input type="number" v-model.number="budgetForm.transport" inputmode="numeric" />
      </div>
      <div class="form-group">
        <label>自由金</label>
        <input type="number" v-model.number="budgetForm.free" inputmode="numeric" />
      </div>
      <div class="form-group">
        <label>その他</label>
        <input type="number" v-model.number="budgetForm.other" inputmode="numeric" />
      </div>
      <button class="btn btn-primary btn-block" @click="submitBudget">保存</button>
    </div>

    <div class="card">
      <h2 class="page-title">カテゴリ別 予算消化</h2>
      <div v-for="item in budgetProgress" :key="item.category" style="margin-bottom: 0.75rem">
        <div class="summary-row" style="margin-bottom: 0.2rem">
          <span>{{ item.category }}</span>
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

const today = new Date()
const currentYM = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)
const expenses = ref([])

const budgetForm = ref({ total: 0, food: 0, daily: 0, transport: 0, free: 0, other: 0 })

const displayMonth = computed(() => {
  const [y, m] = currentYM.value.split('-')
  return `${y}年${parseInt(m)}月`
})

const totalSpent = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))

const monthRemain = computed(() => (budgetForm.value.total || 0) - totalSpent.value)
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

const budgetProgress = computed(() => {
  const mapping = [
    { category: '食費', budget: budgetForm.value.food, filter: '食費' },
    { category: '日用品', budget: budgetForm.value.daily, filter: '日用品' },
    { category: '交通費', budget: budgetForm.value.transport, filter: '交通費' },
    { category: '自由金', budget: budgetForm.value.free, filter: '自由金' },
    { category: 'その他', budget: budgetForm.value.other, filter: null },
  ]
  const tracked = ['食費', '日用品', '交通費', '自由金']
  return mapping.map(m => {
    const spent = m.filter
      ? expenses.value.filter(e => e.category === m.filter).reduce((s, e) => s + Number(e.amount), 0)
      : expenses.value.filter(e => !tracked.includes(e.category)).reduce((s, e) => s + Number(e.amount), 0)
    const budget = m.budget || 0
    return {
      category: m.category,
      budget,
      spent,
      percent: budget ? Math.round((spent / budget) * 100) : 0,
      over: budget > 0 && spent > budget,
    }
  })
})

function changeMonth(delta) {
  const [y, m] = currentYM.value.split('-').map(Number)
  const d = new Date(y, m - 1 + delta, 1)
  currentYM.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

async function fetchData() {
  if (!isConfigured()) return
  try {
    expenses.value = await getExpenses(currentYM.value)
    const b = await getBudget(currentYM.value)
    if (b) {
      budgetForm.value = {
        total: Number(b.budget_total) || 0,
        food: Number(b.budget_food) || 0,
        daily: Number(b.budget_daily) || 0,
        transport: Number(b.budget_transport) || 0,
        free: Number(b.budget_entertainment) || 0,
        other: Number(b.budget_other) || 0,
      }
    }
  } catch (e) {
    console.error('Failed to fetch budget data:', e)
  }
}

async function submitBudget() {
  try {
    await saveBudget(currentYM.value, budgetForm.value)
    alert('予算を保存しました')
  } catch (e) {
    console.error('Failed to save budget:', e)
    alert('保存に失敗しました')
  }
}

watch(currentYM, fetchData)
onMounted(fetchData)
</script>
