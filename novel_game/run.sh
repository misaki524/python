#!/bin/bash
# run.sh — 深夜のコンビニ 起動スクリプト
# エラーが発生した場合、logs/ ディレクトリにタイムスタンプ付きログを保存する

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RENPY_SDK="/Users/kikuchi/renpy-8.3.7-sdk"
PROJECT_DIR="$SCRIPT_DIR"
LOG_DIR="$PROJECT_DIR/logs"

mkdir -p "$LOG_DIR"

# 前回のエラーファイルをクリア
> "$PROJECT_DIR/errors.txt" 2>/dev/null
> "$PROJECT_DIR/traceback.txt" 2>/dev/null

TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="$LOG_DIR/${TIMESTAMP}.log"

echo "========================================" | tee "$LOG_FILE"
echo "深夜のコンビニ — 起動ログ" | tee -a "$LOG_FILE"
echo "日時: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# Ren'Py起動（stdout/stderrをログに記録しつつ画面にも表示）
"$RENPY_SDK/renpy.sh" "$PROJECT_DIR" 2>&1 | tee -a "$LOG_FILE"
EXIT_CODE=${PIPESTATUS[0]}

echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "終了コード: $EXIT_CODE" >> "$LOG_FILE"
echo "終了日時: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "⚠ エラーが発生しました（終了コード: $EXIT_CODE）"
    echo "ログファイル: $LOG_FILE"

    # Ren'Pyのtraceback.txtもコピー
    if [ -f "$PROJECT_DIR/traceback.txt" ]; then
        cp "$PROJECT_DIR/traceback.txt" "$LOG_DIR/${TIMESTAMP}_traceback.txt"
        echo "トレースバック: $LOG_DIR/${TIMESTAMP}_traceback.txt"
    fi
    if [ -f "$PROJECT_DIR/log.txt" ]; then
        cp "$PROJECT_DIR/log.txt" "$LOG_DIR/${TIMESTAMP}_renpy.log"
    fi
fi

# 古いログを30件まで保持（超過分は削除）
cd "$LOG_DIR" && ls -t *.log 2>/dev/null | tail -n +31 | xargs rm -f 2>/dev/null

exit $EXIT_CODE
