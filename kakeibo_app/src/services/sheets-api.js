function getGasUrl() {
  return localStorage.getItem('kakeibo_gas_url') || ''
}

export function isConfigured() {
  return !!getGasUrl()
}

async function callGAS(action, data = {}) {
  const baseUrl = getGasUrl()
  if (!baseUrl) throw new Error('GAS URLが設定されていません。設定画面からURLを入力してください。')

  const url = new URL(baseUrl)
  url.searchParams.set('action', action)
  url.searchParams.set('data', JSON.stringify(data))

  const response = await fetch(url.toString())
  const text = await response.text()

  if (text.startsWith('<!')) {
    throw new Error('GASから正しいレスポンスが返りません。デプロイ設定でアクセスを「全員」にしてください。')
  }

  const result = JSON.parse(text)
  if (!result.ok) throw new Error(result.error || '不明なエラー')
  return result.data
}

// --- Expenses ---

export async function getExpenses(yearMonth) {
  return callGAS('getExpenses', { yearMonth })
}

export async function saveExpense(data) {
  return callGAS('saveExpense', data)
}

export async function deleteExpense(id) {
  return callGAS('deleteExpense', { id })
}

export async function bulkSaveExpenses(expenses) {
  const baseUrl = getGasUrl()
  if (!baseUrl) throw new Error('GAS URLが未設定')

  const batchSize = 20
  for (let i = 0; i < expenses.length; i += batchSize) {
    const batch = expenses.slice(i, i + batchSize)
    await callGAS('bulkSaveExpenses', { expenses: batch })
  }
}

// --- Income ---

export async function getIncome(yearMonth) {
  return callGAS('getIncome', { yearMonth })
}

export async function saveIncome(data) {
  return callGAS('saveIncome', data)
}

export async function deleteIncome(id) {
  return callGAS('deleteIncome', { id })
}

// --- Budget ---

export async function getBudget(yearMonth) {
  return callGAS('getBudget', { yearMonth })
}

export async function saveBudget(yearMonth, budgetData) {
  return callGAS('saveBudget', { yearMonth, ...budgetData })
}

// --- WorkLog ---

export async function getWorkLog(yearMonth) {
  return callGAS('getWorkLog', { yearMonth })
}

export async function saveWorkLog(data) {
  return callGAS('saveWorkLog', data)
}

export async function deleteWorkLog(id) {
  return callGAS('deleteWorkLog', { id })
}

// --- Jobs ---

export async function getJobs() {
  return callGAS('getJobs')
}

export async function saveJob(data) {
  return callGAS('saveJob', data)
}

export async function deleteJob(id) {
  return callGAS('deleteJob', { id })
}

// --- Debt ---

export async function getDebts() {
  return callGAS('getDebts')
}

export async function saveDebt(data) {
  return callGAS('saveDebt', data)
}

export async function repayDebt(id, repaidAmount) {
  return callGAS('repayDebt', { id, repaidAmount })
}

export async function deleteDebt(id) {
  return callGAS('deleteDebt', { id })
}

// --- Init ---

export async function initSheets() {
  return callGAS('initSheets')
}
