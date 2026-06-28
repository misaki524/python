// ========================================
// 勤怠管理アプリ - バックエンド
// ========================================

// スプレッドシートID（デプロイ時に設定してください）
const SPREADSHEET_ID = '1lYb_NpHho6Baa3DjF3UKVQ7nJIBWu_T4XwcHXlwvwh0';

// シート名
const SHEET_ATTENDANCE = 'Attendance';
const SHEET_BREAKS = 'Breaks';
const SHEET_DAILY_REPORT = 'DailyReport';

// タイムゾーン
const TIMEZONE = 'Asia/Tokyo';

// ========================================
// エントリーポイント
// ========================================

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('勤怠管理アプリ')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// ========================================
// ヘルパー関数
// ========================================

function getSheet_(name) {
  return SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(name);
}

function getTodayStr_() {
  return Utilities.formatDate(new Date(), TIMEZONE, 'yyyy-MM-dd');
}

function getNow_() {
  return new Date();
}

function formatTime_(date) {
  return Utilities.formatDate(date, TIMEZONE, 'HH:mm');
}

function formatDate_(date) {
  return Utilities.formatDate(date, TIMEZONE, 'yyyy-MM-dd');
}

/**
 * セルの値からHH:mm形式の文字列を安全に取得する。
 * Google Sheetsが時刻をDate型に変換する場合があるため対応。
 */
function toTimeStr_(cellValue) {
  if (!cellValue && cellValue !== 0) return '';
  if (cellValue instanceof Date) {
    return Utilities.formatDate(cellValue, TIMEZONE, 'HH:mm');
  }
  var s = String(cellValue).trim();
  // HH:mm形式ならそのまま
  if (/^\d{1,2}:\d{2}$/.test(s)) return s;
  return s;
}

/**
 * 指定シートから当日の行を検索し、[行番号, 行データ] の配列を返す。
 * 見つからない場合は空配列。
 */
function findTodayRows_(sheetName) {
  var sheet = getSheet_(sheetName);
  var lastRow = sheet.getLastRow();
  if (lastRow <= 1) return [];
  // 全列を確実に読み取る（getDataRangeだと空列が含まれない場合がある）
  var maxCol = Math.max(sheet.getLastColumn(), 5);
  var data = sheet.getRange(1, 1, lastRow, maxCol).getValues();
  var todayStr = getTodayStr_();
  var results = [];

  for (var i = 1; i < data.length; i++) {
    var cellDate = data[i][0];
    var dateStr = '';
    if (cellDate instanceof Date) {
      dateStr = formatDate_(cellDate);
    } else {
      dateStr = String(cellDate).substring(0, 10);
    }
    if (dateStr === todayStr) {
      results.push({ row: i + 1, data: data[i] });
    }
  }
  return results;
}

/**
 * 時間差を "H:mm" 形式の文字列で返す
 */
function calcDuration_(startTimeStr, endTimeStr) {
  var today = getTodayStr_();
  var start = new Date(today + 'T' + startTimeStr + ':00');
  var end = new Date(today + 'T' + endTimeStr + ':00');
  var diffMs = end.getTime() - start.getTime();
  var diffMin = Math.floor(diffMs / 60000);
  var h = Math.floor(diffMin / 60);
  var m = diffMin % 60;
  return h + ':' + ('0' + m).slice(-2);
}

/**
 * "H:mm" 形式の時間文字列を分に変換
 */
function durationToMinutes_(durationStr) {
  if (!durationStr) return 0;
  var parts = durationStr.split(':');
  return parseInt(parts[0], 10) * 60 + parseInt(parts[1], 10);
}

/**
 * 分を "H:mm" 形式の文字列に変換
 */
function minutesToDuration_(minutes) {
  var h = Math.floor(minutes / 60);
  var m = minutes % 60;
  return h + ':' + ('0' + m).slice(-2);
}

// ========================================
// F-001: 出勤打刻（1日複数回対応）
// ========================================

function clockIn() {
  var rows = findTodayRows_(SHEET_ATTENDANCE);

  // 未退勤のセッションがあれば出勤不可
  for (var i = 0; i < rows.length; i++) {
    if (!toTimeStr_(rows[i].data[2])) {
      return { success: false, message: '既に出勤中です。先に退勤してください' };
    }
  }

  var sheet = getSheet_(SHEET_ATTENDANCE);
  var now = getNow_();
  var timeStr = formatTime_(now);

  sheet.appendRow([
    new Date(getTodayStr_() + 'T00:00:00'),
    timeStr,
    '',
    '',
    '出勤中'
  ]);
  SpreadsheetApp.flush();

  var sessionNum = rows.length + 1;
  return { success: true, message: '出勤しました (' + timeStr + ') [第' + sessionNum + '回]' };
}

// ========================================
// F-002: 退勤打刻（最新の未退勤セッションを閉じる）
// ========================================

function clockOut() {
  var attRows = findTodayRows_(SHEET_ATTENDANCE);

  // 最新の未退勤セッションを探す
  var activeRow = null;
  for (var i = attRows.length - 1; i >= 0; i--) {
    if (!toTimeStr_(attRows[i].data[2])) {
      activeRow = attRows[i];
      break;
    }
  }

  if (!activeRow) {
    return { success: false, message: '出勤中の記録がありません' };
  }

  // 休憩中チェック
  var breakRows = findTodayRows_(SHEET_BREAKS);
  for (var i = 0; i < breakRows.length; i++) {
    if (!toTimeStr_(breakRows[i].data[2])) {
      return { success: false, message: '休憩中は退勤できません。先に休憩を終了してください' };
    }
  }

  var sheet = getSheet_(SHEET_ATTENDANCE);
  var now = getNow_();
  var timeStr = formatTime_(now);

  // このセッション中の休憩時間を計算
  var clockInStr = toTimeStr_(activeRow.data[1]);
  var totalBreakMin = 0;
  for (var j = 0; j < breakRows.length; j++) {
    var bStart = toTimeStr_(breakRows[j].data[1]);
    var bEnd = toTimeStr_(breakRows[j].data[2]);
    // 出勤時刻以降の休憩のみカウント
    if (bStart >= clockInStr && bEnd) {
      totalBreakMin += durationToMinutes_(toTimeStr_(breakRows[j].data[3]));
    }
  }

  // 勤務時間 = 退勤 - 出勤 - 休憩合計
  var today = getTodayStr_();
  var startTime = new Date(today + 'T' + clockInStr + ':00');
  var endTime = now;
  var workMs = endTime.getTime() - startTime.getTime() - (totalBreakMin * 60000);
  var workMin = Math.max(0, Math.floor(workMs / 60000));
  var workHours = minutesToDuration_(workMin);

  var rowNum = activeRow.row;
  sheet.getRange(rowNum, 3).setValue(timeStr);       // 退勤時刻
  sheet.getRange(rowNum, 4).setValue(workHours);      // 勤務時間
  sheet.getRange(rowNum, 5).setValue('退勤済');        // ステータス
  SpreadsheetApp.flush();

  return {
    success: true,
    message: '退勤しました (' + timeStr + ')\n勤務時間: ' + workHours
  };
}

// ========================================
// F-003: 休憩開始
// ========================================

function breakStart() {
  // 出勤チェック（最新の未退勤セッションがあるか）
  var attRows = findTodayRows_(SHEET_ATTENDANCE);
  var isActive = false;
  for (var i = attRows.length - 1; i >= 0; i--) {
    if (!toTimeStr_(attRows[i].data[2])) {
      isActive = true;
      break;
    }
  }
  if (!isActive) {
    return { success: false, message: '出勤中ではありません' };
  }

  // 既に休憩中チェック
  var breakRows = findTodayRows_(SHEET_BREAKS);
  for (var i = 0; i < breakRows.length; i++) {
    if (!toTimeStr_(breakRows[i].data[2])) {
      return { success: false, message: '既に休憩中です' };
    }
  }

  var sheet = getSheet_(SHEET_BREAKS);
  var now = getNow_();
  var timeStr = formatTime_(now);

  sheet.appendRow([
    new Date(getTodayStr_() + 'T00:00:00'),
    timeStr,
    '',
    ''
  ]);
  SpreadsheetApp.flush();

  return { success: true, message: '休憩開始 (' + timeStr + ')' };
}

// ========================================
// F-004: 休憩終了
// ========================================

function breakEnd() {
  var breakRows = findTodayRows_(SHEET_BREAKS);
  var ongoingBreak = null;

  for (var i = breakRows.length - 1; i >= 0; i--) {
    if (!toTimeStr_(breakRows[i].data[2])) {
      ongoingBreak = breakRows[i];
      break;
    }
  }

  if (!ongoingBreak) {
    return { success: false, message: '休憩中の記録がありません' };
  }

  var sheet = getSheet_(SHEET_BREAKS);
  var now = getNow_();
  var timeStr = formatTime_(now);
  var bStartStr = toTimeStr_(ongoingBreak.data[1]);
  var duration = calcDuration_(bStartStr, timeStr);

  var rowNum = ongoingBreak.row;
  sheet.getRange(rowNum, 3).setValue(timeStr);     // 休憩終了
  sheet.getRange(rowNum, 4).setValue(duration);    // 休憩時間
  SpreadsheetApp.flush();

  return {
    success: true,
    message: '休憩終了 (' + timeStr + ')\n休憩時間: ' + duration
  };
}

// ========================================
// F-005: 日報保存
// 列構成: A:日付 / B:タスク内容 / C:反省など / D:コメント
// コメント(D列)は別の人が記入するためアプリからは書き換えない。
// ========================================

function saveReport(task, reflection) {
  var sheet = getSheet_(SHEET_DAILY_REPORT);
  var rows = findTodayRows_(SHEET_DAILY_REPORT);
  var taskVal = task || '';
  var reflectionVal = reflection || '';

  if (rows.length > 0) {
    // 更新（タスク内容・反省などのみ。コメント列は触らない）
    var rowNum = rows[0].row;
    sheet.getRange(rowNum, 2).setValue(taskVal);        // B: タスク内容
    sheet.getRange(rowNum, 3).setValue(reflectionVal);  // C: 反省など
    return { success: true, message: '日報を更新しました' };
  } else {
    // 新規作成（コメント列は空欄でスタート）
    sheet.appendRow([
      new Date(getTodayStr_() + 'T00:00:00'),
      taskVal,
      reflectionVal,
      ''
    ]);
    return { success: true, message: '日報を保存しました' };
  }
}

// ========================================
// F-007: 本日情報取得
// ========================================

function getTodayStatus() {
  var now = getNow_();
  var result = {
    date: getTodayStr_(),
    currentTime: formatTime_(now),
    sessions: [],
    totalWorkHours: '',
    currentStatus: '',
    breaks: [],
    task: '',
    reflection: '',
    comment: ''
  };

  // 勤怠情報（複数セッション対応）
  var attRows = findTodayRows_(SHEET_ATTENDANCE);
  var totalWorkMin = 0;
  var hasActiveSession = false;

  for (var i = 0; i < attRows.length; i++) {
    var att = attRows[i].data;
    var clockIn = toTimeStr_(att[1]);
    var clockOut = toTimeStr_(att[2]);
    var workH = toTimeStr_(att[3]) || '';
    var isActive = !clockOut;

    if (isActive) hasActiveSession = true;
    if (workH) totalWorkMin += durationToMinutes_(workH);

    result.sessions.push({
      num: i + 1,
      clockIn: clockIn,
      clockOut: clockOut,
      workHours: workH,
      active: isActive
    });
  }

  result.totalWorkHours = totalWorkMin > 0 ? minutesToDuration_(totalWorkMin) : '';

  // ステータス判定
  var breakRows = findTodayRows_(SHEET_BREAKS);
  var isOnBreak = false;
  for (var j = 0; j < breakRows.length; j++) {
    var b = breakRows[j].data;
    var bEnd = toTimeStr_(b[2]);
    if (!bEnd) isOnBreak = true;
    result.breaks.push({
      start: toTimeStr_(b[1]),
      end: bEnd,
      duration: toTimeStr_(b[3]) || ''
    });
  }

  if (attRows.length === 0) {
    result.currentStatus = '';
  } else if (hasActiveSession && isOnBreak) {
    result.currentStatus = '休憩中';
  } else if (hasActiveSession) {
    result.currentStatus = '出勤中';
  } else {
    result.currentStatus = '退勤済';
  }

  // 日報情報（B:タスク内容 / C:反省など / D:コメント）
  var reportRows = findTodayRows_(SHEET_DAILY_REPORT);
  if (reportRows.length > 0) {
    var rep = reportRows[0].data;
    result.task = rep[1] || '';
    result.reflection = rep[2] || '';
    result.comment = rep[3] || '';
  }

  return result;
}
