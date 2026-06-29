---
name: portfolio-build
description: Rebuild the portfolio's deployable HTML from portfolio/index.html and publish it via GitHub Pages (docs/ folder on main). Use after editing portfolio/index.html or anything under portfolio/assets/, so both the local preview (portfolio/dist/index.html) and the published version (docs/index.html) stay in sync — or whenever asked to build, regenerate, deploy, or publish the portfolio.
---

# Portfolio build & deploy (GitHub Pages)

The portfolio lives in `portfolio/`. **`portfolio/index.html` is the single source of truth** (CSS + JS are inlined; images are referenced from `portfolio/assets/`).

`portfolio/build-standalone.py` regenerates the deployable file with images downscaled and base64-embedded, so it opens with no folder and no network. It writes to **two locations**:

- **`portfolio/dist/index.html`** — local preview (`open` で確認できる)。
- **`docs/index.html`** — GitHub Pages 公開用。`main` ブランチの `docs/` フォルダを Pages の配信元に設定してあるので、push したら自動デプロイされる。
- **`docs/.nojekyll`** — Jekyll 処理を無効化するための空ファイル（スクリプトが自動で作成）。

## When to run

`portfolio/index.html` か `portfolio/assets/` 配下のどれかを変更したら毎回。出力2つが古くなるのを防ぐため。

## Steps

1. リポジトリのルートからビルドを実行（スクリプトは自分の位置から相対でパスを解決するので `cd` 不要）:

   ```bash
   python3 portfolio/build-standalone.py
   ```

   macOS の `sips`（画像変換用、標準搭載）を使う。

2. 出力サイズを確認:

   ```bash
   ls -la portfolio/dist/index.html docs/index.html
   ```

3. デプロイ（GitHub Pages）:

   ```bash
   git add docs/index.html docs/.nojekyll portfolio/dist/index.html portfolio/index.html portfolio/assets/
   git commit -m "portfolio: 内容更新（GitHub Pagesに反映）"
   git push origin main
   ```

   push 後 1〜2分で GitHub Pages に反映される。公開URLは GitHub リポジトリの **Settings → Pages** で確認できる（初回設定: Source = `Deploy from a branch`, Branch = `main`, Folder = `/docs`）。

## Notes

- **手で編集しないこと**: `portfolio/dist/index.html` と `docs/index.html` は生成物。`portfolio/index.html` を編集して再ビルドする。
- `assets/` に新しい画像を足したら、ビルド時に `src="assets/..."` がすべて data URI に書き換えられて埋め込まれる。
- 画像は最大 1280px・JPEG 品質 82 に縮小してから埋め込み（`MAX_PX` / `JPEG_QUALITY` で調整可）。
- 旧フロー（Netlify Drop に `portfolio/dist/` をドラッグ）は廃止。GitHub Pages に一本化。
