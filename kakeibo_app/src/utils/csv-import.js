import Papa from 'papaparse'

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
        paymentMethod: row[columnMapping.paymentMethod] || 'cash',
        isFixed: false,
      }
    })
    .filter(Boolean)
}
