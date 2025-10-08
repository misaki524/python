# スタートさせたいとき
# nohup python main.py > output.log 2>&1 &
# 終了させたいとき
# kill [id]

from rumps import *
from record import *
import download,datetime,makeworklist

class RumpsTest(App):
    def __init__(self):
      super(RumpsTest, self).__init__("shift_recorder",icon="./images_start.png")
      self.menu=[
          MenuItem("開始",callback=self.start),
          MenuItem("終了",callback=self.end),
          MenuItem("取り消し"),
          MenuItem("経過時間"),
          None,
          MenuItem("出勤簿の出力"),
          None,
          MenuItem("環境設定"),
          MenuItem("詳細")
          ]
      self.menu["出勤簿の出力"].add(MenuItem("今月",callback=self.make_work_list))
      self.menu["出勤簿の出力"].add(MenuItem("先月",callback=self.make_last_work_list))


    def start(self,sender):
      #記録開始
      record("開始","")
      #タイマー起動
      global my_timer,count
      count=0
      my_timer=Timer(self.pass_time,1)
      my_timer.start()
      #メニューの更新
      self.menu["開始"].set_callback(None)
      self.menu["終了"].set_callback(self.end)
      self.menu["取り消し"].set_callback(self.cancel)
      self.menu["経過時間"].title="経過時間"

      #アイコンに色をつける
      self.icon="./images_start.png"

    def end(self,sender):
      print("終了")
      my_timer.stop()

      self.menu["終了"].set_callback(None)
      self.menu["開始"].set_callback(self.start)
      self.menu["取り消し"].set_callback(self.cancel)
      self.menu["経過時間"].title="経過時間"

      self.icon="./images.png"

      response=Window(message="feed back?",dimensions=(300,200)).run()

      record("終了",response.text)

    def pass_time(self,sender):
        global count
        count=count+1
        pass_time=datetime.timedelta(seconds=int(count)+1)
        self.menu["経過時間"].title="経過時間"+str(pass_time)

    def cancel(self,sender):
        if alert("取り消しますか?",ok="はい",cancel="いいえ"):
          record("取り消し","")
          my_timer.stop()
          self.menu["終了"].set_callback(None)
          self.menu["開始"].set_callback(self.start)
          self.menu["取り消し"].set_callback(None)
          self.menu["経過時間"].title="経過時間"
          self.icon="./images_start.png"

    def make_work_list(self,sender):
      makeworklist.make_last_work_list()

    def make_last_work_list(self,sender):
      makeworklist.make_work_list(1)

if __name__=="__main__":
  app = RumpsTest()
  app.run()
