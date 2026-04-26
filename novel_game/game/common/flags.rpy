## engine/flags.rpy — フラグ管理ユーティリティ
##
## ゲーム変数の一括初期化とカウント集計を提供する。
## 使用例:
##   $ init_flags(game_flags)
##   $ count = count_true_flags(["found_diary", "found_camera", "found_girl_clue"])

init python:

    def init_flags(flag_dict):
        """
        flag_dict の各キーを store に設定する。
        flag_dict: dict  {"変数名": デフォルト値, ...}
        例: init_flags({"trust_suit": False, "diary_pages_read": 0})
        """
        for name, value in flag_dict.items():
            setattr(store, name, value)

    def count_true_flags(flag_names):
        """
        指定した変数名リストのうち True であるものの数を返す。
        flag_names: list of str
        """
        return sum(1 for name in flag_names if getattr(store, name, False))
