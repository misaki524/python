## engine/keybinds.rpy — 汎用キーバインドトグル
##
## 特定のキーで screen の表示/非表示をトグルする仕組みを提供する。
## 使用例:
##   init python:
##       register_screen_toggle("K_TAB", "clue_list", "clue_list_toggle")

init python:

    def register_screen_toggle(key, screen_name, action_name):
        """
        key を押すたびに screen_name の screen を表示/非表示する。
        action_name: config.keymap に登録するアクション名（一意であること）
        """
        config.keymap[action_name] = [key]

        def _toggle(sn=screen_name):
            if renpy.get_screen(sn):
                renpy.hide_screen(sn)
            else:
                renpy.show_screen(sn)
            renpy.restart_interaction()

        config.underlay.append(renpy.Keymap(**{action_name: _toggle}))
