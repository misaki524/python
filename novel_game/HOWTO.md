# 深夜のコンビニ — 起動方法

## 前提条件

- Ren'Py SDK 8.3.7 がインストール済み
  - パス: `/Users/kikuchi/renpy-8.3.7-sdk/`

## 起動コマンド

**推奨（ログ付き）:**
```bash
/Users/kikuchi/python/python/novel_game/run.sh
```

**直接起動:**
```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/python/python/novel_game
```

## エラーログ

- `run.sh` で起動すると `novel_game/logs/` にタイムスタンプ付きログが自動保存される
  - `YYYYMMDD_HHMMSS.log` — 起動時の標準出力・エラー出力
  - `YYYYMMDD_HHMMSS_traceback.txt` — エラー時のトレースバック（Ren'Py生成）
  - `YYYYMMDD_HHMMSS_renpy.log` — Ren'Pyのシステムログ
- ログは最大30件保持（超過分は古いものから自動削除）
- `config.developer = True` により開発者モードが有効（Shift+D でデバッグメニュー表示）

## 既知の問題・注意事項

- **文字化け**: ~~解消済み~~ — Ren'Py SDK付属の `SourceHanSansLite.ttf`（源ノ角ゴシック）を `game/` に配置し、`gui.rpy` のフォント設定を変更済み。
  ```
  gui.rpy:
    define gui.text_font = "SourceHanSansLite.ttf"
    define gui.name_text_font = "SourceHanSansLite.ttf"
    define gui.interface_text_font = "SourceHanSansLite.ttf"
  ```
- **画像・音声未実装**: `images/` `audio/` フォルダのリソースは未配置。実行時に画像/音声が見つからない旨の警告が出る場合がある。
- **キャッシュクリア**: エラーが解消しない場合は、以下でキャッシュを削除してから再起動する。
  ```bash
  rm -rf novel_game/game/cache novel_game/tmp
  ```
