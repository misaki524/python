// ========================================
// 愚痴アプリ - バックエンド
// ========================================

const SPREADSHEET_ID ='1hEkpvDZ7csQSiT-eTXTzzSNFGz7mNGay-RGFYsinEvM';
const SHEET_ENTRIES = 'Entries';
const TIMEZONE = 'Asia/Tokyo';
const EMOTION_SCORE = { '怒り': '😡', '悲しみ': '😢', '疲れ': '😴', '不安': '😰' };
const EMOTION_NUM   = { '怒り': 1,    '悲しみ': 2,    '不安': 3,     '疲れ': 4    };
const VALID_EMOTIONS = ['怒り', '悲しみ', '疲れ', '不安'];
// ========================================
// 動作確認用（GASエディタから直接実行）
// ========================================

function testSetup() {
  try {
    var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
    Logger.log('✅ スプレッドシート接続OK: ' + ss.getName());
  } catch (e) {
    Logger.log('❌ スプレッドシート接続失敗: ' + e.message);
    Logger.log('   → SPREADSHEET_IDを正しいIDに変更してください');
    return;
  }
  var sheet = SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_ENTRIES);
  if (sheet) {
    Logger.log('✅ シート "Entries" 発見OK。行数: ' + sheet.getLastRow());
  } else {
    Logger.log('❌ シート "Entries" が見つかりません');
    Logger.log('   → シート名を "Entries" に変更してください');
  }
}

// ========================================
// エントリーポイント
// ========================================

function doGet() {
  return HtmlService.createHtmlOutputFromFile('index')
    .setTitle('愚痴アプリ')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL)
    .addMetaTag('viewport', 'width=device-width, initial-scale=1');
}

// ========================================
// ヘルパー関数
// ========================================

function getSheet_() {
  return SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_ENTRIES);
}

function getNowDate_() {
  return new Date();
}

function formatDate_(date) {
  return Utilities.formatDate(date, TIMEZONE, 'yyyy-MM-dd');
}

function formatDatetime_(date) {
  return Utilities.formatDate(date, TIMEZONE, 'yyyy-MM-dd HH:mm');
}

function formatTime_(date) {
  return Utilities.formatDate(date, TIMEZONE, 'HH:mm');
}

function generateId_() {
  return Utilities.getUuid();
}

function toDateStr_(cellValue) {
  if (cellValue instanceof Date) return formatDate_(cellValue);
  return String(cellValue).substring(0, 10);
}

// ========================================
// F-001: 愚痴エントリー保存
// ========================================

function saveEntry(emotionTag, content, intensityLevel) {
  if (!emotionTag || VALID_EMOTIONS.indexOf(emotionTag) === -1) {
    return { success: false, message: '感情タグを選択してください' };
  }
  if (!content || content.trim() === '') {
    return { success: false, message: '愚痴を入力してください' };
  }
  intensityLevel = parseInt(intensityLevel) || 3;
  if (intensityLevel < 1 || intensityLevel > 5) intensityLevel = 3;

  try {
    var sheet = getSheet_();
    if (!sheet) {
      return { success: false, message: 'シート "Entries" が見つかりません。スプレッドシートのシート名を確認してください' };
    }

    var now = getNowDate_();
    var entryId = generateId_();
    var dateStr = formatDate_(now);
    var datetimeStr = formatDatetime_(now);
    var timeStr = formatTime_(now);
    var moodEmoji = EMOTION_SCORE[emotionTag] || '';

    sheet.appendRow([
      entryId,
      now,
      dateStr,
      emotionTag,
      content.trim(),
      '',
      moodEmoji,
      intensityLevel
    ]);
    SpreadsheetApp.flush();

    // 直近の同じ感情の記録を検索
    var recentSame = '';
    var lastRow = sheet.getLastRow();
    if (lastRow > 2) {
      var allData = sheet.getRange(2, 1, lastRow - 1, 4).getValues();
      allData.sort(function(a, b) {
        var ta = a[1] instanceof Date ? a[1].getTime() : new Date(a[1]).getTime();
        var tb = b[1] instanceof Date ? b[1].getTime() : new Date(b[1]).getTime();
        return tb - ta;
      });
      for (var i = 0; i < allData.length; i++) {
        if (allData[i][0] !== entryId && allData[i][3] === emotionTag) {
          var ts = allData[i][1] instanceof Date ? allData[i][1] : new Date(allData[i][1]);
          recentSame = formatDatetime_(ts);
          break;
        }
      }
    }

    return {
      success: true,
      message: '保存しました',
      entry: {
        id: entryId,
        datetime: datetimeStr,
        time: timeStr,
        emotionTag: emotionTag,
        content: content.trim(),
        moodEmoji: moodEmoji,
        intensityLevel: intensityLevel
      },
      recentSame: recentSame
    };

  } catch (e) {
    return { success: false, message: 'エラー: ' + e.message };
  }
}

// ========================================
// F-002: エントリー一覧取得（新しい順）
// ========================================

function getEntries(offsetRows, limitRows) {
  offsetRows = offsetRows || 0;
  limitRows = limitRows || 20;

  var sheet = getSheet_();
  var lastRow = sheet.getLastRow();

  if (lastRow <= 1) {
    return { success: true, entries: [], hasMore: false, totalCount: 0 };
  }

  var maxCol = 8;
  var data = sheet.getRange(2, 1, lastRow - 1, maxCol).getValues();

  // 日時（列B, index1）で降順ソート
  data.sort(function(a, b) {
    var ta = a[1] instanceof Date ? a[1].getTime() : new Date(a[1]).getTime();
    var tb = b[1] instanceof Date ? b[1].getTime() : new Date(b[1]).getTime();
    return tb - ta;
  });

  var totalCount = data.length;
  var slice = data.slice(offsetRows, offsetRows + limitRows);

  var entries = slice.map(function(row) {
    var ts = row[1] instanceof Date ? row[1] : new Date(row[1]);
    return {
      id: row[0],
      datetime: formatDatetime_(ts),
      date: toDateStr_(row[2]),
      time: formatTime_(ts),
      emotionTag: row[3],
      content: row[4],
      moodEmoji: row[6],
      intensityLevel: row[7] || 3
    };
  });

  return {
    success: true,
    entries: entries,
    hasMore: totalCount > offsetRows + limitRows,
    totalCount: totalCount
  };
}

// ========================================
// F-003: ムードトレンドデータ取得
// ========================================

function getMoodTrend(days) {
  days = days || 30;

  var sheet = getSheet_();
  var lastRow = sheet.getLastRow();

  if (lastRow <= 1) {
    return { success: true, data: [], summary: { total: 0, topEmotion: '-', busiestDay: '-' } };
  }

  var maxCol = 8;
  var data = sheet.getRange(2, 1, lastRow - 1, maxCol).getValues();

  // 対象期間の開始日を計算
  var now = getNowDate_();
  var cutoffDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);
  var cutoffStr = formatDate_(cutoffDate);

  // 期間内のデータをフィルタリング
  var filtered = data.filter(function(row) {
    var dateStr = toDateStr_(row[2]);
    return dateStr >= cutoffStr;
  });

  // 日付ごとにグループ化
  var byDate = {};
  var emotionTotals = {};
  VALID_EMOTIONS.forEach(function(e) { emotionTotals[e] = 0; });

  var dateIntensities = {};
  var totalIntensitySum = 0;
  var totalIntensityCount = 0;

  filtered.forEach(function(row) {
    var dateStr = toDateStr_(row[2]);
    var emotion = row[3];
    var intensity = parseInt(row[7]) || 3;
    if (!byDate[dateStr]) {
      byDate[dateStr] = {};
      VALID_EMOTIONS.forEach(function(e) { byDate[dateStr][e] = 0; });
    }
    if (!dateIntensities[dateStr]) {
      dateIntensities[dateStr] = [];
    }
    if (emotion && byDate[dateStr][emotion] !== undefined) {
      byDate[dateStr][emotion]++;
      emotionTotals[emotion]++;
    }
    dateIntensities[dateStr].push(intensity);
    totalIntensitySum += intensity;
    totalIntensityCount++;
  });

  // 日付昇順でデータ配列を構築
  var dates = Object.keys(byDate).sort();
  var trendData = dates.map(function(dateStr) {
    var counts = byDate[dateStr];
    var dominant = VALID_EMOTIONS.reduce(function(a, b) {
      return counts[a] >= counts[b] ? a : b;
    });
    var intensities = dateIntensities[dateStr] || [3];
    var avgIntensity = Math.round(intensities.reduce(function(a, b) { return a + b; }, 0) / intensities.length * 10) / 10;
    return {
      date: dateStr,
      counts: counts,
      dominantTag: dominant,
      moodScore: avgIntensity,
      moodEmoji: EMOTION_SCORE[dominant] || ''
    };
  });

  // サマリー計算
  var topEmotion = VALID_EMOTIONS.reduce(function(a, b) {
    return emotionTotals[a] >= emotionTotals[b] ? a : b;
  });
  var busiestDay = '-';
  var maxCount = 0;
  dates.forEach(function(d) {
    var count = VALID_EMOTIONS.reduce(function(sum, e) { return sum + byDate[d][e]; }, 0);
    if (count > maxCount) { maxCount = count; busiestDay = d; }
  });

  var avgIntensity = totalIntensityCount > 0 ? Math.round(totalIntensitySum / totalIntensityCount * 10) / 10 : '-';

  return {
    success: true,
    data: trendData,
    summary: {
      total: filtered.length,
      topEmotion: filtered.length > 0 ? topEmotion : '-',
      busiestDay: busiestDay,
      emotionTotals: emotionTotals,
      avgIntensity: avgIntensity
    }
  };
}

// ========================================
// F-004: エントリー削除
// ========================================

function deleteEntry(entryId) {
  if (!entryId) {
    return { success: false, message: 'IDが指定されていません' };
  }

  var sheet = getSheet_();
  var lastRow = sheet.getLastRow();

  if (lastRow <= 1) {
    return { success: false, message: '見つかりませんでした' };
  }

  var ids = sheet.getRange(2, 1, lastRow - 1, 1).getValues();
  for (var i = 0; i < ids.length; i++) {
    if (ids[i][0] === entryId) {
      sheet.deleteRow(i + 2);
      SpreadsheetApp.flush();
      return { success: true, message: '削除しました' };
    }
  }

  return { success: false, message: '見つかりませんでした' };
}
