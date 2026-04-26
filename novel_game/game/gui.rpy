## gui.rpy — ダークテーマGUI設定

init -2:

    # ============================================================
    # カラーパレット
    # ============================================================

    ## 基本色
    define gui.accent_color = '#8b0000'
    define gui.idle_color = '#aaaaaa'
    define gui.idle_small_color = '#888888'
    define gui.hover_color = '#cc0000'
    define gui.selected_color = '#e0e0e0'
    define gui.insensitive_color = '#55555580'
    define gui.muted_color = '#3a1010'
    define gui.hover_muted_color = '#5a2020'

    define gui.text_color = '#e0e0e0'
    define gui.interface_text_color = '#e0e0e0'

    ## テキストウィンドウ背景
    define gui.textbox_height = 240
    define gui.name_xpos = 240
    define gui.name_ypos = 0
    define gui.namebox_width = None
    define gui.namebox_height = None

    define gui.dialogue_xpos = 268
    define gui.dialogue_ypos = 50
    define gui.dialogue_width = 744
    define gui.dialogue_text_xalign = 0.0

    # ============================================================
    # フォント設定
    # ============================================================

    define gui.text_font = "SourceHanSansLite.ttf"
    define gui.name_text_font = "SourceHanSansLite.ttf"
    define gui.interface_text_font = "SourceHanSansLite.ttf"

    define gui.text_size = 24
    define gui.name_text_size = 28
    define gui.interface_text_size = 24
    define gui.label_text_size = 30
    define gui.notify_text_size = 20
    define gui.title_text_size = 50

    # ============================================================
    # メインメニュー・ゲームメニュー
    # ============================================================

    define gui.main_menu_background = "#0a0a0a"
    define gui.game_menu_background = "#0a0a0a"

    define gui.button_width = None
    define gui.button_height = None
    define gui.button_borders = Borders(6, 6, 6, 6)
    define gui.button_text_font = gui.interface_text_font
    define gui.button_text_size = gui.interface_text_size
    define gui.button_text_idle_color = gui.idle_color
    define gui.button_text_hover_color = gui.hover_color
    define gui.button_text_selected_color = gui.selected_color
    define gui.button_text_insensitive_color = gui.insensitive_color

    ## 選択肢ボタン設定
    define gui.choice_button_width = 700
    define gui.choice_button_height = None
    define gui.choice_button_tile = False
    define gui.choice_button_borders = Borders(50, 12, 50, 12)
    define gui.choice_button_text_font = gui.text_font
    define gui.choice_button_text_size = gui.text_size
    define gui.choice_button_text_xalign = 0.5
    define gui.choice_button_text_idle_color = "#aaaaaa"
    define gui.choice_button_text_hover_color = "#cc0000"
    define gui.choice_button_text_insensitive_color = "#55555580"

    # ============================================================
    # スロット設定
    # ============================================================

    define gui.slot_button_width = 276
    define gui.slot_button_height = 206
    define gui.slot_button_borders = Borders(15, 15, 15, 15)

    define config.thumbnail_width = 246
    define config.thumbnail_height = 138

    define gui.file_slot_cols = 3
    define gui.file_slot_rows = 2

    # ============================================================
    # ウィンドウ配置
    # ============================================================

    define gui.navigation_xpos = 40
    define gui.skip_ypos = 10
    define gui.notify_ypos = 45

    define gui.quick_button_text_size = 18

    define gui.scrollbar_size = 12
    define gui.slider_size = 30

    # ============================================================
    # グローバルフォント設定（defaultスタイルに適用）
    # ============================================================

init -1:
    style default:
        font "SourceHanSansLite.ttf"
