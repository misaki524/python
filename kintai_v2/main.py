# スタートさせたいとき
# nohup python main.py > output.log 2>&1 &
# 終了させたいとき
# kill [id]


# rumps: Mac用メニューバーアプリ作成ライブラリ
from rumps import App, MenuItem, Timer, Window, alert
import datetime
import makeworklist
from rumps import MenuItem
from record import record
import download


class RumpsTest(App):
  def __init__(self):
    super().__init__("shift_recorder", icon="./images_start.png")
    # インスタンス変数でタイマーとカウントを管理
    self._timer = None
    self._count = 0
    # メニュー構成
    self.menu = [
      MenuItem("開始", callback=self.start),
      MenuItem("終了", callback=self.end),
      MenuItem("取り消し"),
      MenuItem("経過時間"),
      None,
      MenuItem("出勤簿の出力"),
      None,
      MenuItem("環境設定"),
      MenuItem("詳細")
    ]
    # サブメニューを先に作る
    work_menu = MenuItem("出勤簿の出力")

    work_menu.add(MenuItem("今月", callback=self.make_work_list))
    work_menu.add(MenuItem("先月", callback=self.make_last_work_list))

    self.menu.add(work_menu)

  def start(self, sender):
    """
    出勤記録の開始処理。タイマーを起動し、メニュー状態を更新。
    """
    record("開始", "")
    self._count = 0
    self._timer = Timer(self.pass_time, 1)
    self._timer.start()
    # メニュー状態更新
    self.menu["開始"].set_callback(None)
    self.menu["終了"].set_callback(self.end)
    self.menu["取り消し"].set_callback(self.cancel)
    self.menu["経過時間"].title = "経過時間"
    # アイコン変更
    self.icon = "./images_start.png"

  def end(self, sender):
    """
    出勤記録の終了処理。タイマー停止、メニュー状態更新、フィードバック取得。
    """
    print("終了")
    if self._timer:
      self._timer.stop()
    self.menu["終了"].set_callback(None)
    self.menu["開始"].set_callback(self.start)
    self.menu["取り消し"].set_callback(self.cancel)
    self.menu["経過時間"].title = "経過時間"
    self.icon = "./images.png"
    response = Window(message="フィードバックを入力してください", dimensions=(300, 200)).run()
    record("終了", response.text)

  def pass_time(self, sender):
    """
    経過時間を1秒ごとに更新し、メニューに表示。
    """
    self._count += 1
    elapsed = datetime.timedelta(seconds=self._count)
    self.menu["経過時間"].title = f"経過時間 {elapsed}"

  def cancel(self, sender):
    """
    記録の取り消し処理。ユーザー確認後、タイマー停止とメニュー状態リセット。
    """
    if alert("取り消しますか?", ok="はい", cancel="いいえ"):
      record("取り消し", "")
      if self._timer:
        self._timer.stop()
      self.menu["終了"].set_callback(None)
      self.menu["開始"].set_callback(self.start)
      self.menu["取り消し"].set_callback(None)
      self.menu["経過時間"].title = "経過時間"
      self.icon = "./images_start.png"

  def make_work_list(self, sender):
    """
    今月分の出勤簿を作成
    """
    makeworklist.make_work_list(0)

  def make_last_work_list(self, sender):
    """
    先月分の出勤簿を作成
    """
    makeworklist.make_work_list(1)

if __name__ == "__main__":
    app = RumpsTest()
    app.run()
