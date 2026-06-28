<template>
  <div>
    <div class="card">
      <h2 class="page-title">GAS接続設定</h2>
      <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1rem">
        スプレッドシートのApps Scriptにバックエンドコードを貼り付けてデプロイし、そのURLを入力してください。
      </p>

      <div class="form-group">
        <label>GAS WebアプリURL</label>
        <input type="text" v-model="gasUrl" placeholder="https://script.google.com/macros/s/xxxxx/exec" />
      </div>
      <button class="btn btn-primary btn-block" @click="saveUrl">保存</button>
      <div v-if="gasUrl" style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--success)">設定済み</div>
    </div>

    <div v-if="gasUrl" class="card">
      <h2 class="page-title">接続テスト / シート初期化</h2>
      <button class="btn btn-primary" @click="testAndInit" :disabled="testing">
        {{ testing ? 'テスト中...' : '接続テスト＆シート自動作成' }}
      </button>
      <div v-if="testResult" style="margin-top: 0.5rem; font-size: 0.9rem" :class="testOk ? 'amount-positive' : 'amount-negative'">
        {{ testResult }}
      </div>
      <div v-if="testOk && testDetail.spreadsheetName" style="margin-top: 0.5rem; font-size: 0.8rem; color: var(--text-muted); line-height: 1.6">
        <div>紐づきシート: <strong>{{ testDetail.spreadsheetName }}</strong></div>
        <div v-if="testDetail.spreadsheetUrl">
          <a :href="testDetail.spreadsheetUrl" target="_blank" rel="noopener" style="color: var(--primary)">スプレッドシートを開く</a>
        </div>
        <div>今回作成: {{ testDetail.created.length ? testDetail.created.join(', ') : 'なし（全シート既に存在）' }}</div>
        <div v-if="testDetail.existing.length">既存: {{ testDetail.existing.join(', ') }}</div>
      </div>
    </div>

    <div class="card">
      <h2 class="page-title">カテゴリ管理</h2>
      <div class="category-pills" style="margin-bottom: 0.5rem">
        <span v-for="cat in categories" :key="cat.name" class="category-pill" style="cursor: default">
          <template v-if="editingCat === cat.name">
            <input type="text" v-model="editCatName" style="width: 6rem; padding: 0.1rem 0.3rem; border: 1px solid var(--border); border-radius: 6px; font-size: 0.8rem" />
            <button @click="saveEditCat(cat.name)" style="margin-left: 0.25rem; background: none; border: none; cursor: pointer; color: var(--success); font-size: 0.8rem">✔</button>
            <button @click="editingCat = ''" style="margin-left: 0.1rem; background: none; border: none; cursor: pointer; color: var(--text-muted); font-size: 0.8rem">✕</button>
          </template>
          <template v-else>
            {{ cat.icon }} {{ cat.name }}
            <template v-if="!cat._default">
              <button @click="startEditCat(cat.name)" style="margin-left: 0.25rem; background: none; border: none; cursor: pointer; color: var(--primary); font-size: 0.8rem">✎</button>
              <button @click="removeCat(cat.name)" style="margin-left: 0.1rem; background: none; border: none; cursor: pointer; color: var(--danger); font-size: 0.8rem">✕</button>
            </template>
          </template>
        </span>
      </div>
      <div style="display: flex; gap: 0.5rem">
        <input type="text" v-model="newCatName" placeholder="新しいカテゴリ名" style="flex: 1; padding: 0.4rem 0.6rem; border: 1px solid var(--border); border-radius: 8px; font-size: 0.85rem" @keyup.enter="doAddCat" />
        <button class="btn btn-primary btn-sm" @click="doAddCat">追加</button>
      </div>

      <div v-if="deletedCategories.length" style="margin-top: 0.75rem; border-top: 1px solid var(--border); padding-top: 0.5rem">
        <p style="font-size: 0.8rem; color: var(--text-muted); margin-bottom: 0.4rem">削除された項目です（過去データの表示用に保持）</p>
        <div class="category-pills">
          <span v-for="cat in deletedCategories" :key="cat.name" class="category-pill" style="cursor: default; opacity: 0.6; text-decoration: line-through">
            {{ cat.icon }} {{ cat.name }}
            <button @click="restoreCat(cat.name)" style="margin-left: 0.25rem; background: none; border: none; cursor: pointer; color: var(--success); font-size: 0.7rem; text-decoration: none">復元</button>
          </span>
        </div>
      </div>
    </div>

    <div class="card">
      <h2 class="page-title">セットアップ手順</h2>
      <ol style="font-size: 0.85rem; color: var(--text-muted); padding-left: 1.25rem; line-height: 2">
        <li>対象のスプレッドシートを開く<br />
          <input type="text" v-model="sheetUrl" placeholder="自分のスプレッドシートURLを貼り付け" @change="saveSheetUrl" style="width: 100%; padding: 0.3rem 0.5rem; border: 1px solid var(--border); border-radius: 6px; font-size: 0.8rem; margin: 0.25rem 0" />
          <a v-if="sheetUrl" :href="sheetUrl" target="_blank" rel="noopener" style="color: var(--primary)">スプレッドシートを開く</a>
        </li>
        <li><strong>拡張機能</strong> → <strong>Apps Script</strong> を開く</li>
        <li><code>docs/gas-code.js</code> の内容を全てコピーして貼り付ける</li>
        <li>保存（Ctrl+S）</li>
        <li><strong>デプロイ</strong> → <strong>新しいデプロイ</strong></li>
        <li>種類: <strong>ウェブアプリ</strong></li>
        <li>実行ユーザー: <strong>自分</strong></li>
        <li>アクセス: <strong>全員</strong></li>
        <li>デプロイ → URLをコピー</li>
        <li>上のフォームにURLを貼り付けて保存</li>
        <li>「接続テスト＆シート自動作成」ボタンを押す<br />（必要なシート・ヘッダーが自動作成されます）</li>
      </ol>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { initSheets, isConfigured } from '../services/sheets-api'
import { getCategories, getDeletedCategories, addCategory, removeCategory, editCategory, isDefaultCategory } from '../utils/categories'
import { useToast } from '../composables/useToast'
import { useConfirm } from '../composables/useConfirm'

const toast = useToast()
const { confirm } = useConfirm()

const gasUrl = ref('')
const sheetUrl = ref('')
const testing = ref(false)
const testResult = ref('')
const testOk = ref(false)
const testDetail = ref({ spreadsheetName: '', spreadsheetUrl: '', created: [], existing: [] })
const categories = ref([])
const deletedCategories = ref([])
const newCatName = ref('')
const editingCat = ref('')
const editCatName = ref('')

onMounted(() => {
  gasUrl.value = localStorage.getItem('kakeibo_gas_url') || ''
  sheetUrl.value = localStorage.getItem('kakeibo_sheet_url') || ''
  loadCategories()
})

function saveSheetUrl() {
  localStorage.setItem('kakeibo_sheet_url', sheetUrl.value.trim())
}

function loadCategories() {
  categories.value = getCategories().map(c => ({
    ...c,
    _default: isDefaultCategory(c.name),
  }))
  deletedCategories.value = getDeletedCategories()
}

function saveUrl() {
  localStorage.setItem('kakeibo_gas_url', gasUrl.value.trim())
  toast.success('URLを保存しました')
}

async function testAndInit() {
  testing.value = true
  testResult.value = ''
  testDetail.value = { spreadsheetName: '', spreadsheetUrl: '', created: [], existing: [] }
  try {
    const result = await initSheets()
    testOk.value = true
    const createdCount = (result.created || []).length
    testResult.value = createdCount
      ? `接続成功！${createdCount}個のシートを新規作成しました`
      : '接続成功（シートは既に全て存在しています）'
    testDetail.value = {
      spreadsheetName: result.spreadsheetName || '',
      spreadsheetUrl: result.spreadsheetUrl || '',
      created: result.created || [],
      existing: result.existing || [],
    }
  } catch (e) {
    testOk.value = false
    testResult.value = '接続失敗: ' + (e.message || e)
  } finally {
    testing.value = false
  }
}

function doAddCat() {
  const name = newCatName.value.trim()
  if (!name) return
  if (addCategory(name)) {
    newCatName.value = ''
    loadCategories()
  } else {
    toast.error('そのカテゴリは既に存在します')
  }
}

async function removeCat(name) {
  const ok = await confirm(
    `「${name}」を削除しますか？\n過去データはスプレッドシートに残り、「削除された項目です」として表示されます。`,
    { danger: true, confirmText: '削除' }
  )
  if (ok) {
    removeCategory(name)
    loadCategories()
  }
}

function startEditCat(name) {
  editingCat.value = name
  editCatName.value = name
}

function saveEditCat(oldName) {
  const newName = editCatName.value.trim()
  if (!newName) return
  if (newName === oldName) {
    editingCat.value = ''
    return
  }
  if (editCategory(oldName, newName)) {
    editingCat.value = ''
    loadCategories()
  } else {
    toast.error('その名前は使用できません（既存のカテゴリと重複しています）')
  }
}

function restoreCat(name) {
  if (addCategory(name)) {
    loadCategories()
  }
}
</script>
