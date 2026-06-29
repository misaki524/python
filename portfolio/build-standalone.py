#!/usr/bin/env python3
"""index.html と assets/ を 1 つの HTML ファイルにまとめる。

画像は表示用に軽量化（JPEG・最大1280px）して base64 で埋め込むため、
出力された単一ファイルだけで、フォルダ無し・ネット接続無しで閲覧できます。

出力:
  portfolio/dist/index.html   … ローカル閲覧用（ダブルクリックで開ける）
  docs/index.html             … GitHub Pages 公開用（main の docs/ をPages設定で配信）

使い方:  python3 portfolio/build-standalone.py
"""
import base64
import pathlib
import re
import subprocess
import tempfile

HERE = pathlib.Path(__file__).parent
REPO_ROOT = HERE.parent
SRC = HERE / "index.html"
DIST = HERE / "dist" / "index.html"
DOCS = REPO_ROOT / "docs" / "index.html"
MAX_PX = 1280       # 長辺の最大ピクセル
JPEG_QUALITY = 82   # 画質 (0-100)

tmp = pathlib.Path(tempfile.mkdtemp())


def to_data_uri(rel_path: str) -> str:
    png = HERE / rel_path
    out = tmp / (png.stem + ".jpg")
    # macOS 標準の sips で JPEG 変換＋リサイズ
    subprocess.run(
        ["sips", "-s", "format", "jpeg",
         "-s", "formatOptions", str(JPEG_QUALITY),
         "-Z", str(MAX_PX), str(png), "--out", str(out)],
        check=True, capture_output=True,
    )
    b64 = base64.b64encode(out.read_bytes()).decode()
    return f"data:image/jpeg;base64,{b64}"


html = SRC.read_text(encoding="utf-8")
html = re.sub(r'src="(assets/[^"]+)"', lambda m: f'src="{to_data_uri(m.group(1))}"', html)

for out_path in (DIST, DOCS):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

# Jekyll処理を無効化（先頭がアンダースコアのパス等を素通しさせる）
(DOCS.parent / ".nojekyll").touch()

size_mb = DIST.stat().st_size / 1024 / 1024
print(f"作成しました ({size_mb:.1f} MB):")
print(f"  portfolio/dist/index.html  … ローカル閲覧用（ダブルクリックで開ける）")
print(f"  docs/index.html            … GitHub Pages 公開用（commit & push で反映）")
