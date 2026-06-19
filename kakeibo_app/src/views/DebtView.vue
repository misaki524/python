<template>
  <div>
    <div class="card">
      <h2 class="page-title">借金を登録</h2>
      <div class="form-group">
        <label>日付</label>
        <input type="date" v-model="form.dateStr" />
      </div>
      <div class="form-group">
        <label>借入先・相手</label>
        <input type="text" v-model="form.lender" placeholder="例: 友人A、消費者金融B" />
      </div>
      <div class="form-group">
        <label>金額（円）</label>
        <input type="number" v-model.number="form.amount" inputmode="numeric" placeholder="0" />
      </div>
      <div class="form-group">
        <label>メモ</label>
        <input type="text" v-model="form.memo" placeholder="例: ランチ代立替" />
      </div>
      <button class="btn btn-primary btn-block" @click="submitDebt">登録</button>
    </div>

    <!-- サマリー -->
    <div class="card">
      <div class="summary-row total amount-negative">
        <span>未返済合計</span>
        <span>{{ unpaidTotal.toLocaleString() }}円</span>
      </div>
      <div v-if="Object.keys(lenderSummary).length > 1" style="margin-top: 0.5rem">
        <div v-for="(amount, lender) in lenderSummary" :key="lender" class="summary-row">
          <span>{{ lender }}</span>
          <span class="amount-negative">{{ amount.toLocaleString() }}円</span>
        </div>
      </div>
    </div>

    <!-- 未返済一覧 -->
    <div class="card">
      <h2 class="page-title">未返済一覧</h2>
      <div v-if="!unpaidDebts.length" class="empty-state">借金はありません</div>
      <ul v-else class="expense-list">
        <li v-for="d in unpaidDebts" :key="d.debt_id" class="expense-item" style="flex-wrap: wrap">
          <div class="expense-info" style="min-width: 0">
            <div class="expense-name">{{ d.lender }}</div>
            <div class="expense-meta">
              {{ d.date_str }} {{ d.memo }}
              <span v-if="Number(d.repaid_amount) > 0" style="color: var(--success)">
                （返済済: {{ Number(d.repaid_amount).toLocaleString() }}円）
              </span>
            </div>
          </div>
          <div style="text-align: right">
            <span class="expense-amount amount-negative">{{ remainingAmount(d).toLocaleString() }}円</span>
            <div v-if="Number(d.repaid_amount) > 0" style="font-size: 0.7rem; color: var(--text-muted)">
              元: {{ Number(d.amount).toLocaleString() }}円
            </div>
          </div>
          <div style="display: flex; gap: 0.25rem; width: 100%; margin-top: 0.5rem">
            <button class="btn btn-success btn-sm" @click="openRepayDialog(d)">返済する</button>
            <button class="btn btn-danger btn-sm" @click="removeDebt(d.debt_id)">削除</button>
          </div>
        </li>
      </ul>
    </div>

    <!-- 返済ダイアログ -->
    <div v-if="repayTarget" style="position: fixed; inset: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 1rem">
      <div class="card" style="max-width: 400px; width: 100%">
        <h2 class="page-title">{{ repayTarget.lender }} への返済</h2>
        <div class="summary-row">
          <span>残額</span>
          <span>{{ remainingAmount(repayTarget).toLocaleString() }}円</span>
        </div>
        <div class="form-group" style="margin-top: 0.75rem">
          <label>返済金額（円）</label>
          <input type="number" v-model.number="repayAmount" inputmode="numeric" :placeholder="String(remainingAmount(repayTarget))" />
        </div>
        <div style="display: flex; gap: 0.5rem">
          <button class="btn btn-success" style="flex: 1" @click="doRepay">返済</button>
          <button class="btn" style="flex: 1; background: var(--border)" @click="repayTarget = null">取消</button>
        </div>
      </div>
    </div>

    <!-- 返済済み -->
    <div v-if="paidDebts.length" class="card">
      <h2 class="page-title">返済済み</h2>
      <ul class="expense-list">
        <li v-for="d in paidDebts" :key="d.debt_id" class="expense-item" style="opacity: 0.5">
          <div class="expense-info">
            <div class="expense-name">{{ d.lender }}</div>
            <div class="expense-meta">返済日: {{ d.repaid_date }} {{ d.memo }}</div>
          </div>
          <span class="expense-amount">{{ Number(d.amount).toLocaleString() }}円</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getDebts, saveDebt, repayDebt, deleteDebt, isConfigured } from '../services/sheets-api'

const debts = ref([])
const form = ref({
  dateStr: new Date().toISOString().slice(0, 10),
  lender: '',
  amount: '',
  memo: '',
})
const repayTarget = ref(null)
const repayAmount = ref('')

const unpaidDebts = computed(() => debts.value.filter(d => d.is_repaid !== 'TRUE'))
const paidDebts = computed(() => debts.value.filter(d => d.is_repaid === 'TRUE'))

function remainingAmount(d) {
  return Number(d.amount) - Number(d.repaid_amount || 0)
}

const unpaidTotal = computed(() => unpaidDebts.value.reduce((s, d) => s + remainingAmount(d), 0))

const lenderSummary = computed(() => {
  const map = {}
  for (const d of unpaidDebts.value) {
    const lender = d.lender || '不明'
    map[lender] = (map[lender] || 0) + remainingAmount(d)
  }
  return map
})

function openRepayDialog(debt) {
  repayTarget.value = debt
  repayAmount.value = remainingAmount(debt)
}

async function fetchDebts() {
  if (!isConfigured()) return
  try {
    debts.value = await getDebts()
  } catch (e) {
    console.error('Failed to fetch debts:', e)
  }
}

async function submitDebt() {
  if (!form.value.lender || !form.value.amount) return
  try {
    await saveDebt(form.value)
    form.value.lender = ''
    form.value.amount = ''
    form.value.memo = ''
    await fetchDebts()
  } catch (e) {
    console.error('Failed to save debt:', e)
    alert('登録に失敗しました: ' + e.message)
  }
}

async function doRepay() {
  if (!repayAmount.value || repayAmount.value <= 0) return
  try {
    await repayDebt(repayTarget.value.debt_id, repayAmount.value)
    repayTarget.value = null
    repayAmount.value = ''
    await fetchDebts()
  } catch (e) {
    console.error('Failed to repay:', e)
    alert('返済記録に失敗しました: ' + e.message)
  }
}

async function removeDebt(id) {
  if (!confirm('削除しますか？')) return
  try {
    await deleteDebt(id)
    await fetchDebts()
  } catch (e) {
    console.error('Failed to delete debt:', e)
  }
}

onMounted(fetchDebts)
</script>
