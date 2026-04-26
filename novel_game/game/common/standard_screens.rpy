## standard_screens.rpy — Ren'Py 必須スクリーン定義
## ゲーム起動に必要な標準スクリーンを定義する。

# ============================================================
# Say（台詞表示）
# ============================================================

screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        background Solid("#00000099")

        vbox:
            xalign 0.5
            yalign 0.5
            spacing 10

            if who is not None:
                text who id "who" style "say_label" xalign 0.5

            text what id "what" style "say_dialogue"

    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yfill True

style say_label:
    color "#87ceeb"
    size 30
    xalign 0.5
    text_align 0.5

style say_dialogue:
    xalign 0.5
    text_align 0.5
    xsize 900
    color "#e0e0e0"
    size 26

# ============================================================
# Input（テキスト入力）
# ============================================================

screen input(prompt):
    style_prefix "input"

    window:
        vbox:
            xalign gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

# ============================================================
# Choice（選択肢）
# ============================================================

screen choice(items):
    style_prefix "choice"

    add Solid("#00000099")

    vbox:
        for i in items:
            textbutton i.caption action i.action

style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 270
    yanchor 0.5
    spacing 22

style choice_button is default:
    xsize gui.choice_button_width

style choice_button_text is default:
    xalign 0.5

# ============================================================
# クイックメニュー
# ============================================================

screen quick_menu():
    zorder 100

    if quick_menu:
        hbox:
            style_prefix "quick"
            xalign 0.5
            yalign 1.0

            textbutton _("巻き戻し") action Rollback()
            textbutton _("ヒストリー") action ShowMenu('history')
            textbutton _("スキップ") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("オート") action Preference("auto-forward", "toggle")
            textbutton _("設定") action ShowMenu('preferences')

init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button_text:
    size gui.quick_button_text_size

# ============================================================
# Navigation（ナビゲーションメニュー）
# ============================================================

screen navigation():
    vbox:
        style_prefix "navigation"
        xpos gui.navigation_xpos
        yalign 0.5
        spacing 6

        if main_menu:
            textbutton _("スタート") action Start()
        else:
            textbutton _("ヒストリー") action ShowMenu("history")
            textbutton _("セーブ") action ShowMenu("save")

        textbutton _("ロード") action ShowMenu("load")
        textbutton _("設定") action ShowMenu("preferences")

        if _in_replay:
            textbutton _("リプレイ終了") action EndReplay(confirm=True)
        elif not main_menu:
            textbutton _("メインメニュー") action MainMenu()

        textbutton _("バージョン情報") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("終了") action Quit(confirm=not main_menu)

style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"

# ============================================================
# Main Menu（メインメニュー — セーブスロット付き）
# ============================================================

screen main_menu():
    tag menu
    add gui.main_menu_background

    $ _has_saves = any(renpy.can_load(str(_si)) for _si in range(1, 6))

    vbox:
        xalign 0.5
        yalign 0.4
        spacing 15

        text "[config.name!t]":
            size gui.title_text_size
            color gui.accent_color
            xalign 0.5
            bold True

        text "[config.version]":
            size gui.notify_text_size
            color "#555555"
            xalign 0.5

        null height 30

        # セーブデータがある場合、ロードスロットを表示
        if _has_saves:
            frame:
                xalign 0.5
                xsize 500
                ypadding 20
                xpadding 25
                background Frame(Solid("#0a0a0acc"), 5, 5, 5, 5)

                vbox:
                    spacing 8

                    text "— 続きから —" size 20 color "#808080" xalign 0.5

                    null height 5

                    for _si in range(1, 6):
                        $ _slot_exists = renpy.can_load(str(_si))
                        if _slot_exists:
                            button:
                                xfill True
                                ysize 45
                                background Solid("#1a3a1a")
                                hover_background Solid("#3a1010")
                                action Function(renpy.load, str(_si))

                                hbox:
                                    spacing 15
                                    xalign 0.5
                                    yalign 0.5

                                    text "SLOT [_si]" size 20 color "#00ff41"
                                    text _format_save_time(_si) size 16 color "#aaaaaa"

            null height 15

        textbutton _("新規開始"):
            xalign 0.5
            text_size 26
            text_color "#aaaaaa"
            text_hover_color "#cc0000"
            action Start()

        textbutton _("設定"):
            xalign 0.5
            text_size 22
            text_color "#666666"
            text_hover_color "#cc0000"
            action ShowMenu("preferences")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("終了"):
                xalign 0.5
                text_size 22
                text_color "#555555"
                text_hover_color "#cc0000"
                action Quit(confirm=False)

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 280
    yfill True
    background "#0a0a0aCC"

style main_menu_vbox:
    xalign 1.0
    xoffset -20
    xmaximum 800
    yalign 1.0
    yoffset -20

style main_menu_title:
    size gui.title_text_size

style main_menu_version:
    size gui.notify_text_size

# ============================================================
# Game Menu（ゲームメニューフレーム）
# ============================================================

screen game_menu(title, scroll=None, yinitial=0.0):
    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:
            frame:
                style "game_menu_navigation_frame"
            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":
                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude
                elif scroll == "vpgrid":
                    vpgrid:
                        cols 1
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude
                else:
                    transclude

    use navigation

    textbutton _("戻る"):
        style "return_button"
        action Return()

    label title

style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_vscrollbar is gui_vscrollbar
style game_menu_side is gui_side
style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 30
    top_padding 120
    background gui.game_menu_background

style game_menu_navigation_frame:
    xsize 280
    yfill True

style game_menu_content_frame:
    left_margin 40
    right_margin 20
    top_margin 10

style game_menu_label:
    xpos 50
    ysize 120

style game_menu_label_text:
    size 36
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -30

# ============================================================
# About（バージョン情報）
# ============================================================

screen about():
    tag menu
    use game_menu(_("バージョン情報"), scroll="viewport"):
        style_prefix "about"

        vbox:
            label "[config.name!t]"
            text _("バージョン [config.version!t]\n")
            if gui.about:
                text "[gui.about!t]\n"
            text _("Ren'Py {size=15}[renpy.version_only]\n[renpy.license!t]{/size}")

style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text
style about_label_text:
    size gui.label_text_size

# ============================================================
# Save / Load — common/save_screen.rpy に移動済み
# ============================================================

# ============================================================
# Preferences（設定画面）
# ============================================================

screen preferences():
    tag menu
    use game_menu(_("設定"), scroll="viewport"):
        vbox:
            xfill True
            spacing 20

            hbox:
                box_wrap True
                spacing 20

                vbox:
                    style_prefix "radio"
                    label _("表示")
                    textbutton _("ウィンドウ") action Preference("display", "any window")
                    textbutton _("フルスクリーン") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("スキップ")
                    textbutton _("未読テキスト") action Preference("skip", "toggle")
                    textbutton _("選択肢後も継続") action Preference("after choices", "toggle")
                    textbutton _("トランジション") action Preference("skip", "toggle")

            null height 10

            hbox:
                spacing 20

                vbox:
                    style_prefix "slider"
                    label _("テキスト速度")
                    bar value Preference("text speed")
                    label _("オート待機時間")
                    bar value Preference("auto-forward time")

                vbox:
                    style_prefix "slider"
                    label _("音楽")
                    bar value Preference("music volume")
                    label _("効果音")
                    bar value Preference("sfx volume")

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_vbox is pref_vbox

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_vbox:
    spacing 3

style check_vbox:
    spacing 3

style slider_vbox:
    xsize 338

style pref_vbox:
    xsize 225

# ============================================================
# History（ヒストリー）
# ============================================================

screen history():
    tag menu
    use game_menu(_("ヒストリー"), scroll="vpgrid"):
        style_prefix "history"

        for h in _history_list:
            window:
                has fixed:
                    yfit True

                if h.who:
                    label h.who:
                        style "history_name"
                        substitute False
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags) if hasattr(gui, 'history_allow_tags') else h.what
                text what:
                    substitute False

        if not _history_list:
            label _("ヒストリーはありません。")

define config.history_length = 250

style history_window is empty
style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text
style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize 150

style history_name:
    xpos 150
    xanchor 1.0
    ypos 0
    xsize 150

style history_name_text:
    min_width 150
    textalign 1.0

style history_text:
    xpos 170
    ypos 2
    xanchor 0.0
    xsize 740
    min_width 740
    textalign 0.0
    layout "subtitle"

style history_label:
    xfill True

style history_label_text:
    xalign 0.5

# ============================================================
# Confirm（確認ダイアログ）
# ============================================================

screen confirm(message, yes_action, no_action):
    modal True
    zorder 200

    style_prefix "confirm"

    add Solid("#000000CC")

    frame:
        vbox:
            xalign .5
            yalign .5
            spacing 30

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 100

                textbutton _("はい") action yes_action
                textbutton _("いいえ") action no_action

    key "game_menu" action no_action

style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame(Solid("#1a1a1a"), 40, 40, 40, 40)
    padding [40, 40, 40, 40]
    xalign .5
    yalign .5

# ============================================================
# Skip / Notify
# ============================================================

screen skip_indicator():
    zorder 100
    style_prefix "skip"

    frame:
        hbox:
            spacing 6
            text _("スキップ中")
            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"

transform delayed_blink(delay, cycle):
    alpha .5
    pause delay
    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .6)
        repeat

style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame(Solid("#000000AA"), 16, 5, 50, 5)
    padding [16, 5, 50, 5]

style skip_text:
    size gui.notify_text_size

screen notify(message):
    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')

transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0

style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos
    background Frame(Solid("#000000AA"), 16, 5, 40, 5)
    padding [16, 5, 40, 5]

style notify_text:
    size gui.notify_text_size

# ============================================================
# NVL
# ============================================================

screen nvl(dialogue, items=None):
    window:
        style "nvl_window"

        has vbox:
            spacing 15

        use nvl_dialogue(dialogue)

        for i in items or []:
            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0

screen nvl_dialogue(dialogue):
    for d in dialogue:
        window:
            id d.window_id

            fixed:
                yfit True

                if d.who is not None:
                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id

style nvl_window is default
style nvl_entry is default
style nvl_label is say_label
style nvl_dialogue is say_dialogue
style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True
    background "#0a0a0aDD"
    padding [30, 30, 30, 30]
