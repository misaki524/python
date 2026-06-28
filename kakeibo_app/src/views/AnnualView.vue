<template>
  <div>
    <div class="month-nav">
      <button @click="changeYear(-1)">&lt;</button>
      <span>{{ year }}年</span>
      <button @click="changeYear(1)">&gt;</button>
    </div>

    <div v-if="!configured" class="card">
      <div class="empty-state">
        Google Sheets接続が未設定です。<br />
        「設定」タブでGAS URLを設定すると、月別の支出が表示されます。
      </div>
    </div>

    <div v-else-if="loading" class="card">
      <div class="empty-state">読み込み中...</div>
    </div>

    <template v-else>
      <div class="card">
        <div class="summary-row total">
          <span>年間支出合計</span>
          <span class="amount-negative">{{ yearTotal.toLocaleString() }}円</span>
        </div>
        <div class="summary-row">
          <span>月平均（支出のあった月）</span>
          <span>{{ monthlyAvg.toLocaleString() }}円</span>
        </div>
      </div>

      <div class="card">
        <h2 class="page-title">月別支出</h2>
        <canvas v-if="yearTotal > 0" ref="chartEl"></canvas>
        <div v-else class="empty-state">支出データがありません</div>
      </div>

      <div class="card">
        <h2 class="page-title">カテゴリ別 月別一覧</h2>
        <div v-if="!categoryRows.length" class="empty-state">支出データがありません</div>
        <div v-else style="overflow-x: auto">
          <table class="annual-table">
            <thead>
              <tr>
                <th class="sticky-col">カテゴリ</th>
                <th v-for="m in 12" :key="m">{{ m }}月</th>
                <th class="total-col">合計</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in categoryRows" :key="row.name">
                <td class="sticky-col">
                  <span class="dot" :style="{ background: getCategoryColor(row.name) }"></span>
                  {{ getCategoryIcon(row.name) }} {{ row.name }}
                </td>
                <td v-for="(v, i) in row.months" :key="i" class="num">
                  <span v-if="v">{{ v.toLocaleString() }}</span>
                  <span v-else class="zero">·</span>
                </td>
                <td class="num total-col">{{ row.total.toLocaleString() }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td class="sticky-col">月合計</td>
                <td v-for="(v, i) in monthlyTotals" :key="i" class="num">
                  <span v-if="v">{{ v.toLocaleString() }}</span>
                  <span v-else class="zero">·</span>
                </td>
                <td class="num total-col">{{ yearTotal.toLocaleString() }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { getExpenses, isConfigured } from '../services/sheets-api'
import { getCategoryColor, getCategoryIcon } from '../utils/categories'
import { useAsync } from '../composables/useAsync'

Chart.register(...registerables)

const { loading, run } = useAsync()

const configured = ref(isConfigured())
const year = ref(new Date().getFullYear())
const monthsData = ref(Array.from({ length: 12 }, () => [])) // 各月の支出配列
const chartEl = ref(null)
let chartInstance = null

function changeYear(delta) {
  year.value += delta
}

const monthlyTotals = computed(() =>
  monthsData.value.map((list) => list.reduce((s, e) => s + Number(e.amount || 0), 0))
)
const yearTotal = computed(() => monthlyTotals.value.reduce((s, v) => s + v, 0))
const monthlyAvg = computed(() => {
  const active = monthlyTotals.value.filter((v) => v > 0).length
  return active ? Math.round(yearTotal.value / active) : 0
})

// カテゴリ × 月（12列）のマトリクス。年間合計の多い順に並べる。
const categoryRows = computed(() => {
  const map = new Map()
  monthsData.value.forEach((list, mi) => {
    for (const e of list) {
      const cat = e.category || '未分類'
      if (!map.has(cat)) map.set(cat, Array(12).fill(0))
      map.get(cat)[mi] += Number(e.amount || 0)
    }
  })
  return [...map.entries()]
    .map(([name, months]) => ({ name, months, total: months.reduce((s, v) => s + v, 0) }))
    .sort((a, b) => b.total - a.total)
})

function renderChart() {
  if (!chartEl.value) return
  if (chartInstance) chartInstance.destroy()
  chartInstance = new Chart(chartEl.value, {
    type: 'bar',
    data: {
      labels: Array.from({ length: 12 }, (_, i) => `${i + 1}月`),
      datasets: [{ label: '支出', data: monthlyTotals.value, backgroundColor: '#4f46e5', borderRadius: 4 }],
    },
    options: {
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true, ticks: { callback: (v) => '¥' + Number(v).toLocaleString() } } },
    },
  })
}

async function fetchYear() {
  configured.value = isConfigured()
  if (!configured.value) return
  await run(
    async () => {
      const results = await Promise.all(
        Array.from({ length: 12 }, (_, i) =>
          getExpenses(`${year.value}-${String(i + 1).padStart(2, '0')}`)
        )
      )
      monthsData.value = results.map((r) => r || [])
    },
    { errorMessage: 'データの取得に失敗しました' }
  )
  await nextTick()
  renderChart()
}

watch(year, fetchYear)
onMounted(fetchYear)
onUnmounted(() => {
  if (chartInstance) chartInstance.destroy()
})
</script>

<style scoped>
.annual-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.78rem;
  white-space: nowrap;
}
.annual-table th,
.annual-table td {
  padding: 0.4rem 0.5rem;
  border-bottom: 1px solid var(--border);
  text-align: right;
}
.annual-table thead th {
  color: var(--text-muted);
  font-weight: 600;
}
.annual-table .num {
  font-variant-numeric: tabular-nums;
}
.annual-table .total-col {
  font-weight: 700;
}
.annual-table tfoot td {
  font-weight: 700;
  border-top: 2px solid var(--border);
  border-bottom: none;
}
.annual-table .zero {
  color: var(--border);
}
/* カテゴリ列は横スクロール時に固定 */
.sticky-col {
  position: sticky;
  left: 0;
  text-align: left !important;
  background: var(--surface);
  z-index: 1;
}
.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-right: 4px;
  vertical-align: middle;
}
</style>
