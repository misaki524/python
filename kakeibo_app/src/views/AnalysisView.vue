<template>
  <div>
    <div class="month-nav">
      <button @click="changeMonth(-1)">&lt;</button>
      <span>{{ displayMonth }}</span>
      <button @click="changeMonth(1)">&gt;</button>
    </div>

    <div class="card">
      <h2 class="page-title">収支サマリー</h2>
      <div class="summary-row total" :class="balance >= 0 ? 'amount-positive' : 'amount-negative'">
        <span>{{ balance >= 0 ? '黒字' : '赤字' }}</span>
        <span>{{ (balance >= 0 ? '+' : '') }}{{ balance.toLocaleString() }}円</span>
      </div>
      <div class="summary-row">
        <span>収入合計</span>
        <span class="amount-positive">{{ totalIncome.toLocaleString() }}円</span>
      </div>
      <div class="summary-row">
        <span>支出合計</span>
        <span class="amount-negative">{{ totalExpense.toLocaleString() }}円</span>
      </div>
    </div>

    <div class="card">
      <h2 class="page-title">カテゴリ別支出</h2>
      <canvas ref="categoryChart"></canvas>
    </div>

    <div class="card">
      <h2 class="page-title">支払い方法別</h2>
      <canvas ref="paymentChart"></canvas>
    </div>

    <div class="card">
      <h2 class="page-title">節約日カウント</h2>
      <div style="font-size: 2rem; font-weight: 700; text-align: center; color: var(--success)">
        {{ noSpendDays }}日
      </div>
      <div style="text-align: center; color: var(--text-muted); font-size: 0.85rem">
        今月お金を使わなかった日
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { getExpenses, getIncome, isConfigured } from '../services/sheets-api'
import { getCategoryColor, PAYMENT_METHODS, getPaymentLabel } from '../utils/categories'

Chart.register(...registerables)

const today = new Date()
const currentYM = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)
const expenses = ref([])
const incomes = ref([])
const categoryChart = ref(null)
const paymentChart = ref(null)
let catChartInstance = null
let payChartInstance = null

const displayMonth = computed(() => {
  const [y, m] = currentYM.value.split('-')
  return `${y}年${parseInt(m)}月`
})

const totalExpense = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))
const totalIncome = computed(() => incomes.value.reduce((s, e) => s + Number(e.amount), 0))
const balance = computed(() => totalIncome.value - totalExpense.value)

const noSpendDays = computed(() => {
  const [y, m] = currentYM.value.split('-').map(Number)
  const daysInMonth = new Date(y, m, 0).getDate()
  const now = new Date()
  const maxDay = (now.getFullYear() === y && now.getMonth() + 1 === m) ? now.getDate() : daysInMonth
  const spendDays = new Set(expenses.value.map(e => e.date_str))
  let count = 0
  for (let d = 1; d <= maxDay; d++) {
    const ds = `${currentYM.value}-${String(d).padStart(2, '0')}`
    if (!spendDays.has(ds)) count++
  }
  return count
})

function changeMonth(delta) {
  const [y, m] = currentYM.value.split('-').map(Number)
  const d = new Date(y, m - 1 + delta, 1)
  currentYM.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

function renderCharts() {
  if (!categoryChart.value || !paymentChart.value) return

  const catData = {}
  for (const e of expenses.value) {
    catData[e.category] = (catData[e.category] || 0) + Number(e.amount)
  }
  const catLabels = Object.keys(catData)
  const catValues = Object.values(catData)
  const catColors = catLabels.map(l => getCategoryColor(l))

  if (catChartInstance) catChartInstance.destroy()
  catChartInstance = new Chart(categoryChart.value, {
    type: 'doughnut',
    data: {
      labels: catLabels,
      datasets: [{ data: catValues, backgroundColor: catColors }],
    },
    options: { plugins: { legend: { position: 'bottom' } } },
  })

  const pmData = {}
  for (const e of expenses.value) {
    const label = getPaymentLabel(e.payment_method)
    pmData[label] = (pmData[label] || 0) + Number(e.amount)
  }
  const pmLabels = Object.keys(pmData)
  const pmValues = Object.values(pmData)
  const pmColors = ['#22c55e', '#3b82f6', '#f59e0b', '#8b5cf6']

  if (payChartInstance) payChartInstance.destroy()
  payChartInstance = new Chart(paymentChart.value, {
    type: 'pie',
    data: {
      labels: pmLabels,
      datasets: [{ data: pmValues, backgroundColor: pmColors.slice(0, pmLabels.length) }],
    },
    options: { plugins: { legend: { position: 'bottom' } } },
  })
}

async function fetchData() {
  if (!isConfigured()) return
  try {
    expenses.value = await getExpenses(currentYM.value)
    incomes.value = await getIncome(currentYM.value)
    await nextTick()
    renderCharts()
  } catch (e) {
    console.error('Failed to fetch analysis data:', e)
  }
}

watch(currentYM, fetchData)
onMounted(fetchData)
</script>
