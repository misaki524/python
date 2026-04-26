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
        zorder 50

        frame:
            xalign 0.0
            yalign 0.5
            xpadding 4
            ypadding 14
            background Frame(Solid("#0a0a0acc"), 3, 3, 3, 3)

            vbox:
                spacing 6

                textbutton "保存":
                    text_size 14
                    text_color "#8b0000"
                    text_hover_color "#cc0000"
                    text_bold True
                    xalign 0.5
                    action ShowMenu("save")

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
        """指定スロットにセーブし、メインメニューに戻る"""
        renpy.save(str(slot))
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

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 520
        xpadding 40
        ypadding 30
        background Frame(Solid("#0a0a0aee"), 5, 5, 5, 5)

        vbox:
            spacing 12

            text "セーブ" size 30 color "#8b0000" xalign 0.5 bold True
            text "スロットを選択してください" size 16 color "#666666" xalign 0.5

            null height 10

            for i in range(1, 6):
                $ _sv_exists = renpy.can_load(str(i))
                button:
                    xfill True
                    ysize 60
                    background (Solid("#1a3a1a") if _sv_exists else Solid("#1a1a1a"))
                    hover_background Solid("#3a1010")
                    action Function(_confirm_overwrite_save, slot=i)

                    hbox:
                        spacing 20
                        xoffset 20
                        yalign 0.5

                        text "SLOT [i]" size 22 color "#e0e0e0" min_width 100 yalign 0.5

                        if _sv_exists:
                            text _format_save_time(i) size 18 color "#00ff41" yalign 0.5
                        else:
                            text "— 空きスロット —" size 18 color "#555555" yalign 0.5

            null height 10

            textbutton "閉じる":
                xalign 0.5
                text_size 22
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

    add Solid("#000000cc")

    frame:
        xalign 0.5
        yalign 0.5
        xsize 700
        ysize 520
        xpadding 40
        ypadding 30
        background Frame(Solid("#0a0a0aee"), 5, 5, 5, 5)

        vbox:
            spacing 12

            text "ロード" size 30 color "#8b0000" xalign 0.5 bold True

            null height 10

            for i in range(1, 6):
                $ _ld_exists = renpy.can_load(str(i))
                button:
                    xfill True
                    ysize 60
                    background (Solid("#1a3a1a") if _ld_exists else Solid("#1a1a1a"))
                    hover_background (Solid("#3a1010") if _ld_exists else Solid("#1a1a1a"))
                    action Function(renpy.load, str(i))
                    sensitive _ld_exists

                    hbox:
                        spacing 20
                        xoffset 20
                        yalign 0.5

                        text "SLOT [i]" size 22 color ("#e0e0e0" if _ld_exists else "#555555") min_width 100 yalign 0.5

                        if _ld_exists:
                            text _format_save_time(i) size 18 color "#00ff41" yalign 0.5
                        else:
                            text "— 空きスロット —" size 18 color "#555555" yalign 0.5

            null height 10

            textbutton "閉じる":
                xalign 0.5
                text_size 22
                text_color "#aaaaaa"
                text_hover_color "#cc0000"
                action Return()

    key "game_menu" action Return()
