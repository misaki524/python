<template>
  <div>
    <div class="month-nav">
      <button @click="changeMonth(-1)">&lt;</button>
      <span>{{ displayMonth }}</span>
      <button @click="changeMonth(1)">&gt;</button>
    </div>

    <div class="card">
      <h2 class="page-title">支出を追加</h2>
      <div class="form-group">
        <label>日付</label>
        <input type="date" v-model="form.dateStr" />
      </div>
      <div class="form-group">
        <label>カテゴリ</label>
        <div class="category-pills">
          <button
            v-for="cat in categories"
            :key="cat.name"
            class="category-pill"
            :class="{ active: form.category === cat.name }"
            @click="form.category = cat.name"
          >
            {{ cat.icon }} {{ cat.name }}
          </button>
          <button class="category-pill" style="border-style: dashed" @click="showAddCategory = true">＋ 追加</button>
        </div>
        <div v-if="showAddCategory" style="display: flex; gap: 0.5rem; margin-top: 0.5rem">
          <input type="text" v-model="newCategoryName" placeholder="新しいカテゴリ名" style="flex: 1; padding: 0.4rem 0.6rem; border: 1px solid var(--border); border-radius: 8px; font-size: 0.85rem" />
          <button class="btn btn-primary btn-sm" @click="doAddCategory">追加</button>
          <button class="btn btn-sm" style="background: var(--border)" @click="showAddCategory = false">取消</button>
        </div>
      </div>
      <div class="form-group">
        <label>品名・メモ</label>
        <input type="text" v-model="form.itemName" placeholder="例: スーパーで買い物" />
      </div>
      <div class="form-group">
        <label>金額（円）</label>
        <input type="number" v-model.number="form.amount" inputmode="numeric" placeholder="0" />
      </div>
      <div class="form-group">
        <label>支払い方法</label>
        <div style="display: flex; gap: 0.5rem; flex-wrap: wrap">
          <button
            v-for="pm in PAYMENT_METHODS"
            :key="pm.value"
            class="category-pill"
            :class="{ active: form.paymentMethod === pm.value }"
            @click="form.paymentMethod = pm.value"
          >
            {{ pm.label }}
          </button>
        </div>
      </div>
      <button class="btn btn-primary btn-block" @click="submitExpense" :disabled="saving">
        {{ saving ? '保存中...' : '保存' }}
      </button>
    </div>

    <div class="card">
      <div class="summary-row total">
        <span>合計</span>
        <span>{{ total.toLocaleString() }}円</span>
      </div>
      <div v-for="pm in paymentSummary" :key="pm.label" class="summary-row">
        <span>{{ pm.label }}</span>
        <span>{{ pm.amount.toLocaleString() }}円</span>
      </div>
    </div>

    <div class="card">
      <h2 class="page-title">支出一覧</h2>
      <div v-if="loading" class="empty-state">読み込み中...</div>
      <div v-else-if="!expenses.length" class="empty-state">支出データがありません</div>
      <ul v-else class="expense-list">
        <template v-for="(group, date) in groupedByDate" :key="date">
          <li class="date-separator">{{ date }}</li>
          <li v-for="exp in group" :key="exp.expense_id" class="expense-item">
            <span class="expense-cat-dot" :style="{ background: getCategoryColor(exp.category) }"></span>
            <div class="expense-info">
              <div class="expense-name">
                {{ getCategoryIcon(exp.category) }} {{ exp.item_name || exp.category }}
                <span v-if="isCategoryDeleted(exp.category)" style="font-size: 0.7rem; color: var(--danger)">（削除された項目です）</span>
              </div>
              <div class="expense-meta">
                <span class="payment-badge" :class="badgeClass(exp.payment_method)">
                  {{ getPaymentLabel(exp.payment_method) }}
                </span>
              </div>
            </div>
            <span class="expense-amount">{{ Number(exp.amount).toLocaleString() }}円</span>
            <button class="btn btn-danger btn-sm" @click="removeExpense(exp.expense_id)">削除</button>
          </li>
        </template>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { getCategories, addCategory, PAYMENT_METHODS, getCategoryColor, getCategoryIcon, getPaymentLabel, isCategoryDeleted } from '../utils/categories'
import { getExpenses, saveExpense, deleteExpense, isConfigured } from '../services/sheets-api'
import { useMonthNav } from '../composables/useMonthNav'
import { useAsync } from '../composables/useAsync'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'

const today = new Date()
const { currentYM, displayMonth, changeMonth } = useMonthNav()
const { loading, run } = useAsync()
const { loading: saving, run: runSave } = useAsync()
const toast = useToast()
const { confirm } = useConfirm()

const expenses = ref([])
const categories = ref(getCategories())
const showAddCategory = ref(false)
const newCategoryName = ref('')

const form = ref({
  dateStr: today.toISOString().slice(0, 10),
  category: '',
  itemName: '',
  amount: '',
  paymentMethod: 'cash',
})

const total = computed(() => expenses.value.reduce((s, e) => s + Number(e.amount), 0))

const paymentSummary = computed(() => {
  return PAYMENT_METHODS.map(pm => ({
    label: pm.label,
    amount: expenses.value
      .filter(e => e.payment_method === pm.value)
      .reduce((s, e) => s + Number(e.amount), 0),
  })).filter(p => p.amount > 0)
})

const groupedByDate = computed(() => {
  const groups = {}
  const sorted = [...expenses.value].sort((a, b) => (b.date_str || '').localeCompare(a.date_str || ''))
  for (const exp of sorted) {
    const d = exp.date_str || '不明'
    if (!groups[d]) groups[d] = []
    groups[d].push(exp)
  }
  return groups
})

function badgeClass(pm) {
  if (pm === 'card') return 'card'
  if (pm === 'dcard') return 'dcard'
  return 'cash'
}

function doAddCategory() {
  const name = newCategoryName.value.trim()
  if (!name) return
  if (addCategory(name)) {
    categories.value = getCategories()
    form.value.category = name
    newCategoryName.value = ''
    showAddCategory.value = false
  } else {
    toast.error('そのカテゴリは既に存在します')
  }
}

async function fetchExpenses() {
  if (!isConfigured()) return
  await run(async () => {
    expenses.value = await getExpenses(currentYM.value)
  }, { errorMessage: 'データの取得に失敗しました' })
}

async function submitExpense() {
  if (!form.value.amount || !form.value.category) return
  await runSave(async () => {
    const cat = categories.value.find(c => c.name === form.value.category)
    await saveExpense({
      dateStr: form.value.dateStr,
      category: form.value.category,
      itemName: form.value.itemName,
      amount: form.value.amount,
      paymentMethod: form.value.paymentMethod,
      isFixed: cat?.isFixed || false,
    })
    form.value.itemName = ''
    form.value.amount = ''
    await fetchExpenses()
  }, { errorMessage: '保存に失敗しました', successMessage: '保存しました' })
}

async function removeExpense(id) {
  if (!(await confirm('この支出を削除しますか？', { danger: true, confirmText: '削除' }))) return
  await run(async () => {
    await deleteExpense(id)
    await fetchExpenses()
  }, { errorMessage: '削除に失敗しました', successMessage: '削除しました' })
}

watch(currentYM, fetchExpenses)
onMounted(fetchExpenses)
</script>
