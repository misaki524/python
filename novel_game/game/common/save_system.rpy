## engine/save_system.rpy — エンディング管理・永続データ管理
##
## エンディング登録の共通処理と、エンディングギャラリー画面を提供する。
## 使用例:
##   call register_ending("ending_dawn")
##
##   screen my_ending_gallery():
##       use ending_gallery(my_endings_data)

# ============================================================
# エンディング登録（共通処理）
# ============================================================
# 各エンディングの末尾で呼び出す。
#   persistent.endings_seen に登録
#   persistent.playthrough_count をインクリメント
#   永続データを保存

label register_ending(ending_key):
    $ persistent.endings_seen.add(ending_key)
    $ persistent.playthrough_count += 1
    $ renpy.save_persistent()
    return

# ============================================================
# エンディングギャラリー（汎用screen）
# ============================================================
# endings_data: list of (表示番号, タイトル, カテゴリ, persistent_key) のタプルリスト
#
# 使用例:
#   python:
#       my_data = [("END 1", "夜明け", "トゥルーエンド", "ending_dawn"), ...]
#   use ending_gallery(my_data)

screen ending_gallery(endings_data):
    vbox:
        spacing 10

        for num, title, category, key in endings_data:
            hbox:
                spacing 20
                if persistent.endings_seen and key in persistent.endings_seen:
                    text "[num]" color "#00ff41" size 22 min_width 80
                    text "[title]" color "#e0e0e0" size 22 min_width 250
                    text "[category]" color "#808080" size 20
                else:
                    text "[num]" color "#555555" size 22 min_width 80
                    text "？？？" color "#555555" size 22 min_width 250
