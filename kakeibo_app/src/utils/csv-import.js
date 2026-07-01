import Papa from 'papaparse'
import { PAYMENT_METHODS } from './categories'

export function parseCSV(file) {
  return new Promise((resolve, reject) => {
    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      encoding: 'UTF-8',
      complete: (results) => resolve(results),
      error: (error) => reject(error),
    })
  })
}

function normalizePaymentMethod(raw) {
  if (!raw) return 'cash'
  const v = String(raw).trim()
  if (!v) return 'cash'
  // 既に内部値ならそのまま
  if (PAYMENT_METHODS.some(pm => pm.value === v)) return v
  // 日本語ラベルなら対応する value を返す
  const hit = PAYMENT_METHODS.find(pm => pm.label === v)
  if (hit) return hit.value
  // 部分一致（"クレジットカード" → card 等）
  if (v.includes('分割')) return 'installment'
  if (v.includes('Dカード') || v.toLowerCase().includes('dcard')) return 'dcard'
  if (v.includes('カード') || v.toLowerCase().includes('card')) return 'card'
  if (v.includes('引落') || v.includes('引き落') || v.includes('口座')) return 'debit'
  if (v.includes('現金') || v.toLowerCase().includes('cash')) return 'cash'
  return 'cash'
}

export function mapCSVToExpenses(rows, columnMapping) {
  return rows
    .map((row) => {
      const dateStr = row[columnMapping.date] || ''
      const amount = parseInt(row[columnMapping.amount], 10)
      if (!dateStr || isNaN(amount)) return null

      const yearMonth = dateStr.slice(0, 7)
      return {
        id: crypto.randomUUID(),
        timestamp: new Date(dateStr).toISOString(),
        dateStr,
        yearMonth,
        category: row[columnMapping.category] || 'その他',
        itemName: row[columnMapping.itemName] || '',
        amount,
        paymentMethod: normalizePaymentMethod(row[columnMapping.paymentMethod]),
        isFixed: false,
      }
    })
    .filter(Boolean)
}
