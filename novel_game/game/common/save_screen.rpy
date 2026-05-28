## common/save_screen.rpy — セーブ・ロード画面（5スロット）
##
## ① 左端にセーブボタン常時表示
## ② ボタン押下 → セーブスロット選択画面
## ③ 既存データありの場合「上書きしますか？」確認
## ④ セーブ完了後 → スタート画面（メインメニュー）へ戻る
## ⑤ スタート画面からセーブデータ選択で続きからプレイ可能

# ============================================================
# 左端セーブボタン（ゲームプレイ中に常時表示）
# ============================================================

screen save_panel():
    if not main_menu:
        zorder 150

        hbox:
            xalign 1.0
            yalign 0.0
            xoffset -15
            yoffset 15
            spacing 8

            frame:
                xpadding 24
                ypadding 14
                background Frame(Solid("#2a5a99cc"), 8, 8, 8, 8)

                textbutton "SAVE":
                    text_size 20
                    text_color "#ffffff"
                    text_hover_color "#cce0ff"
                    text_bold True
                    xalign 0.5
                    action ShowMenu("save")

            frame:
                xpadding 24
                ypadding 14
                background Frame(Solid("#2a6a2acc"), 8, 8, 8, 8)

                textbutton "LOAD":
                    text_size 20
                    text_color "#ffffff"
                    text_hover_color "#ccffcc"
                    text_bold True
                    xalign 0.5
                    action ShowMenu("load")

init python:
    config.overlay_screens.append("save_panel")

    def _format_save_time(slot):
        """セーブスロットの保存時刻を文字列で返す"""
        import datetime
        mtime = renpy.slot_mtime(str(slot))
        if mtime is None:
            return ""
        return datetime.datetime.fromtimestamp(mtime).strftime("%Y/%m/%d %H:%M")

    def _save_and_return_to_title(slot):
        renpy.save(str(slot))
        renpy.music.stop(channel='music', fadeout=0.3)
        renpy.sound.stop()
        renpy.full_restart()

    def _confirm_overwrite_save(slot):
        """既存データがあれば上書き確認、なければ即セーブ"""
        if renpy.can_load(str(slot)):
            renpy.invoke_in_new_context(
                renpy.call_screen, "save_overwrite_confirm", slot=slot
            )
        else:
            _save_and_return_to_title(slot)

# ============================================================
# セーブ画面（5スロット）
# ============================================================

screen save():
    tag menu
    modal True
    zorder 200

    add Solid("#000000dd")

    frame:
        xfill True
        yfill True
        xpadding 80
        ypadding 60
        background Frame(Solid("#0a0a0aee"), 5, 5, 5, 5)

        vbox:
            spacing 16
            xalign 0.5
            yalign 0.5

            text "セーブ" size 36 color "#8b0000" xalign 0.5 bold True
            text "スロットを選択してください" size 18 color "#666666" xalign 0.5

            null height 20

            for i in range(1, 6):
                $ _sv_exists = renpy.can_load(str(i))
                button:
                    xfill True
                    ysize 80
                    background (Solid("#1a3a1a") if _sv_exists else Solid("#1a1a1a"))
                    hover_background Solid("#3a1010")
                    action Function(_confirm_overwrite_save, slot=i)

                    hbox:
                        spacing 30
                        xoffset 40
                        yalign 0.5

                        text "SLOT [i]" size 26 color "#e0e0e0" min_width 120 yalign 0.5

                        if _sv_exists:
                            text _format_save_time(i) size 20 color "#00ff41" yalign 0.5
                        else:
                            text "— 空きスロット —" size 20 color "#555555" yalign 0.5

            null height 20

            textbutton "閉じる":
                xalign 0.5
                text_size 26
                text_color "#aaaaaa"
                text_hover_color "#cc0000"
                action Return()

    key "game_menu" action Return()

# ============================================================
# 上書き確認ダイアログ
# ============================================================

screen save_overwrite_confirm(slot):
    modal True
    zorder 300

    add Solid("#000000dd")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 500
        ypadding 30
        xpadding 40
        background Frame(Solid("#1a1a1aee"), 5, 5, 5, 5)

        vbox:
            spacing 20
            xalign 0.5

            text "上書きしますか？" size 26 color "#e0e0e0" xalign 0.5
            text "SLOT [slot] のセーブデータが上書きされます" size 16 color "#888888" xalign 0.5

            null height 10

            hbox:
                spacing 60
                xalign 0.5

                textbutton "はい":
                    text_size 24
                    text_color "#cc0000"
                    text_hover_color "#ff0000"
                    action Function(_save_and_return_to_title, slot=slot)

                textbutton "いいえ":
                    text_size 24
                    text_color "#aaaaaa"
                    text_hover_color "#e0e0e0"
                    action Return()

# ============================================================
# ロード画面（5スロット — メニュー用）
# ============================================================

screen load():
    tag menu
    modal True
    zorder 200

    add Solid("#000000dd")

    frame:
        xfill True
        yfill True
        xpadding 80
        ypadding 60
        background Frame(Solid("#0a0a0aee"), 5, 5, 5, 5)

        vbox:
            spacing 16
            xalign 0.5
            yalign 0.5

            text "ロード" size 36 color "#8b0000" xalign 0.5 bold True

            null height 20

            for i in range(1, 6):
                $ _ld_exists = renpy.can_load(str(i))
                button:
                    xfill True
                    ysize 80
                    background (Solid("#1a3a1a") if _ld_exists else Solid("#1a1a1a"))
                    hover_background (Solid("#3a1010") if _ld_exists else Solid("#1a1a1a"))
                    action Function(renpy.load, str(i))
                    sensitive _ld_exists

                    hbox:
                        spacing 30
                        xoffset 40
                        yalign 0.5

                        text "SLOT [i]" size 26 color ("#e0e0e0" if _ld_exists else "#555555") min_width 120 yalign 0.5

                        if _ld_exists:
                            text _format_save_time(i) size 20 color "#00ff41" yalign 0.5
                        else:
                            text "— 空きスロット —" size 20 color "#555555" yalign 0.5

            null height 20

            textbutton "閉じる":
                xalign 0.5
                text_size 26
                text_color "#aaaaaa"
                text_hover_color "#cc0000"
                action Return()

    key "game_menu" action Return()
