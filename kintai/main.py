from rumps import * #MacOSのメニューバーアプリケーションを作成するためのライブラリ
from record import * #record.pyの呼び出し
#下記ファイルを一括インポート
#import download: download.py というファイルがある場合、その中の関数やクラスを使う。
#import datetime: 日付や時間を操作するためのPythonの標準ライブラリを使う。
#import makeworklist: makeworklist.py というファイルから、作業リストを作成する機能を使う。
import download,datetime,makeworklist

class RumpsTest(App): #RumpsTesttというクラスを作成してその中に記載
    def __init__(self): #def__int__(self)の中でアプリ全体の設定
        super(RumpsTest,self).__init__("kintai",icon="images/PC.png",title=None,quit_button="kintaiの終了") #super()は親クラス。selfはインタンス(オブジェクト)
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
        ] #menu属性にMenuItem型で項目をリスト形式に記載
        self.menu["開始"].add(MenuItem("開始1"))
        self.menu["開始"].add(MenuItem("開始2"))
        self.menu["kintaiの出力"].add(MenuItem("今月",callback=self.make_work_list)) #kintaiの出力を押出た時、make_work_listをcallbackで呼び出し実行。今月をmenuにadd関数で項目を追加
        self.menu["kintaiの出力"].add(MenuItem("先月",callback=self.make_last_work_list))


    def start(self,sender): #record.pyを呼び出す
        #記録開始
        record("開始","") #開始という文字列を空の文字列を引数として渡す
        global my_timer,count #my_timer,countは引数　#グローバル変数（どこからでもアクセスできる変数)
        count=0 #countを0に初期化
        my_timer= Timer(self.pass_time,1) #Timerクラスを処理１秒間ごとに処理をself.pass_timeに設定
        my_timer.start() #Timerを実際にスタートする
        #メニューの更新
        self.menu["開始"].set_callback(None) #set_callback関数で呼び出し。開始を押しても何も起こらない
        self.menu["終了"].set_callback(self.end) #set_callback関数で呼び出し。終了を押したらself.endメゾットを呼び出す
        self.menu["取り消し"].set_callback(self.cancel) #et_callback関数で呼び出し。取り消しを押したらself.cancelメゾットを呼び出す
        #アイコンが変更する
        self.icon="images/hamster.png"

    def pass_time(self,sender):
        global count
        #カウントを1を進める
        count += 1 #countが0を1ずつ増やす

        #時間の表示形式を変更
        pass_time=datetime.timedelta(seconds=int(cont)+1) #countが10だとtimedeltaが0:00:00に変換。countが75だとtimedeltaが0:01:15に変換

        #経過時間項目の横に時間を表示する
        self.menu["経過時間"].title="経過時間："+str(pass_time) #経過時間を文字列で表示

    def cancel(self,sender):
        if alert("取り消しますか？",ok="はい",cancel="いいえ"): #alert関数でメッセージを表示をする。OK＝TRUE、FALSE＝いいえを返す。TRUEの場合下記を処理
            #取り消しの記録
            record("取り消し","") #取り消しという文字列を空の文字列を引数として渡す
            #タイマーの停止
            my_timer.stop()
            #表示項目の更新
            self.menu["終了"].set_callback(None)#set_callback関数で呼び出し。終了を押しても何も起こらない
            self.menu["開始"].set_callback(self.start) #set_callback関数で呼び出し。開始を押したらself.endメゾットを呼び出す
            self.menu["取り消し"].set_callback(None) #set_callback関数で呼び出し。終了を押しても何も起こらない
            self.menu["経過時間"].title="経過時間" #経過時間に戻して経過時間の表示のリセット
            self.icon="images/hamster.png"

    def end(self,sender): #何かの終了を処理するために呼ばれるメソッド。
        print("終了")
        #Window(): これは、ユーザーにフィードバックを求めるウィンドウを表示する命令
        #message="Feed back?": このメッセージがウィンドウに表示され「Feed back?」と表示
        #dimensions=(300, 200): ウィンドウの大きさを指定（幅300px、高さ200px）。
        #run(): ウィンドウを実行して、ユーザーが入力するまで待機する。
        respose=Window(message="Feed back?",dimensions=(300,200)).run()
        print(respose.text)

    def make_work_list(self,sender):
        #makeworklist クラスの make_work_list メソッドを呼び出し。引数なし
        makeworklist.make_work_list()

    def make_work_list(self,sender):
        #1 という引数を make_work_list メソッドに渡す
        makeworklist.make_work_list(1) #引数ありで実行。2回目のものが上書きされる

if __name__=="__main__": #このファイルが直接実行されたときのみ以下のコードを実行する。他のファイルでインポートされても表示されない
    app=RumpsTest() #作ったクラスでappを作って走らせる
    app.run() #run() のRumpsライブラリのメソッドでappを実行


#補足：
#defは関数を定義するもの
#モジュール = コードをまとめたファイル
#クラス = データと動作をまとめた設計図
#メソッド = クラスの中で定義された関数