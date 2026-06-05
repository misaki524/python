## script.rpy — エントリポイント、キャラクター定義、変数定義

# ============================================================
# 背景画像定義
# ============================================================

image bg_store_front = "images/bg/コンビニの店内.jpg"
image bg_store_front_fog = "images/bg/霧.jpg"
image bg_store_inside = "images/bg/コンビニの店内.jpg"
image bg_store_inside_dark = "images/bg/コンビニの店内暗い.jpg"
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
# CTC（Click-to-Continue）インジケータ
# ============================================================

image ctc_enter:
    Text(" ▼", size=16, color="#666666")
    alpha 0.0
    pause 0.15
    linear 0.35 alpha 1.0
    pause 0.4
    linear 0.35 alpha 0.0
    repeat

# ============================================================
# キャラクター定義
# ============================================================

default player_name = "安藤ユウキ"
define narrator = Character(None, kind=nvl, ctc="ctc_enter", ctc_position="nestled")
define p = Character("[player_name]", color="#87ceeb", kind=nvl, ctc="ctc_enter", ctc_position="nestled")
define suit = Character("スーツの男", color="#808080", kind=nvl, ctc="ctc_enter", ctc_position="nestled")
define misaki = Character("ミサキ", color="#ffffff", kind=nvl, ctc="ctc_enter", ctc_position="nestled")
define hood = Character("???", color="#8b0000", kind=nvl, ctc="ctc_enter", ctc_position="nestled")
define sato = Character("佐藤ケンジ", color="#ffa500", kind=nvl, ctc="ctc_enter", ctc_position="nestled")

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
# タイトル画面（メインメニューの前に表示）
# ============================================================

label splashscreen:
    scene black
    play music "audio/bgm/fuon.ogg" fadein 2.0
    call screen title_screen
    return

# ============================================================
# ゲーム開始
# ============================================================

label start:

    # 名前入力（背景: コンビニ店内暗い）
    nvl clear
    scene bg_store_inside_dark
    $ player_name = renpy.input("名前を入力してください（空欄でデフォルト）", default="安藤ユウキ", length=12)
    $ player_name = player_name.strip()
    if player_name == "":
        $ player_name = "安藤ユウキ"

label name_confirm:

    "「[player_name]」でよろしいですか？"

    menu:
        "はい、この名前で始める":
            jump name_confirmed
        "いいえ、入力し直す":
            $ player_name = renpy.input("名前を入力してください（空欄でデフォルト）", default="安藤ユウキ", length=12)
            $ player_name = player_name.strip()
            if player_name == "":
                $ player_name = "安藤ユウキ"
            jump name_confirm

label name_confirmed:

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
