const DEFAULT_CATEGORIES = [
  { name: 'サブスク', color: '#9966FF', icon: '🔄', isFixed: true },
  { name: '家賃', color: '#E7E9ED', icon: '🏠', isFixed: true },
  { name: 'ローン', color: '#FF9F40', icon: '💳', isFixed: true },
  { name: '病院', color: '#FF6384', icon: '🏥', isFixed: false },
  { name: '光熱費', color: '#FFCE56', icon: '💡', isFixed: true },
  { name: '携帯電話', color: '#36A2EB', icon: '📱', isFixed: true },
  { name: '自由金', color: '#4BC0C0', icon: '🎮', isFixed: false },
  { name: '交通費', color: '#7BC8A4', icon: '🚃', isFixed: false },
  { name: '食費', color: '#FF6384', icon: '🍚', isFixed: false },
  { name: '日用品', color: '#C9CBCF', icon: '🧴', isFixed: false },
  { name: 'ペット', color: '#F7DC6F', icon: '🐾', isFixed: false },
]

const EXTRA_COLORS = ['#E74C3C', '#8E44AD', '#2ECC71', '#E67E22', '#1ABC9C', '#D35400', '#2C3E50']

export const DELETED_LABEL = '削除された項目です'

const CUSTOM_KEY = 'kakeibo_custom_categories'
const DELETED_KEY = 'kakeibo_deleted_categories'

function readCustom() {
  return JSON.parse(localStorage.getItem(CUSTOM_KEY) || '[]')
}
function writeCustom(list) {
  localStorage.setItem(CUSTOM_KEY, JSON.stringify(list))
}
function readDeleted() {
  return JSON.parse(localStorage.getItem(DELETED_KEY) || '[]')
}
function writeDeleted(list) {
  localStorage.setItem(DELETED_KEY, JSON.stringify(list))
}

export function isDefaultCategory(name) {
  return DEFAULT_CATEGORIES.some(c => c.name === name)
}

// 有効なカテゴリ（デフォルト＋カスタム）
export function getCategories() {
  return [...DEFAULT_CATEGORIES, ...readCustom()]
}

// 削除済みカテゴリ（過去データ表示用に保持）
export function getDeletedCategories() {
  return readDeleted()
}

export function addCategory(name) {
  const all = getCategories()
  if (all.some(c => c.name === name)) return false
  const custom = readCustom()
  const colorIdx = custom.length % EXTRA_COLORS.length
  custom.push({ name, color: EXTRA_COLORS[colorIdx], icon: '📝', isFixed: false })
  writeCustom(custom)
  // 同名の削除済み項目があれば復活させる（削除済みリストから除去）
  const deleted = readDeleted().filter(c => c.name !== name)
  writeDeleted(deleted)
  return true
}

// カスタムカテゴリの編集（名称・アイコン）。デフォルトは編集不可。
export function editCategory(oldName, newName, icon) {
  if (isDefaultCategory(oldName)) return false
  const custom = readCustom()
  const target = custom.find(c => c.name === oldName)
  if (!target) return false
  const trimmed = (newName || '').trim()
  if (!trimmed) return false
  // 改名先が既存の別カテゴリと重複していないか
  if (trimmed !== oldName && getCategories().some(c => c.name === trimmed)) return false
  target.name = trimmed
  if (icon) target.icon = icon
  writeCustom(custom)
  return true
}

// カスタムカテゴリの削除。過去データ表示用に削除済みリストへ退避する。
export function removeCategory(name) {
  if (isDefaultCategory(name)) return false
  const custom = readCustom()
  const target = custom.find(c => c.name === name)
  const filtered = custom.filter(c => c.name !== name)
  writeCustom(filtered)
  if (target) {
    const deleted = readDeleted().filter(c => c.name !== name)
    deleted.push({ ...target })
    writeDeleted(deleted)
  }
  return true
}

export const PAYMENT_METHODS = [
  { value: 'cash', label: '現金' },
  { value: 'card', label: 'カード' },
  { value: 'dcard', label: 'Dカード' },
  { value: 'debit', label: '口座引落' },
  { value: 'installment', label: '分割払い' },
]

// 有効・削除済みの両方から検索（過去データの色・アイコンを保持するため）
function findAny(name) {
  return getCategories().find(c => c.name === name) || readDeleted().find(c => c.name === name)
}

export function isCategoryDeleted(name) {
  if (!name) return false
  if (getCategories().some(c => c.name === name)) return false
  return readDeleted().some(c => c.name === name)
}

// 表示用ラベル: 削除済みなら「（削除された項目です）」を付与
export function getCategoryDisplayName(name) {
  return isCategoryDeleted(name) ? `${name}（${DELETED_LABEL}）` : name
}

export function getCategoryColor(name) {
  return findAny(name)?.color ?? '#999999'
}

export function getCategoryIcon(name) {
  return findAny(name)?.icon ?? '📝'
}

export function getPaymentLabel(value) {
  return PAYMENT_METHODS.find(p => p.value === value)?.label ?? value
}
