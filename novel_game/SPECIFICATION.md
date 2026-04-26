# 深夜のコンビニ — プロジェクト仕様書

## 1. 概要

| 項目 | 内容 |
|---|---|
| タイトル | 深夜のコンビニ |
| ジャンル | ホラー / サスペンス・ノベルゲーム |
| エンジン | Ren'Py |
| 解像度 | 1280×720 (16:9) |
| ビルド名 | ShinyaNoConvini |
| バージョン | 1.0 |

### あらすじ

大学生の安藤ユウキ（デフォルト名・変更可）は、コンビニ「ファミリーショップ立花店」の深夜バイト。
午後11時、突如として店の外に濃霧が発生し、外界との接触が断たれる。
奇妙な客、行方不明の前任者の日記、謎の少女——。
午前5時の夜明けまで生き延び、真相に辿り着けるか。

---

## 2. プロジェクト構成

```
novel_game/
└── game/
    ├── options.rpy          # ゲーム設定（タイトル、解像度、ビルド名）
    ├── gui.rpy              # ダークテーマUI定義
    ├── script.rpy           # エントリポイント、キャラクター/フラグ定義
    ├── screens.rpy          # ゲーム固有UI（手がかりリスト、エンディング一覧）
    ├── prologue.rpy         # プロローグ（PM 11:00）
    ├── chapter1.rpy         # 第1章（AM 0:00）
    ├── chapter2.rpy         # 第2章（AM 1:00）
    ├── chapter3.rpy         # 第3章（AM 2:00）
    ├── chapter4.rpy         # 第4章（AM 3:00）— 大分岐
    ├── chapter5.rpy         # 第5章（AM 4:00）— クライマックス
    ├── endings.rpy          # 全8エンディング
    └── engine/              # 汎用エンジンモジュール（再利用可能）
        ├── effects.rpy      # ビジュアルエフェクト
        ├── flags.rpy        # フラグ管理ユーティリティ
        ├── hud.rpy          # HUD（時計、コレクションリスト）
        ├── keybinds.rpy     # キーバインドトグル
        └── save_system.rpy  # エンディング登録・ギャラリー
```

---

## 3. engine/ モジュール仕様

### 3.1 engine/effects.rpy — ビジュアルエフェクト

| screen / 変数 | 引数 | 説明 |
|---|---|---|
| `flash_effect` | `flash_color="#ffffff"`, `flash_alpha=0.1`, `flash_duration=0.05` | 任意色の短時間フラッシュ。zorder 150。 |
| `color_overlay` | `overlay_color="#ff0000"`, `overlay_alpha=0.15`, `overlay_duration=0.08` | カラーオーバーレイ。ホラー演出向き。 |
| `blackout_effect` | `blackout_duration=0.5` | 完全暗転 → 自動復帰。zorder 200。 |
| `short_shake` | — | `ShakeTransition(0.3, dist=8)` 衝撃用 |
| `long_shake` | — | `ShakeTransition(0.8, dist=12)` 地震用 |

**使用例:**
```renpy
show screen flash_effect("#ffffff", 0.1, 0.05)
with short_shake
```

### 3.2 engine/flags.rpy — フラグ管理

| 関数 | 引数 | 戻り値 | 説明 |
|---|---|---|---|
| `init_flags(flag_dict)` | `dict {name: default_value}` | なし | `store` に各変数を一括設定 |
| `count_true_flags(flag_names)` | `list[str]` | `int` | 指定変数のうち `True` の数を返す |

**使用例:**
```renpy
# label start: で全フラグをリセット
$ init_flags(GAME_FLAGS)

# 手がかり数の更新
$ clue_count = count_true_flags(CLUE_FLAGS)
```

### 3.3 engine/hud.rpy — HUD部品

| screen | 引数 | 説明 |
|---|---|---|
| `generic_clock` | `time_var="current_time"`, `time_color="#00ff41"`, `clock_size=32` | 右上固定の時刻表示。store 変数名を文字列で渡す。 |
| `collection_list` | `items` (list[dict]), `title`, `screen_name`, `dismiss_key` | モーダルな一覧画面。各 dict は `{"label", "found", "detail(任意)"}` |

**items の形式:**
```python
[
    {"label": "田中の日記", "found": found_diary, "detail": "田中の日記（3ページ）"},
    {"label": "防犯カメラ", "found": found_camera},
]
```

### 3.4 engine/keybinds.rpy — キーバインドトグル

| 関数 | 引数 | 説明 |
|---|---|---|
| `register_screen_toggle(key, screen_name, action_name)` | key: Ren'Py キー名, screen_name: 表示する screen, action_name: 一意のアクション名 | 指定キーで screen の表示/非表示をトグル |

**使用例:**
```renpy
init python:
    register_screen_toggle("K_TAB", "clue_list", "clue_list_toggle")
```

### 3.5 engine/save_system.rpy — エンディング管理

| label / screen | 引数 | 説明 |
|---|---|---|
| `register_ending` (label) | `ending_key` (str) | `persistent.endings_seen` に追加、`playthrough_count` をインクリメント、永続保存 |
| `ending_gallery` (screen) | `endings_data` (list[tuple]) | タプル `(番号, タイトル, カテゴリ, key)` のリストからギャラリー表示 |

**使用例:**
```renpy
# エンディング末尾
call register_ending("ending_dawn")
return

# ギャラリー画面
screen ending_list():
    use ending_gallery(ENDINGS_DATA)
```

---

## 4. キャラクター定義

| 変数名 | 名前 | テキスト色 | 説明 |
|---|---|---|---|
| `p` | `[player_name]` (入力可) | `#87ceeb` | 主人公（デフォルト: 安藤ユウキ） |
| `suit` | スーツの男 | `#808080` | 第1章で出現する謎の男 |
| `misaki` | ミサキ | `#ffffff` | 霧の中に現れる少女 |
| `hood` | ??? | `#8b0000` | フードの人物（正体不明） |
| `sato` | 佐藤ケンジ | `#ffa500` | 前任者・田中の友人 |

---

## 5. ストーリーフラグ一覧

`GAME_FLAGS` 辞書（`script.rpy` で `define`）で一元管理。`label start:` で `init_flags(GAME_FLAGS)` により一括リセット。

| フラグ名 | 型 | デフォルト | 設定タイミング |
|---|---|---|---|
| `trust_suit` | bool | False | 第1章: スーツの男を信用した |
| `info_suit` | bool | False | 第1章: スーツの男から情報を得た |
| `found_diary` | bool | False | 第2章: 日記発見 |
| `found_camera` | bool | False | 第2章: 防犯カメラ映像発見 |
| `found_girl_clue` | bool | False | 第2章: 少女の証言入手 |
| `diary_pages_read` | int | 0 | 第2章: 日記の既読ページ数 |
| `confront_hood` | bool | False | 第3章: フードの人物に対峙 |
| `tried_police` | bool | False | 第3章: 警察に連絡を試みた |
| `observed_hood` | bool | False | 第3章: フードの人物を観察 |
| `underground` | bool | False | 第4章: 地下ルート選択 |
| `barricade` | bool | False | 第4章: バリケードルート選択 |
| `went_outside` | bool | False | 第4章: 外に出るルート選択 |
| `called_sato` | bool | False | 第4章: 佐藤に連絡ルート選択 |
| `showed_diary_to_sato` | bool | False | 第5章: 佐藤に日記を見せた |
| `ritual_success` | bool | False | 第5章: 儀式成功 |
| `accepted_doppelganger` | bool | False | 第5章: ドッペルゲンガー受入 |
| `store_manager_notes` | int | 0 | 2周目以降: 店長メモ発見数 |
| `current_time` | str | "23:00" | UI表示用の現在時刻 |
| `clue_count` | int | 0 | 手がかり数（`CLUE_FLAGS` から自動計算） |

### 手がかりフラグ

`CLUE_FLAGS = ["found_diary", "found_camera", "found_girl_clue"]`

`count_true_flags(CLUE_FLAGS)` で手がかり数を算出。

---

## 6. Persistent（永続）変数

| 変数 | 型 | 初期値 | 用途 |
|---|---|---|---|
| `persistent.endings_seen` | set | `set()` | 到達済みエンディングのキー集合 |
| `persistent.playthrough_count` | int | 0 | 周回数（2周目以降の追加コンテンツ制御） |

---

## 7. ストーリー構成

### 時系列

| 章 | ファイル | 時間帯 | 主要イベント |
|---|---|---|---|
| プロローグ | prologue.rpy | PM 11:00 | 深夜シフト開始、異変の予兆、店長メモ分岐(2周目) |
| 第1章 | chapter1.rpy | AM 0:00 | スーツの男との遭遇、3wayブランチ |
| 第2章 | chapter2.rpy | AM 1:00 | ミサキ登場、3wayアイテム探索 |
| 第3章 | chapter3.rpy | AM 2:00 | フードの人物、3wayブランチ |
| 第4章 | chapter4.rpy | AM 3:00 | **大分岐（4way）**: 地下/バリケード/外出/佐藤 |
| 第5章 | chapter5.rpy | AM 4:00 | クライマックス、儀式ルート分岐 |

### 分岐マップ

```
prologue (PM11)
  └── chapter1 (AM0)
        ├── 信用する → trust_suit
        ├── 無視する → (default)
        └── 問いただす → info_suit
              └── chapter2 (AM1)
                    ├── 日記探索 → found_diary
                    ├── カメラ確認 → found_camera
                    └── 少女の手がかり → found_girl_clue
                          └── chapter3 (AM2)
                                ├── 対峙 → confront_hood
                                ├── 通報 → tried_police
                                └── 観察 → observed_hood
                                      └── chapter4 (AM3) ★大分岐
                                            ├── 地下 → chapter5 地下ルート
                                            ├── バリケード → clue_countで自動分岐
                                            │     ├── 0-1: END 4 霧の住人
                                            │     └── 2-3: END 3 日常への帰還
                                            ├── 外出 → END 6 永遠の夜勤
                                            └── 佐藤連絡 → chapter5 佐藤ルート
```

---

## 8. エンディング一覧

| # | キー | タイトル | カテゴリ | 到達条件 |
|---|---|---|---|---|
| END 1 | `ending_dawn` | 夜明け | トゥルーエンド | 地下ルート → 儀式成功(`ritual_success`) |
| END 2 | `ending_survivor` | 生還者 | グッドエンド | 佐藤ルート → 日記を見せる |
| END 3 | `ending_normal` | 日常への帰還 | ノーマルエンド | バリケードルート × clue_count 2-3 |
| END 4 | `ending_fog` | 霧の住人 | バッドエンド | バリケードルート × clue_count 0-1 |
| END 5 | `ending_swap` | 入れ替わり | バッドエンド | 地下ルート → ドッペルゲンガー受入(`accepted_doppelganger`) |
| END 6 | `ending_eternal` | 永遠の夜勤 | バッドエンド | 外出ルート選択 |
| END 7 | `ending_predecessor` | 前任者の真実 | 隠しエンド | 佐藤ルート → 日記+カメラ発見済み |
| END 8 | `ending_manager` | 店長の秘密 | 隠しエンド | 2周目以降 × store_manager_notes ≥ 3 |

---

## 9. UI / テーマ仕様

### カラーパレット

| 用途 | 色コード |
|---|---|
| 背景 | `#0a0a0a` |
| アクセント | `#8b0000`（ダークレッド） |
| テキスト | `#e0e0e0` |
| ホバー | `#cc0000` |
| 時計 | `#00ff41`（グリーン） |
| 無効 | `#55555580` |

### HUD

- **時計表示**: 画面右上固定、`generic_clock` screen 使用
- **手がかりリスト**: Tab キートグル、`clue_list` screen（`collection_list` ベース）
- **エンディングギャラリー**: タイトルメニュー → `ending_list` screen（未到達は "???" 表示）

### ホラー演出

- `noise_effect` / `heavy_noise_effect`: 画面全体のノイズフラッシュ
- `blackout`: 暗転演出
- `short_shake` / `long_shake`: 画面揺れトランジション

---

## 10. 2周目以降の追加要素

- `persistent.playthrough_count >= 1` で以下が解放:
  - プロローグ: 店長メモの追加分岐
  - 手がかりリスト: 店長メモカウンター表示
  - END 8（店長の秘密）: 店長メモ3つ以上で到達可能

---

## 11. 音声・リソース想定

| 種別 | パス | 内容 |
|---|---|---|
| BGM | `audio/bgm/` | タイトル、通常店内、深夜、緊張、クライマックス |
| SE | `audio/sfx/` | 自動ドア、来客チャイム、蛍光灯、ノイズ |
| 背景 | `images/` | 店外、店内（通常/暗）、裏口、地下、霧 |

※ 現時点では画像・音声は未実装。定義箇所のみ存在。

---

## 12. 起動方法

### 前提条件

- Ren'Py SDK 8.3.7 がインストール済み
  - パス: `/Users/kikuchi/renpy-8.3.7-sdk/`

### 起動コマンド

**推奨（ログ付き）:**
```bash
/Users/kikuchi/python/python/novel_game/run.sh
```

**直接起動:**
```bash
/Users/kikuchi/renpy-8.3.7-sdk/renpy.sh /Users/kikuchi/python/python/novel_game
```

### エラーログ

- `run.sh` で起動すると `novel_game/logs/` にタイムスタンプ付きログが自動保存される
  - `YYYYMMDD_HHMMSS.log` — 起動時の標準出力・エラー出力
  - `YYYYMMDD_HHMMSS_traceback.txt` — エラー時のトレースバック（Ren'Py生成）
  - `YYYYMMDD_HHMMSS_renpy.log` — Ren'Pyのシステムログ
- ログは最大30件保持（超過分は古いものから自動削除）
- `config.developer = True` により開発者モードが有効（Shift+D でデバッグメニュー表示）

### 既知の問題・注意事項

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

---

## 13. ビルド設定

- `build.classify("game/**.rpy", None)` — ソースコードはアーカイブに含めない
- `build.classify("**", "archive")` — その他は archive に格納
- セーブディレクトリ: `ShinyaNoConvini-1`
