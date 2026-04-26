## script.rpy — エントリポイント、キャラクター定義、変数定義

# ============================================================
# 背景画像定義
# ============================================================

image bg_store_front = "images/bg/コンビニの店内.jpg"
image bg_store_front_fog = "images/bg/霧.jpg"
image bg_store_inside = "images/bg/コンビニの店内.jpg"
image bg_store_inside_dark = "images/bg/コンビニの店内.jpg"
image bg_backyard = "images/bg/街中の横断歩道（夜・赤信号）.jpg"
image bg_underground = Solid("#0a0a10")
image bg_fog = "images/bg/霧.jpg"
image bg_room = "images/bg/部屋.jpg"

# ============================================================
# キャラクター画像定義（プレースホルダー）
# ============================================================

image chara_suit = Solid("#00000000")
image chara_girl = Solid("#00000000")
image chara_girl_smile = Solid("#00000000")
image chara_hood = Solid("#00000000")

# ============================================================
# キャラクター定義
# ============================================================

define player_name = "安藤ユウキ"
define p = Character("[player_name]", color="#87ceeb")
define suit = Character("スーツの男", color="#808080")
define misaki = Character("ミサキ", color="#ffffff")
define hood = Character("???", color="#8b0000")
define sato = Character("佐藤ケンジ", color="#ffa500")

# ============================================================
# ストーリーフラグ（default宣言 — Ren'Py 初回定義用）
# ============================================================

# 第1章: スーツの男
default trust_suit = False
default info_suit = False

# 第2章: 探索・手がかり
default found_diary = False
default found_camera = False
default found_girl_clue = False
default diary_pages_read = 0

# 第3章: フードの人物
default confront_hood = False
default tried_police = False
default observed_hood = False

# 第4章: 核心の大分岐
default underground = False
default barricade = False
default went_outside = False
default called_sato = False

# 第5章: 追加フラグ
default showed_diary_to_sato = False
default ritual_success = False
default accepted_doppelganger = False

# 店長メモ（2周目以降）
default store_manager_notes = 0

# UI用
default current_time = "23:00"
default clue_count = 0

# engine/flags.rpy の init_flags() で一括リセット用辞書
define GAME_FLAGS = {
    "trust_suit": False,
    "info_suit": False,
    "found_diary": False,
    "found_camera": False,
    "found_girl_clue": False,
    "diary_pages_read": 0,
    "confront_hood": False,
    "tried_police": False,
    "observed_hood": False,
    "underground": False,
    "barricade": False,
    "went_outside": False,
    "called_sato": False,
    "showed_diary_to_sato": False,
    "ritual_success": False,
    "accepted_doppelganger": False,
    "store_manager_notes": 0,
    "current_time": "23:00",
    "clue_count": 0,
}

# 手がかりフラグ名リスト（count_true_flags用）
define CLUE_FLAGS = ["found_diary", "found_camera", "found_girl_clue"]

# ============================================================
# 周回用persistent変数
# ============================================================

default persistent.endings_seen = set()
default persistent.playthrough_count = 0

# ============================================================
# ゲーム開始
# ============================================================

label start:

    # 名前入力
    $ player_name = renpy.input("名前を入力してください（空欄でデフォルト）", default="安藤ユウキ", length=12)
    $ player_name = player_name.strip()
    if player_name == "":
        $ player_name = "安藤ユウキ"

    # 変数一括初期化（engine/flags.rpy）
    $ init_flags(GAME_FLAGS)

    jump prologue


# ============================================================
# 手がかり数計算（各章の先頭で呼ぶ）
# engine/flags.rpy の count_true_flags() を利用
# ============================================================

label update_clue_count:
    $ clue_count = count_true_flags(CLUE_FLAGS)
    return
