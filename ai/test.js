// 2つの日付の間の日数を計算する関数
// begin: 開始日（例: '2026-02-01' などの文字列やDateオブジェクト）
// end: 終了日（例: '2026-02-03' などの文字列やDateオブジェクト）
// 戻り値: 2つの日付の間の日数（整数値）
function calculateDaysBetweenDates(begin, end) {
    // 1日のミリ秒数を計算（24時間 × 60分 × 60秒 × 1000ミリ秒）
    const oneDay = 24 * 60 * 60 * 1000;
    // 引数からDateオブジェクトを作成
    const firstDate = new Date(begin);
    const secondDate = new Date(end);
    // 2つの日付の差分（ミリ秒）を絶対値で取得し、1日あたりのミリ秒数で割る
    // Math.absを使うことで順序に関係なく正の値になる
    const diffDays = Math.round(Math.abs((secondDate - firstDate) / oneDay));
    // 差分日数を返す
    return diffDays;
}