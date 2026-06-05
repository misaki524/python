# 深夜のコンビニ — 起動・ビルド手順

## 前提条件

- Ren'Py SDK 8.3.7 がインストール済み
  - パス: `/Users/kikuchi/renpy-8.3.7-sdk/`

---

## 1. デスクトップ起動

**推奨（ログ付き）:**
```bash
/Users/kikuchi/python/python/novel_game/run.sh
```

**直接起動:**
```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/python/python/novel_game
```

**モバイルエミュレーション（デスクトップ上でタッチ端末をシミュレート）:**
```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/python/python/novel_game --variant "small phone touch android mobile"
```

---

## 2. Web (HTML5) ビルド — スマホのブラウザで遊ぶ

### 2-1. Webサポートのインストール（初回のみ）

```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/renpy-8.3.7-sdk/launcher
```

1. Ren'Py ランチャーが起動する
2. 画面右下の **「設定」(Preferences)** をクリック
3. **「Webのサポートをインストール」(Install Web Support)** をクリック
4. ダウンロード完了を待つ

### 2-2. Webビルドの実行

```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/renpy-8.3.7-sdk/launcher
```

1. ランチャー左側でプロジェクト **「深夜のコンビニ」** を選択
2. **「Webをビルド」(Build Web Application)** をクリック
3. ビルド完了後、出力先フォルダが自動的に開く

出力先: プロジェクトと同じ階層に `ShinyaNoConvini-1.0-web` フォルダが生成される

### 2-3. ローカルで動作確認

```bash
cd /Users/kikuchi/python/python/ShinyaNoConvini-1.0-web
python3 -m http.server 8080
```

ブラウザで `http://localhost:8080` を開く。同じWi-Fiに接続したスマホからも、MacのIPアドレスでアクセス可能:

```
http://<MacのIPアドレス>:8080
```

MacのIPアドレスの確認方法:
```bash
ipconfig getifaddr en0
```

### 2-4. 公開する場合（itch.io）

1. [itch.io](https://itch.io) でアカウント作成
2. **Dashboard → Create new project**
3. 設定:
   - Kind of project: **HTML**
   - Upload: `ShinyaNoConvini-1.0-web` フォルダをzipにしてアップロード
   - **「This file will be played in the browser」** にチェック
   - Viewport dimensions: **1280 x 720**
   - **「Mobile friendly」** にチェック、Orientation: **Landscape**
4. Save → 公開URLをスマホで開いてプレイ

---

## 3. Android APK ビルド — スマホアプリとして配布

### 3-1. Android サポートのインストール（初回のみ）

```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/renpy-8.3.7-sdk/launcher
```

1. 画面右下の **「設定」(Preferences)** をクリック
2. **「Androidのサポートをインストール」(Install Android Support)** をクリック
3. ダウンロード完了を待つ

### 3-2. Android SDKのインストール（初回のみ）

1. ランチャーでプロジェクトを選択
2. 画面下部の **「Android」** をクリック
3. **「Install SDK & Create Keys」** をクリック
4. 画面の指示に従ってインストール（数分かかる）

### 3-3. Androidプロジェクトの設定

1. **「Configure」** をクリック
2. 以下を入力:
   - Package Name: `com.yourname.shinyanoconvini`（任意のパッケージ名）
   - App Name: `深夜のコンビニ`
   - Version: `1.0`
   - Orientation: **Landscape**（横向き）
   - Permissions: そのまま（特別な権限は不要）

### 3-4. APKビルド

1. **「Build Package」** をクリック
2. **「Universal APK」** を選択（全端末対応）
3. ビルド完了後、APKファイルの場所が表示される
4. APKファイルをスマホに転送してインストール

APKのインストール時、スマホの設定で「提供元不明のアプリを許可」が必要。

---

## 4. スマホでの操作方法

| 操作 | PC | スマホ |
|---|---|---|
| テキスト送り | Enter / クリック | **画面タップ** |
| 選択肢を選ぶ | クリック | **タップ** |
| セーブ | 右下「SAVE」ボタン | 右下 **「SAVE」タップ** |
| ロード | 右下「LOAD」ボタン | 右下 **「LOAD」タップ** |
| 手がかりリスト | Tabキー | 左下 **「手がかり」タップ** |
| スキップ | Ctrl | クイックメニュー「スキップ」 |
| メニュー | 右クリック / Esc | **2本指タップ** |
| 巻き戻し | スクロール上 | **2本指スワイプ上** |
| テキスト履歴 | クイックメニュー | クイックメニュー「ヒストリー」 |

### 画面の向き
- **横向き（ランドスケープ）** で遊んでください
- スマホの自動回転をONにしておくと自動で横になります

---

## エラーログ

- `run.sh` で起動すると `novel_game/logs/` にタイムスタンプ付きログが自動保存される
  - `YYYYMMDD_HHMMSS.log` — 起動時の標準出力・エラー出力
  - `YYYYMMDD_HHMMSS_traceback.txt` — エラー時のトレースバック（Ren'Py生成）
  - `YYYYMMDD_HHMMSS_renpy.log` — Ren'Pyのシステムログ
- ログは最大30件保持（超過分は古いものから自動削除）
- `config.developer = True` により開発者モードが有効（Shift+D でデバッグメニュー表示）

## 既知の問題・注意事項

- **フォント**: `SourceHanSansLite.ttf`（源ノ角ゴシック）を使用。Web/Android/デスクトップ全対応。
- **キャッシュクリア**: エラーが解消しない場合は、以下でキャッシュを削除してから再起動する。
  ```bash
  rm -rf novel_game/game/cache novel_game/tmp
  ```
