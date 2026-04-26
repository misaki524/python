## engine/hud.rpy — 汎用HUD部品
##
## 時計表示やコレクション一覧など、画面上に常時 / トグル表示するUI部品。
## 使用例:
##   show screen generic_clock("current_time", "#00ff41")
##   show screen collection_list(my_items, "【アイテム一覧】")

# ============================================================
# 汎用時計表示（画面右上）
# ============================================================
# time_var: 表示する変数名を文字列で渡す（デフォルト "current_time"）
# time_color: 時刻のテキストカラー
# clock_size: フォントサイズ

# clock_display エイリアス（chapter スクリプトから呼ばれる）
screen clock_display():
    use generic_clock("current_time", "#00ff41", 32)

screen generic_clock(time_var="current_time", time_color="#00ff41", clock_size=32):
    frame:
        xalign 1.0
        yalign 0.0
        xpadding 20
        ypadding 10
        xmargin 10
        ymargin 10
        background Frame(Solid("#00000099"), 5, 5, 5, 5)

        $ _clock_text = getattr(store, time_var, "??:??")
        text "[_clock_text]":
            size clock_size
            color time_color
            font "SourceHanSansLite.ttf"
            bold True

# ============================================================
# 汎用コレクションリスト画面（トグル表示）
# ============================================================
# items: list of dict  [{"label": str, "found": bool, "detail": str (optional)}]
# title: リスト画面のタイトル文字列
# extra_widget: 追加表示するscreen名（オプション）
# dismiss_key: 閉じるキー

screen collection_list(items, title="【コレクション】", screen_name="collection_list", dismiss_key="K_TAB"):
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

            text title size 30 color "#8b0000" xalign 0.5
            null height 10

            for item in items:
                hbox:
                    spacing 10
                    if item.get("found", False):
                        text "✓" color "#00ff41" size 24
                        text item.get("detail", item["label"]) color "#e0e0e0" size 22
                    else:
                        text "？" color "#555555" size 24
                        text "？？？" color "#555555" size 22

            null height 20

            textbutton "閉じる":
                xalign 0.5
                text_size 24
                text_color "#aaaaaa"
                text_hover_color "#cc0000"
                action Hide(screen_name)

    key dismiss_key action Hide(screen_name)
    key "game_menu" action Hide(screen_name)
