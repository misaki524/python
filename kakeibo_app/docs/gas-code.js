// ============================================
// 家計簿アプリ GASバックエンド
// このコードをスプレッドシートの Apps Script に貼り付けてください
// ============================================

const SHEET_NAMES = {
  expenses: 'Expenses',
  income: 'Income',
  budget: 'Budget',
  workLog: 'WorkLog',
  debt: 'Debt',
  jobs: 'Jobs',
};

const HEADERS = {
  Expenses: ['expense_id','timestamp','date_str','year_month','category','item_name','amount','payment_method','is_fixed'],
  Income: ['income_id','timestamp','date_str','year_month','source','amount','memo'],
  Budget: ['year_month','budget_total','budget_json'],
  WorkLog: ['work_id','date_str','year_month','start_time','end_time','break_minutes','work_hours','hourly_rate','daily_pay','job_name','transport_cost'],
  Debt: ['debt_id','date_str','lender','amount','memo','is_repaid','repaid_date','repaid_amount'],
  Jobs: ['job_id','store_name','hourly_rate','daily_rate','transport_cost','is_active'],
};

function doGet(e) {
  return handleRequest(e);
}

function doPost(e) {
  return handleRequest(e);
}

function handleRequest(e) {
  try {
    const params = e.parameter || {};
    let body = {};
    if (e.postData && e.postData.contents) {
      body = JSON.parse(e.postData.contents);
    }
    // GETリクエスト時はdataパラメータからJSONを読み取る
    if (params.data) {
      body = Object.assign(body, JSON.parse(params.data));
    }
    const action = params.action || body.action;
    let result;

    switch (action) {
      case 'initSheets': result = initSheets(); break;
      case 'getExpenses': result = getExpenses(params.yearMonth || body.yearMonth); break;
      case 'saveExpense': result = saveExpense(body); break;
      case 'deleteExpense': result = deleteRow_('Expenses', 'expense_id', body.id); break;
      case 'bulkSaveExpenses': result = bulkSaveExpenses(body.expenses); break;
      case 'getIncome': result = getIncome(params.yearMonth || body.yearMonth); break;
      case 'saveIncome': result = saveIncome(body); break;
      case 'deleteIncome': result = deleteRow_('Income', 'income_id', body.id); break;
      case 'getBudget': result = getBudget(params.yearMonth || body.yearMonth); break;
      case 'saveBudget': result = saveBudget(body); break;
      case 'getWorkLog': result = getWorkLog(params.yearMonth || body.yearMonth); break;
      case 'saveWorkLog': result = saveWorkLog(body); break;
      case 'deleteWorkLog': result = deleteRow_('WorkLog', 'work_id', body.id); break;
      case 'getJobs': result = getJobs(); break;
      case 'saveJob': result = saveJob(body); break;
      case 'deleteJob': result = deleteJob(body.id); break;
      case 'getDebts': result = getDebts(); break;
      case 'saveDebt': result = saveDebt(body); break;
      case 'repayDebt': result = repayDebt(body); break;
      case 'deleteDebt': result = deleteRow_('Debt', 'debt_id', body.id); break;
      default: throw new Error('Unknown action: ' + action);
    }

    return ContentService.createTextOutput(JSON.stringify({ ok: true, data: result }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// --- 日本語ヘッダー（2行目に説明行として挿入） ---

const HEADERS_JP = {
  Expenses: ['ID','記録日時','日付','年月','カテゴリ','品名・メモ','金額(円)','支払方法','固定費'],
  Income: ['ID','記録日時','日付','年月','収入元','金額(円)','メモ'],
  Budget: ['年月','月予算合計(円)','カテゴリ別予算(JSON)'],
  WorkLog: ['ID','日付','年月','開始時刻','終了時刻','休憩(分)','実働時間(h)','時給(円)','日給(円)','バイト先','交通費(円)'],
  Debt: ['ID','借りた日','貸主・借入先','金額(円)','メモ','返済済み','返済日','返済済み金額(円)'],
  Jobs: ['ID','店名・会社名','時給(円)','日給(円)','交通費/日(円)','有効'],
};

const SHEET_COLORS = {
  Expenses: '#ea4335',
  Income: '#34a853',
  Budget: '#fbbc04',
  WorkLog: '#4285f4',
  Debt: '#ff6d01',
  Jobs: '#46bdc6',
};

// --- シート初期化 ---

function initSheets() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    throw new Error('スプレッドシートに紐づいていません。対象スプレッドシートを開き「拡張機能 → Apps Script」から作ったプロジェクトにコードを貼り直してください。');
  }
  const created = [];
  const existing = [];
  for (const [name, headers] of Object.entries(HEADERS)) {
    let sheet = ss.getSheetByName(name);
    if (!sheet) {
      sheet = ss.insertSheet(name);
      created.push(name);
    } else {
      existing.push(name);
    }

    // 1行目: 英語ヘッダー（プログラム用）。スキーマ変更時も追従するよう全列を比較
    const existing = sheet.getRange(1, 1, 1, headers.length).getValues()[0];
    if (headers.some((h, i) => existing[i] !== h)) {
      sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    }

    // 2行目: 日本語説明（無ければ挿入し、常に最新ラベルへ更新）
    const jpHeaders = HEADERS_JP[name];
    if (jpHeaders) {
      const row2 = sheet.getRange(2, 1, 1, jpHeaders.length).getValues()[0];
      if (row2[0] !== jpHeaders[0]) {
        sheet.insertRowBefore(2);
      }
      sheet.getRange(2, 1, 1, jpHeaders.length).setValues([jpHeaders]);

      // 2行目のスタイル: 背景色グレー、太字、文字色白
      const jpRange = sheet.getRange(2, 1, 1, jpHeaders.length);
      jpRange.setBackground('#444444');
      jpRange.setFontColor('#ffffff');
      jpRange.setFontWeight('bold');
      jpRange.setFontSize(9);
    }

    // 1行目のスタイル: 背景色薄グレー、太字
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setBackground('#e8eaed');
    headerRange.setFontWeight('bold');
    headerRange.setFontSize(9);

    // 1行目と2行目を固定表示
    sheet.setFrozenRows(2);

    // シートタブの色
    const color = SHEET_COLORS[name];
    if (color) {
      sheet.setTabColor(color);
    }

    // 列幅を自動調整
    for (let c = 1; c <= headers.length; c++) {
      sheet.autoResizeColumn(c);
    }
  }
  return {
    message: 'シート初期化完了（日本語ヘッダー・色分け適用済み）',
    spreadsheetName: ss.getName(),
    spreadsheetUrl: ss.getUrl(),
    created: created,
    existing: existing,
  };
}

// --- ヘルパー ---

function getSheetData_(sheetName) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  if (!sheet) return [];
  const data = sheet.getDataRange().getValues();
  if (data.length < 3) return [];
  const headers = data[0];
  const jpHeaders = HEADERS_JP[sheetName];
  // 2行目が日本語説明行ならスキップ（データは3行目から）
  const startRow = (jpHeaders && data[1][0] === jpHeaders[0]) ? 2 : 1;
  return data.slice(startRow).map((row, idx) => {
    const obj = { _row: idx + startRow + 1 };
    headers.forEach((h, i) => { obj[h] = row[i]; });
    return obj;
  });
}

function appendRow_(sheetName, values) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  sheet.appendRow(values);
}

function updateRow_(sheetName, rowNum, values) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  sheet.getRange(rowNum, 1, 1, values.length).setValues([values]);
}

function deleteRow_(sheetName, idField, id) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName);
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const idCol = headers.indexOf(idField);
  if (idCol < 0) return { error: 'ID field not found' };
  // 2行目は日本語説明行なのでスキップ（3行目=index2から検索）
  for (let i = data.length - 1; i >= 2; i--) {
    if (String(data[i][idCol]) === String(id)) {
      sheet.deleteRow(i + 1);
      return { deleted: true };
    }
  }
  return { deleted: false };
}

// --- Expenses ---

function getExpenses(yearMonth) {
  const all = getSheetData_('Expenses');
  if (yearMonth) return all.filter(e => e.year_month === yearMonth);
  return all;
}

function saveExpense(data) {
  const row = [
    data.id || Utilities.getUuid(),
    new Date().toISOString(),
    data.dateStr,
    data.dateStr.substring(0, 7),
    data.category,
    data.itemName || '',
    Number(data.amount),
    data.paymentMethod || 'cash',
    data.isFixed ? 'TRUE' : 'FALSE',
  ];
  appendRow_('Expenses', row);
  return { saved: true };
}

function bulkSaveExpenses(expenses) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName('Expenses');
  const rows = expenses.map(e => [
    e.id || Utilities.getUuid(),
    e.timestamp || new Date().toISOString(),
    e.dateStr,
    (e.yearMonth || e.dateStr.substring(0, 7)),
    e.category,
    e.itemName || '',
    Number(e.amount),
    e.paymentMethod || 'cash',
    e.isFixed ? 'TRUE' : 'FALSE',
  ]);
  if (rows.length > 0) {
    const lastRow = sheet.getLastRow();
    sheet.getRange(lastRow + 1, 1, rows.length, rows[0].length).setValues(rows);
  }
  return { saved: rows.length };
}

// --- Income ---

function getIncome(yearMonth) {
  const all = getSheetData_('Income');
  if (yearMonth) return all.filter(e => e.year_month === yearMonth);
  return all;
}

function saveIncome(data) {
  const row = [
    Utilities.getUuid(),
    new Date().toISOString(),
    data.dateStr,
    data.dateStr.substring(0, 7),
    data.source,
    Number(data.amount),
    data.memo || '',
  ];
  appendRow_('Income', row);
  return { saved: true };
}

// --- Budget ---

function getBudget(yearMonth) {
  const all = getSheetData_('Budget');
  return all.find(b => b.year_month === yearMonth) || null;
}

function saveBudget(data) {
  const all = getSheetData_('Budget');
  const existing = all.find(b => b.year_month === data.yearMonth);
  // カテゴリ別予算は { カテゴリ名: 金額 } を JSON 文字列として保存（項目の増減に追従）
  const budgets = data.budgets || {};
  const values = [
    data.yearMonth,
    Number(data.total || 0),
    JSON.stringify(budgets),
  ];
  if (existing) {
    updateRow_('Budget', existing._row, values);
  } else {
    appendRow_('Budget', values);
  }
  return { saved: true };
}

// --- WorkLog ---

function getWorkLog(yearMonth) {
  const all = getSheetData_('WorkLog');
  if (yearMonth) return all.filter(e => e.year_month === yearMonth);
  return all;
}

function saveWorkLog(data) {
  const startMin = parseTime_(data.startTime);
  const endMin = parseTime_(data.endTime);
  const workMins = endMin - startMin - Number(data.breakMinutes || 0);
  const workHours = Math.max(0, workMins / 60);
  const rate = Number(data.hourlyRate || 0);
  const dailyPay = Math.round(workHours * rate);
  const row = [
    Utilities.getUuid(),
    data.dateStr,
    data.dateStr.substring(0, 7),
    data.startTime,
    data.endTime,
    Number(data.breakMinutes || 0),
    Number(workHours.toFixed(1)),
    rate,
    dailyPay,
    data.jobName || '',
    Number(data.transportCost || 0),
  ];
  appendRow_('WorkLog', row);
  return { saved: true };
}

function parseTime_(t) {
  const parts = String(t).split(':');
  return Number(parts[0]) * 60 + Number(parts[1] || 0);
}

// --- Jobs ---

const DELETED_LABEL = '削除された項目です';

function getJobs() {
  return getSheetData_('Jobs').filter(j => j.is_active !== 'FALSE');
}

// idが既存の行に一致すれば更新、なければ新規追加（編集対応）
function saveJob(data) {
  const all = getSheetData_('Jobs');
  const existing = data.id ? all.find(j => String(j.job_id) === String(data.id)) : null;
  const row = [
    data.id || Utilities.getUuid(),
    data.storeName,
    Number(data.hourlyRate || 0),
    Number(data.dailyRate || 0),
    Number(data.transportCost || 0),
    'TRUE',
  ];
  if (existing) {
    updateRow_('Jobs', existing._row, row);
  } else {
    appendRow_('Jobs', row);
  }
  return { saved: true };
}

// バイト先削除: 過去の勤怠データで使われている場合は行を残し「削除された項目です」と記載する。
// 未使用なら行ごと削除する。
function deleteJob(id) {
  const jobs = getSheetData_('Jobs');
  const job = jobs.find(j => String(j.job_id) === String(id));
  if (!job) return { deleted: false };

  const used = getSheetData_('WorkLog').some(w => w.job_name === job.store_name);
  if (!used) {
    return deleteRow_('Jobs', 'job_id', id);
  }

  const markedName = String(job.store_name).indexOf(DELETED_LABEL) >= 0
    ? job.store_name
    : job.store_name + '（' + DELETED_LABEL + '）';
  const row = [
    job.job_id,
    markedName,
    Number(job.hourly_rate || 0),
    Number(job.daily_rate || 0),
    Number(job.transport_cost || 0),
    'FALSE',
  ];
  updateRow_('Jobs', job._row, row);
  return { deleted: true, kept: true };
}

// --- Debt ---

function getDebts() {
  return getSheetData_('Debt');
}

function saveDebt(data) {
  const row = [
    Utilities.getUuid(),
    data.dateStr,
    data.lender,
    Number(data.amount),
    data.memo || '',
    'FALSE',
    '',
    0,
  ];
  appendRow_('Debt', row);
  return { saved: true };
}

function repayDebt(data) {
  const all = getSheetData_('Debt');
  const debt = all.find(d => String(d.debt_id) === String(data.id));
  if (!debt) return { error: 'Not found' };
  const repaidAmount = Number(data.repaidAmount || debt.amount);
  const totalRepaid = Number(debt.repaid_amount || 0) + repaidAmount;
  const fullyRepaid = totalRepaid >= Number(debt.amount);
  const today = new Date().toISOString().substring(0, 10);
  const values = [
    debt.debt_id,
    debt.date_str,
    debt.lender,
    Number(debt.amount),
    debt.memo,
    fullyRepaid ? 'TRUE' : 'FALSE',
    today,
    totalRepaid,
  ];
  updateRow_('Debt', debt._row, values);
  return { saved: true, fullyRepaid: fullyRepaid };
}
