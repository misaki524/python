## options.rpy — ゲーム設定

define config.name = _("深夜のコンビニ")
define config.version = "1.0"

define gui.show_name = True
define gui.about = _p("""「深夜のコンビニ」— ホラーノベルゲーム

深夜のコンビニバイト中に起こる異常現象。
午前5時まで生き延びろ。
""")

define build.name = "ShinyaNoConvini"

define config.has_sound = True
define config.has_music = True
define config.has_voice = False

define config.main_menu_music = "audio/bgm/fuon.ogg"

define config.save_directory = "ShinyaNoConvini-1"

define config.window_icon = None

init python:
    config.screen_width = 1280
    config.screen_height = 720

    config.log_enable = True
    config.developer = True

    def _stop_music_on_quit():
        renpy.music.stop(fadeout=0.0)

    config.quit_callbacks.append(_stop_music_on_quit)

    build.classify("**~", None)
    build.classify("**.bak", None)
    build.classify("**/.**", None)
    build.classify("**/#**", None)
    build.classify("**/thumbs.db", None)
    build.classify("game/**.rpy", None)
    build.classify("game/HiraginoMinchoProN.ttc", None)
    build.classify("**", "archive")
