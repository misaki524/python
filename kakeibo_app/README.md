# 家計簿アプリ

Google スプレッドシートを DB として使う、スマホ向けのシンプルな家計簿アプリです。
フロントエンドは Vue 3 + Vite、バックエンドは Google Apps Script（GAS）経由でスプレッドシートに読み書きします。

## 主な機能

| タブ | パス | 機能 |
|------|------|------|
| 月の支出 | `/monthly` | 当月の支出一覧・入力・合計 |
| 週の支出 | `/weekly` | 今週の支出一覧・合計・日平均 |
| 収入・収支 | `/income` | 収入入力・月間収支 |
| 予算 | `/budget` | 予算設定・消化率・残額計算 |
| バイト | `/work` | 勤怠入力・バイト先管理・月間集計 |
| 借金 | `/debt` | 借金一覧・返済管理 |
| 分析 | `/analysis` | グラフ・収支・節約日カウント |
| 取込 | `/import` | 既存スプレッドシートから CSV 取込 |
| 設定 | `/settings` | GAS URL 設定・カテゴリ管理 |

## 技術スタック

- **フロントエンド**: Vue 3（`<script setup>`）+ Vue Router + Vite
- **バックエンド/DB**: Google Apps Script + Google スプレッドシート（5シート: Expenses / Income / Budget / WorkLog / Debt）
- **グラフ**: Chart.js
- **CSV 取込**: PapaParse
- **PWA**: manifest + Service Worker（ホーム画面追加・オフライン表示に対応）

## セットアップ

### 1. 依存インストール

```bash
npm install
```

### 2. GAS バックエンドを用意

1. 新しい Google スプレッドシートを作成
2. 拡張機能 → Apps Script を開き、[`docs/gas-code.js`](docs/gas-code.js) の内容を貼り付け
3. 「デプロイ」→「新しいデプロイ」→ 種類「ウェブアプリ」
   - 実行ユーザー: 自分
   - アクセスできるユーザー: **全員**（必須。「自分のみ」だとアプリから呼べません）
4. 発行された **ウェブアプリ URL** を控える

### 3. アプリを起動して GAS URL を設定

```bash
npm run dev
```

ブラウザで開いたら「設定」タブに GAS URL を入力して保存します（`localStorage` に保存）。
初回は設定画面の初期化ボタンで 5 シートを自動作成できます。

詳しいアクセス方法・スマホでの開き方は [`docs/access-guide.md`](docs/access-guide.md)、
既存データの取込手順は [`docs/csv-import-guide.md`](docs/csv-import-guide.md) を参照してください。

## 開発コマンド

```bash
npm run dev       # 開発サーバ起動
npm run build     # 本番ビルド（dist/ に出力）
npm run preview   # ビルド結果をローカルでプレビュー
node scripts/gen-icons.mjs  # PWA アイコン(PNG)を再生成
```

## デプロイ

`npm run build` で生成される `dist/` を静的ホスティング（Netlify / Cloudflare Pages 等）に配置します。
SPA のため、`dist/_redirects`（`/* /index.html 200`）でフォールバックを設定済みです。

## PWA（ホーム画面に追加）

スマホのブラウザで開き、共有メニューから「ホーム画面に追加」するとアプリとして起動できます
（アイコン・スプラッシュ・スタンドアロン表示に対応）。Service Worker は本番ビルド時のみ有効です。

## ドキュメント

- [設計書](docs/design.md)
- [アクセスガイド](docs/access-guide.md)
- [CSV 取込ガイド](docs/csv-import-guide.md)
- [GAS バックエンドコード](docs/gas-code.js)
