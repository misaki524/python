## screens.rpy — ゲーム固有UI（手がかりリスト、エンディングリスト）
## 共通部品は common/ から読み込み。
## - 時計表示: common/hud.rpy (generic_clock, clock_display)
## - ビジュアルエフェクト: common/effects.rpy
## - キーバインドトグル: common/keybinds.rpy
## - エンディングギャラリー: common/save_system.rpy
## - セーブ・ロード: common/save_screen.rpy
## - 標準スクリーン: common/standard_screens.rpy

# ============================================================
# 手がかりリスト画面（Tabキーでトグル表示）
# ============================================================

screen clue_list():
    modal True
    zorder 200

    frame:
        xalign 0.5
        yalign 0.5
        xsize 600
        ysize 500
        xpadding 30
        ypadding 30
        background Frame(Solid("#0a0a0aee"), 5, 5, 5, 5)

        vbox:
            spacing 15

            text "【手がかりリスト】" size 30 color "#8b0000" xalign 0.5

            null height 10

            if found_diary:
                hbox:
                    spacing 10
                    text "✓" color "#00ff41" size 24
                    text "田中の日記（[diary_pages_read]ページ）" color "#e0e0e0" size 22
            else:
                hbox:
                    spacing 10
                    text "？" color "#555555" size 24
                    text "？？？" color "#555555" size 22

            if found_camera:
                hbox:
                    spacing 10
                    text "✓" color "#00ff41" size 24
                    text "防犯カメラの映像" color "#e0e0e0" size 22
            else:
                hbox:
                    spacing 10
                    text "？" color "#555555" size 24
                    text "？？？" color "#555555" size 22

            if found_girl_clue:
                hbox:
                    spacing 10
                    text "✓" color "#00ff41" size 24
                    text "少女の証言" color "#e0e0e0" size 22
            else:
                hbox:
                    spacing 10
                    text "？" color "#555555" size 24
                    text "？？？" color "#555555" size 22

            if persistent.playthrough_count >= 1:
                null height 10
                text "【店長のメモ】" size 26 color "#8b0000" xalign 0.5
                hbox:
                    spacing 10
                    text "発見数:" color "#aaaaaa" size 22
                    text "[store_manager_notes]/3" color "#ffa500" size 22

            null height 20

            textbutton "閉じる":
                xalign 0.5
                text_size 24
                text_color "#aaaaaa"
                text_hover_color "#cc0000"
                action Hide("clue_list")

    key "K_TAB" action Hide("clue_list")
    key "game_menu" action Hide("clue_list")

# Tabキーで手がかりリストを開く（common/keybinds.rpy を利用）
init python:
    register_screen_toggle("K_TAB", "clue_list", "clue_list_toggle")

# 手がかりリストボタン（タッチ端末向け）
screen clue_list_button():
    zorder 998
    if not main_menu and (renpy.variant("touch") or renpy.variant("small")):
        frame:
            xalign 0.0
            yalign 1.0
            xoffset 15
            yoffset -15
            xpadding 20
            ypadding 14
            background Frame(Solid("#3a3a3acc"), 8, 8, 8, 8)

            textbutton "手がかり":
                text_size 20
                text_color "#ffa500"
                text_hover_color "#ffcc00"
                text_bold True
                action ToggleScreen("clue_list")

init python:
    config.overlay_screens.append("clue_list_button")

# ============================================================
# エンディングリスト画面（common/save_system.rpy の ending_gallery を利用）
# ============================================================

define ENDINGS_DATA = [
    ("END 1", "夜明け", "トゥルーエンド", "ending_dawn"),
    ("END 2", "生還者", "グッドエンド", "ending_survivor"),
    ("END 3", "日常への帰還", "ノーマルエンド", "ending_normal"),
    ("END 4", "霧の住人", "バッドエンド", "ending_fog"),
    ("END 5", "入れ替わり", "バッドエンド", "ending_swap"),
    ("END 6", "永遠の夜勤", "バッドエンド", "ending_eternal"),
    ("END 7", "前任者の真実", "隠しエンド", "ending_predecessor"),
    ("END 8", "店長の秘密", "隠しエンド", "ending_manager"),
]

screen ending_list():
    tag menu
    use game_menu(_("エンディングリスト"), scroll="viewport"):

        style_prefix "ending_list"

        use ending_gallery(ENDINGS_DATA)

style ending_list_vbox:
    spacing 10
