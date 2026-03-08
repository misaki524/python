# スタートさせたいとき
# nohup python main.py > output.log 2>&1 &
# 終了させたいとき
# kill [id]


# rumps: Mac用メニューバーアプリ作成ライブラリ
from rumps import App, MenuItem, Timer, Window, alert, notification
import datetime
import makeworklist
from record import record
import download
import subprocess


class RumpsTest(App):
  def __init__(self):
    super().__init__("", icon="./images_start.png")
    # インスタンス変数でタイマーとカウントを管理
    self._timer = None
    self._count = 0
    # 通知タイマー関連
    self._notify_timer = None
    self._notify_interval = 30 * 60  # デフォルト30分（秒）
    self._notify_paused = False
    # メニュー構成
    # サブメニュー親を先に作成
    notify_menu = MenuItem("通知間隔の設定")
    notify_menu.add(MenuItem("30分ごと", callback=self.set_notify_30))
    notify_menu.add(MenuItem("15分ごと", callback=self.set_notify_15))

    export_menu = MenuItem("出勤簿の出力")
    export_menu.add(MenuItem("今月", callback=self.make_work_list))
    export_menu.add(MenuItem("先月", callback=self.make_last_work_list))

    # メニューアイテムへの参照を保持
    self._mi_start = MenuItem("開始", callback=self.start)
    self._mi_end = MenuItem("終了（待機中）")  # 初期状態は非活性
    self._mi_cancel = MenuItem("取り消し")
    self._mi_elapsed = MenuItem("経過時間")

    self.menu = [
      self._mi_start,
      self._mi_end,
      self._mi_cancel,
      self._mi_elapsed,
      None,
      notify_menu,
      MenuItem("通知一時停止", callback=self.pause_notify),
      MenuItem("通知再開", callback=self.resume_notify),
      None,
      export_menu,
      None,
      MenuItem("環境設定"),
      MenuItem("詳細")
    ]
    self.start_notify_timer()

  def start_notify_timer(self):
    if self._notify_timer:
      self._notify_timer.stop()
    self._notify_timer = Timer(self.notify, self._notify_interval)
    if not self._notify_paused:
      self._notify_timer.start()

  # 通知タイマー停止
  def stop_notify_timer(self):
    if self._notify_timer:
      self._notify_timer.stop()
      self._notify_timer = None

  # 通知処理
  def notify(self, sender):
    try:
      notification("リマインダー", "作業中ですか？", f"{self._notify_interval//60}分経過しました。休憩や記録を忘れずに！")
    except RuntimeError:
      # Info.plistがない環境では通知が使えないのでスキップ
      pass

  # 通知間隔設定
  def set_notify_30(self, sender):
    self._notify_interval = 30 * 60
    self.start_notify_timer()
    alert("通知間隔を30分ごとに設定しました。")

  def set_notify_15(self, sender):
    self._notify_interval = 15 * 60
    self.start_notify_timer()
    alert("通知間隔を15分ごとに設定しました。")

  # 通知一時停止
  def pause_notify(self, sender):
    self._notify_paused = True
    self.stop_notify_timer()
    alert("通知を一時停止しました。")

  # 通知再開
  def resume_notify(self, sender):
    self._notify_paused = False
    self.start_notify_timer()
    alert("通知を再開しました。")

  def start(self, sender):
    """
    出勤記録の開始処理。タイマーを起動し、メニュー状態を更新。
    """
    record("開始", "")
    self._count = 0
    self._timer = Timer(self.pass_time, 1)
    self._timer.start()
    self.start_notify_timer()
    self._set_menu_state(recording=True)

  def end(self, sender):
    """
    出勤記録の終了処理。タイマー停止、メニュー状態更新、フィードバック取得。
    """
    if self._timer:
      self._timer.stop()
    self.stop_notify_timer()
    self._set_menu_state(recording=False)

    # チェックボックス風の選択UI（AppleScriptで実現）
    options = ["ITパス", "AWS関連", "code", "codeAI", "まとめ関連", "その他"]
    selected_options = self._show_checkbox_dialog(options)
    
    if selected_options:
      # 「その他」が含まれている場合は自由記入
      if "その他" in selected_options:
        free = Window(
          message="自由にご記入ください",
          title="フィードバック自由記入",
          default_text="",
          dimensions=(400, 300)
        ).run()
        other_text = free.text.strip() if free.text.strip() else "その他(内容未記入)"
        selected_options = [opt for opt in selected_options if opt != "その他"] + [other_text]
      feedback = ", ".join(selected_options)
    else:
      feedback = "未選択"
    record("終了", feedback)

  def pass_time(self, sender):
    """
    経過時間を1秒ごとに更新し、メニューに表示。
    """
    self._count += 1
    elapsed = datetime.timedelta(seconds=self._count)
    self._mi_elapsed.title = f"経過時間 {elapsed}"

  def cancel(self, sender):
    """
    記録の取り消し処理。ユーザー確認後、タイマー停止とメニュー状態リセット。
    """
    if alert("取り消しますか?", ok="はい", cancel="いいえ"):
      record("取り消し", "")
      if self._timer:
        self._timer.stop()
      self._set_menu_state(recording=False)
      self._mi_cancel.set_callback(None)

  def _set_menu_state(self, recording):
    """
    メニューとアイコンの状態を一括更新。recording=True: 記録中, False: 待機中
    """
    if recording:
      self._mi_start.set_callback(None)
      self._mi_start.title = "開始（記録中）"
      self._mi_end.set_callback(self.end)
      self._mi_end.title = "終了"
      self._mi_cancel.set_callback(self.cancel)
      self.icon = None
      self.icon = "./images.png"
    else:
      self._mi_start.set_callback(self.start)
      self._mi_start.title = "開始"
      self._mi_end.set_callback(None)
      self._mi_end.title = "終了（待機中）"
      self._mi_cancel.set_callback(self.cancel)
      self._mi_elapsed.title = "経過時間"
      self.icon = None
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

  def _show_checkbox_dialog(self, options):
    """
    AppleScriptでチェックボックス付きダイアログを表示し、選択された項目のリストを返す。
    """
    # choose from list で複数選択可能なダイアログを表示
    items_str = ", ".join(f'"{opt}"' for opt in options)
    script = f'''
    set chosenItems to choose from list {{{items_str}}} with title "フィードバック選択" with prompt "フィードバック内容を選択してください（複数選択可）:" with multiple selections allowed
    if chosenItems is false then
      return ""
    else
      set AppleScript's text item delimiters to ","
      return chosenItems as text
    end if
    '''
    try:
      result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True, text=True, timeout=120
      )
      if result.returncode == 0 and result.stdout.strip():
        return [item.strip() for item in result.stdout.strip().split(",")]
    except Exception:
      pass
    return []

if __name__ == "__main__":
    app = RumpsTest()
    app.run()