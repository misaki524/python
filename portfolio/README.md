# 開発ポートフォリオ

個人開発・趣味開発で制作したWebアプリ／ゲームをまとめたポートフォリオサイトです。
個人を特定する情報（氏名・所属・連絡先など）は含めていません。

## 掲載作品

| # | 作品 | 種別 | 主な技術 |
|---|------|------|----------|
| 01 | 家計簿アプリ | Web App / SPA | Vue.js 3, Vite, Chart.js, Google Apps Script |
| 02 | ノベルゲーム「深夜のコンビニ」 | Game | Ren'Py, Python |
| 03 | 勤怠管理アプリ | Web App / PWA | Google Apps Script, Google Sheets |

## 構成

```
portfolio/
├── index.html      # ポートフォリオ本体（CSS・JS埋め込みの単一ファイル）
├── assets/         # スクリーンショット画像
└── README.md       # このファイル
```

## 閲覧方法

`index.html` をダブルクリックするだけで表示できます（ビルド不要・ネット接続不要）。

Web に公開したい場合は、`portfolio` フォルダをそのまま静的ホスティングに置くだけです。
例：[Netlify Drop](https://app.netlify.com/drop) にフォルダをドラッグ＆ドロップ。

## 備考

- スクリーンショットはノベルゲームのゲーム画面です。
- 各Webアプリは個人利用を前提としたサーバーレス構成（Google Apps Script + スプレッドシート）で稼働しています。
