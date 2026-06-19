// 年間予算サマリーCSV → 家計簿アプリ「取込」用CSV 変換スクリプト
//   実行: node scripts/convert-budget-csv.mjs "2026_家計簿 - 2026.csv"
//   出力: 取込用_<元ファイル名>.csv（日付,カテゴリ,品名,金額 の1行=1レコード）
//
// 元CSVの構造:
//   - 3か月ずつ横並びのブロック。各月は4列 [カテゴリ名, 予算, 金額(=実績), 差分]
//   - ヘッダー行の実績列に "N月" が入る → そこから対象月を判定
//   - 実績(金額)列を支出レコードとして展開。収入(手取り/副業 等)・合計・予算は除外
import Papa from 'papaparse'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, basename, join } from 'node:path'

const YEAR = 2026
// アプリの支出カテゴリのみ取り込む（収入・合計・内訳ラベルは除外される）
const EXPENSE_CATEGORIES = [
  'サブスク', '家賃', 'ローン', '病院', '光熱費',
  '携帯電話', '自由金', '交通費', '食費', '日用品', 'ペット',
]
const catOrder = new Map(EXPENSE_CATEGORIES.map((c, i) => [c, i]))

const src = process.argv[2] || '2026_家計簿 - 2026.csv'
const text = readFileSync(src, 'utf8')
const { data: grid } = Papa.parse(text, { skipEmptyLines: false })

function parseAmount(s) {
  if (s == null) return NaN
  const cleaned = String(s).replace(/[^0-9-]/g, '') // ¥ やカンマを除去
  if (cleaned === '' || cleaned === '-') return NaN
  return parseInt(cleaned, 10)
}

const records = []
const monthTotals = {} // 検算用: 月ごとの支出合計
let groupMonths = [null, null, null] // 3つの横並び列グループそれぞれの対象月

for (const row of grid) {
  // ヘッダー行判定（実績列に "N月"）。グループごとに対象月を更新
  let isHeader = false
  for (let g = 0; g < 3; g++) {
    const m = String(row[3 + g * 4] || '').match(/(\d+)\s*月/)
    if (m) { groupMonths[g] = Number(m[1]); isHeader = true }
  }
  if (isHeader) continue

  for (let g = 0; g < 3; g++) {
    const month = groupMonths[g]
    if (!month) continue
    const label = String(row[1 + g * 4] || '').trim()
    if (!catOrder.has(label)) continue // 支出カテゴリ以外は除外
    const actual = parseAmount(row[3 + g * 4]) // 金額(実績)列
    if (isNaN(actual) || actual <= 0) continue

    const mm = String(month).padStart(2, '0')
    records.push({
      date: `${YEAR}-${mm}-01`,
      category: label,
      item: `${month}月 ${label}（月合計）`,
      amount: actual,
      _month: month,
    })
    monthTotals[month] = (monthTotals[month] || 0) + actual
  }
}

// 月→カテゴリ順にソート
records.sort((a, b) => a._month - b._month || catOrder.get(a.category) - catOrder.get(b.category))

const out = Papa.unparse({
  fields: ['日付', 'カテゴリ', '品名', '金額'],
  data: records.map((r) => [r.date, r.category, r.item, r.amount]),
})

const outPath = join(dirname(src), `取込用_${basename(src)}`)
writeFileSync(outPath, out + '\n', 'utf8')

console.log(`出力: ${outPath}`)
console.log(`レコード数: ${records.length}`)
console.log('月別 支出合計（検算用）:')
for (const m of Object.keys(monthTotals).map(Number).sort((a, b) => a - b)) {
  console.log(`  ${m}月: ¥${monthTotals[m].toLocaleString()}`)
}
