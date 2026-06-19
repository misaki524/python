<template>
  <div>
    <div class="month-nav">
      <button @click="changeMonth(-1)">&lt;</button>
      <span>{{ displayMonth }}</span>
      <button @click="changeMonth(1)">&gt;</button>
    </div>

    <!-- 収入入力 -->
    <div class="card">
      <h2 class="page-title">収入を追加</h2>
      <div class="form-group">
        <label>日付</label>
        <input type="date" v-model="form.dateStr" />
      </div>
      <div class="form-group">
        <label>収入元</label>
        <input type="text" v-model="form.source" placeholder="例: バイト給与、仕送り" />
      </div>
      <div class="form-group">
        <label>金額（円）</label>
        <input type="number" v-model.number="form.amount" inputmode="numeric" placeholder="0" />
      </div>
      <div class="form-group">
        <label>メモ</label>
        <input type="text" v-model="form.memo" placeholder="例: 6月分" />
      </div>
      <button class="btn btn-primary btn-block" @click="submitIncome" :disabled="saving">
        {{ saving ? '保存中...' : '保存' }}
      </button>
    </div>

    <!-- 収入一覧 -->
    <div class="card">
      <h2 class="page-title">収入一覧</h2>
      <div v-if="!incomes.length" class="empty-state">収入データがありません</div>
      <ul v-else class="expense-list">
        <li v-for="inc in incomes" :key="inc.income_id" class="expense-item">
          <div class="expense-info">
            <div class="expense-name">{{ inc.source }}</div>
            <div class="expense-meta">{{ inc.date_str }} {{ inc.memo }}</div>
          </div>
          <span class="expense-amount amount-positive">+{{ Number(inc.amount).toLocaleString() }}円</span>
          <button class="btn btn-danger btn-sm" @click="removeIncome(inc.income_id)">削除</button>
        </li>
      </ul>
      <div class="summary-row total" style="margin-top: 0.5rem">
        <span>収入合計</span>
        <span class="amount-positive">{{ totalIncome.toLocaleString() }}円</span>
      </div>
    </div>

    <!-- 収支計算① 収入 - 支出 -->
    <div class="card">
      <h2 class="page-title">収支バランス</h2>
      <div class="summary-row">
        <span>収入合計</span>
        <span class="amount-positive">{{ totalIncome.toLocaleString() }}円</span>
      </div>
      <div class="summary-row">
        <span>支出合計</span>
        <span class="amount-negative">-{{ totalExpense.toLocaleString() }}円</span>
      </div>
      <div class="summary-row total" :class="balance >= 0 ? 'amount-positive' : 'amount-negative'" style="font-size: 1.2rem">
        <span>{{ balance >= 0 ? '黒字' : '赤字' }}</span>
        <span>{{ (balance >= 0 ? '+' : '') }}{{ balance.toLocaleString() }}円</span>
      </div>
    </div>

    <!-- 収支計算② 収入 - 固定費内訳 -->
    <div class="card">
      <h2 class="page-title">固定費差引き計算</h2>
      <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.5rem">
        収入から主要な固定支出を差し引いた残額
      </p>
      <div class="summary-row" style="font-weight: 600">
        <span>収入合計</span>
        <span>{{ totalIncome.toLocaleString() }}円</span>
      </div>
      <div v-for="item in fixedBreakdown" :key="item.label" class="summary-row">
        <span>{{ item.label }}</span>
        <span class="amount-negative">-{{ item.amount.toLocaleString() }}円</span>
      </div>
      <div class="summary-row total" :class="fixedRemaining >= 0 ? 'amount-positive' : 'amount-negative'" style="font-size: 1.1rem">
        <span>残り（自由に使える金額）</span>
        <span>{{ fixedRemaining.toLocaleString() }}円</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getExpenses, getIncome, saveIncome, deleteIncome, isConfigured } from '../services/sheets-api'

const today = new Date()
const currentYM = ref(`${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}`)
const expenses = ref([])
const incomes = ref([])
const saving = ref(false)

const form = ref({
  dateStr: today.toISOString().slice(0, 10),
  source: '',
  amount: '',
  memo: '',
})

const displayMonth = computed(() => {
  const [y, m] = currentYM.value.split('-')
  return `${y}年${parseInt(m)}月`
})

const totalIncome = computed(() => incomes.value.reduce((s, e) => s + Number(e.amount), 0))
const totalExpense = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))
const balance = computed(() => totalIncome.value - totalExpense.value)

const fixedBreakdown = computed(() => {
  const cardTotal = sumByPayment('card')
  const dcardTotal = sumByPayment('dcard')
  const gasTotal = sumByCategoryNonCard('光熱費')
  const rentTotal = sumByCategoryNonCard('家賃')
  const loanTotal = sumByCategoryNonCard('ローン')
  const subTotal = sumByCategoryNonCard('サブスク')
  const phoneTotal = sumByCategoryNonCard('携帯電話')

  const countedIds = new Set()
  for (const e of expenses.value) {
    if (e.payment_method === 'card' || e.payment_method === 'dcard') countedIds.add(e.expense_id)
    if (['光熱費', '家賃', 'ローン', 'サブスク', '携帯電話'].includes(e.category) && e.payment_method !== 'card' && e.payment_method !== 'dcard') countedIds.add(e.expense_id)
  }
  const otherTotal = expenses.value
    .filter(e => !countedIds.has(e.expense_id))
    .reduce((s, e) => s + Number(e.amount), 0)

  return [
    { label: 'カード支払い', amount: cardTotal },
    { label: 'Dカード支払い', amount: dcardTotal },
    { label: '光熱費（ガス等）', amount: gasTotal },
    { label: '家賃', amount: rentTotal },
    { label: 'ローン', amount: loanTotal },
    { label: 'サブスク', amount: subTotal },
    { label: '携帯電話', amount: phoneTotal },
    { label: 'その他', amount: otherTotal },
  ].filter(i => i.amount > 0)
})

const fixedRemaining = computed(() => {
  const totalFixed = fixedBreakdown.value.reduce((s, i) => s + i.amount, 0)
  return totalIncome.value - totalFixed
})

function sumByPayment(method) {
  return expenses.value
    .filter(e => e.payment_method === method)
    .reduce((s, e) => s + Number(e.amount), 0)
}

function sumByCategoryNonCard(category) {
  return expenses.value
    .filter(e => e.category === category && e.payment_method !== 'card' && e.payment_method !== 'dcard')
    .reduce((s, e) => s + Number(e.amount), 0)
}

function changeMonth(delta) {
  const [y, m] = currentYM.value.split('-').map(Number)
  const d = new Date(y, m - 1 + delta, 1)
  currentYM.value = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

async function fetchData() {
  if (!isConfigured()) return
  try {
    expenses.value = await getExpenses(currentYM.value)
    incomes.value = await getIncome(currentYM.value)
  } catch (e) {
    console.error('Failed to fetch data:', e)
  }
}

async function submitIncome() {
  if (!form.value.source || !form.value.amount) return
  saving.value = true
  try {
    await saveIncome(form.value)
    form.value.source = ''
    form.value.amount = ''
    form.value.memo = ''
    await fetchData()
  } catch (e) {
    console.error('Failed to save income:', e)
    alert('保存に失敗しました: ' + e.message)
  } finally {
    saving.value = false
  }
}

async function removeIncome(id) {
  if (!confirm('削除しますか？')) return
  try {
    await deleteIncome(id)
    await fetchData()
  } catch (e) {
    console.error('Failed to delete income:', e)
  }
}

watch(currentYM, fetchData)
onMounted(fetchData)
</script>
