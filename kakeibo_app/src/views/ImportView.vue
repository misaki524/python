<template>
  <div>
    <div class="card">
      <h2 class="page-title">スプレッドシートからCSV取込</h2>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem">
        既存のスプレッドシートからCSVでエクスポートしたファイルを取り込みます。<br />
        手順: スプレッドシートを開く → ファイル → ダウンロード → CSV(.csv)
      </p>

      <div class="form-group">
        <label>CSVファイルを選択</label>
        <input type="file" accept=".csv" @change="onFileSelect" />
      </div>
    </div>

    <div v-if="csvHeaders.length" class="card">
      <h2 class="page-title">列マッピング</h2>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem">
        CSVの列を家計簿アプリのフィールドに対応付けてください。
      </p>

      <div class="form-group">
        <label>日付の列</label>
        <select v-model="mapping.date">
          <option value="">-- 選択 --</option>
          <option v-for="h in csvHeaders" :key="h" :value="h">{{ h }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>品名・内容の列</label>
        <select v-model="mapping.itemName">
          <option value="">-- 選択 --</option>
          <option v-for="h in csvHeaders" :key="h" :value="h">{{ h }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>金額の列</label>
        <select v-model="mapping.amount">
          <option value="">-- 選択 --</option>
          <option v-for="h in csvHeaders" :key="h" :value="h">{{ h }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>カテゴリの列（あれば）</label>
        <select v-model="mapping.category">
          <option value="">-- なし --</option>
          <option v-for="h in csvHeaders" :key="h" :value="h">{{ h }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>支払い方法の列（あれば）</label>
        <select v-model="mapping.paymentMethod">
          <option value="">-- なし --</option>
          <option v-for="h in csvHeaders" :key="h" :value="h">{{ h }}</option>
        </select>
      </div>
    </div>

    <div v-if="previewRows.length" class="card">
      <h2 class="page-title">プレビュー（先頭5件）</h2>
      <div style="overflow-x: auto">
        <table style="width: 100%; font-size: 0.8rem; border-collapse: collapse">
          <thead>
            <tr>
              <th style="text-align: left; padding: 0.3rem; border-bottom: 1px solid var(--border)">日付</th>
              <th style="text-align: left; padding: 0.3rem; border-bottom: 1px solid var(--border)">品名</th>
              <th style="text-align: left; padding: 0.3rem; border-bottom: 1px solid var(--border)">カテゴリ</th>
              <th style="text-align: right; padding: 0.3rem; border-bottom: 1px solid var(--border)">金額</th>
              <th style="text-align: left; padding: 0.3rem; border-bottom: 1px solid var(--border)">支払</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, i) in previewRows" :key="i">
              <td style="padding: 0.3rem">{{ row.dateStr }}</td>
              <td style="padding: 0.3rem">{{ row.itemName }}</td>
              <td style="padding: 0.3rem">{{ row.category }}</td>
              <td style="padding: 0.3rem; text-align: right">{{ Number(row.amount).toLocaleString() }}</td>
              <td style="padding: 0.3rem">{{ getPaymentLabel(row.paymentMethod) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div style="margin-top: 0.75rem; font-size: 0.85rem; color: var(--text-muted)">
        合計 {{ mappedRows.length }}件のデータ
      </div>
    </div>

    <div v-if="mappedRows.length" class="card">
      <button class="btn btn-primary btn-block" @click="doImport" :disabled="importing">
        {{ importing ? '取込中...' : `${mappedRows.length}件を取り込む` }}
      </button>
      <div v-if="importResult" style="margin-top: 0.75rem; text-align: center; color: var(--success); font-weight: 600">
        {{ importResult }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { parseCSV, mapCSVToExpenses } from '../utils/csv-import'
import { bulkSaveExpenses, isConfigured } from '../services/sheets-api'
import { getPaymentLabel } from '../utils/categories'
import { useAsync } from '../composables/useAsync'
import { useToast } from '../composables/useToast'

const { loading: importing, run } = useAsync()
const toast = useToast()

const csvRows = ref([])
const csvHeaders = ref([])
const mapping = ref({ date: '', itemName: '', amount: '', category: '', paymentMethod: '' })
const importResult = ref('')

async function onFileSelect(e) {
  const file = e.target.files[0]
  if (!file) return
  importResult.value = ''
  try {
    const result = await parseCSV(file)
    csvRows.value = result.data
    csvHeaders.value = result.meta.fields || []
    autoDetectMapping()
  } catch (err) {
    console.error('CSV parse error:', err)
    toast.error('CSVの読み込みに失敗しました')
  }
}

function autoDetectMapping() {
  for (const h of csvHeaders.value) {
    const lower = h.toLowerCase()
    if (lower.includes('日付') || lower.includes('date')) mapping.value.date = h
    else if (lower.includes('品名') || lower.includes('内容') || lower.includes('item') || lower.includes('メモ') || lower.includes('摘要')) mapping.value.itemName = h
    else if (lower.includes('金額') || lower.includes('amount') || lower.includes('合計')) mapping.value.amount = h
    else if (lower.includes('カテゴリ') || lower.includes('category') || lower.includes('分類')) mapping.value.category = h
    else if (lower.includes('支払') || lower.includes('payment') || lower.includes('方法')) mapping.value.paymentMethod = h
  }
}

const mappedRows = computed(() => {
  if (!mapping.value.date || !mapping.value.amount) return []
  return mapCSVToExpenses(csvRows.value, mapping.value)
})

const previewRows = computed(() => mappedRows.value.slice(0, 5))

async function doImport() {
  if (!isConfigured()) {
    toast.error('GAS URLが未設定です。設定画面で接続設定を行ってください。')
    return
  }
  if (!mappedRows.value.length) return
  const count = mappedRows.value.length
  await run(async () => {
    const result = await bulkSaveExpenses(mappedRows.value)
    const saved = Number(result?.saved || 0)
    if (saved === count) {
      importResult.value = `${count}件のデータを取り込みました！`
    } else if (saved > 0) {
      importResult.value = `${saved}/${count}件のみ保存されました。GAS側のログを確認してください。`
      toast.error(`期待 ${count}件 のうち ${saved}件 しか保存されませんでした`)
    } else {
      importResult.value = ''
      throw new Error(`保存件数が0件です。GASのデプロイが古い可能性があります（gas-code.js を貼り直して再デプロイしてください）`)
    }
  }, { errorMessage: '取込に失敗しました' })
}
</script>
