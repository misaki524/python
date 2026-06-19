<template>
  <div>
    <div class="month-nav">
      <button @click="changeWeek(-1)">&lt;</button>
      <span>{{ weekLabel }}</span>
      <button @click="changeWeek(1)">&gt;</button>
    </div>

    <div class="card">
      <div class="summary-row total">
        <span>週合計</span>
        <span>{{ total.toLocaleString() }}円</span>
      </div>
      <div class="summary-row">
        <span>1日あたり平均</span>
        <span>{{ dailyAvg.toLocaleString() }}円</span>
      </div>
    </div>

    <div class="card">
      <div v-if="loading" class="empty-state">読み込み中...</div>
      <div v-else-if="!expenses.length" class="empty-state">この週の支出はありません</div>
      <ul v-else class="expense-list">
        <li v-for="exp in expenses" :key="exp.expense_id" class="expense-item">
          <span class="expense-cat-dot" :style="{ background: getCategoryColor(exp.category) }"></span>
          <div class="expense-info">
            <div class="expense-name">
              {{ getCategoryIcon(exp.category) }} {{ exp.item_name || exp.category }}
              <span v-if="isCategoryDeleted(exp.category)" style="font-size: 0.7rem; color: var(--danger)">（削除された項目です）</span>
            </div>
            <div class="expense-meta">{{ exp.date_str }}</div>
          </div>
          <span class="expense-amount">{{ Number(exp.amount).toLocaleString() }}円</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getCategoryColor, getCategoryIcon, isCategoryDeleted } from '../utils/categories'
import { getExpenses, isConfigured } from '../services/sheets-api'
import { useAsync } from '../composables/useAsync'

const { loading, run } = useAsync()

function getMonday(d) {
  const date = new Date(d)
  const day = date.getDay()
  const diff = date.getDate() - day + (day === 0 ? -6 : 1)
  return new Date(date.setDate(diff))
}

function formatDate(d) {
  return d.toISOString().slice(0, 10)
}

const weekStart = ref(getMonday(new Date()))

const weekEnd = computed(() => {
  const d = new Date(weekStart.value)
  d.setDate(d.getDate() + 6)
  return d
})

const weekLabel = computed(() => {
  return `${formatDate(weekStart.value)} 〜 ${formatDate(weekEnd.value)}`
})

const expenses = ref([])
const total = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))
const dailyAvg = computed(() => (expenses.value.length ? Math.round(total.value / 7) : 0))

function changeWeek(delta) {
  const d = new Date(weekStart.value)
  d.setDate(d.getDate() + delta * 7)
  weekStart.value = d
}

async function fetchWeekly() {
  if (!isConfigured()) return
  await run(async () => {
    const start = formatDate(weekStart.value)
    const end = formatDate(weekEnd.value)
    const ym = start.slice(0, 7)
    const all = await getExpenses(ym)
    expenses.value = all
      .filter(e => e.date_str >= start && e.date_str <= end)
      .sort((a, b) => b.date_str.localeCompare(a.date_str))
  }, { errorMessage: 'データの取得に失敗しました' })
}

watch(weekStart, fetchWeekly)
onMounted(fetchWeekly)
</script>
