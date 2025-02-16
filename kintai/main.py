from rumps import *
from record import *
import download,datetime,makeworklist

class RumpsTest(App):
    def __init__(self):
        super(RumpsTest,self).__init__("kintai",icon="images/PC.png",title=None,quit_button="kintaiの終了")
        self.menu=[
          MenuItem("開始",callback=self.start),
          MenuItem("終了"),
          MenuItem("取り消し"),
          MenuItem("経過時間"),
          None,
          MenuItem("kintaiの出力"),
          None,
          MenuItem("環境設定"),
          MenuItem("詳細")
        ]
        self.menu["開始"].add(MenuItem("開始1"))
        self.menu["開始"].add(MenuItem("開始2"))
        self.menu["kintaiの出力"].add(MenuItem("今月",callback=self.make_work_list))
        self.menu["kintaiの出力"].add(MenuItem("先月",callback=self.make_last_work_list))


    def start(self,sender):
        print("開始")
        self.icon="images/hamster.png"
        global my_timer,count
        count=0
        my_timer= Timer(self.pass_time,1)
        self.menu["開始"].set_callback(None)
        self.menu["開始"].title="仕事中"
        if alert("取り消しますか？",ok="はい",cancel="いいえ"):
            print("開始")
        else:
            print("いいえが押されました")

    def pass_time(self,sender):
        global count
        print(count)
        count += 1


    def end(self,sender):
        print("終了")
        respose=Window(message="Feed back?",dimensions=(300,200)).run()
        print(respose.text)

if __name__=="__main__":
    app=RumpsTest()
    app.run()
