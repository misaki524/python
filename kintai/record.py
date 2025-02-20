from datetime import datetime #現在の日付と時刻を取得をするためのモジュール
import pandas as pd #データの表形式を操作するためのライブラリ。csvファイルの書き込みに使用
import numpy as np #数値計算をサポートするライブラリ
import os #ファイルやディレクトリの操作を行うモジュール。指定したディレクトリがない場合に作成

def record(active,text=""): #record関数は何かした情報をcsvに記録。activity（活動内容）と text（任意のコメント）を受け取る。
    time_now=datetime.now() #datetime.now()で現在の日時を取得
    date=time_now.strftime("%Y-%m") #strftime("%Y-%m")で「年-月」の形式に変換
    try:
        #日付の月のファイルを開く
        df=pd.read_csv("datas/"+date+".csv") #該当月のcsvファイルを読み込む
    except:
        #なかったら作成する
        df=pd.DataFrame(columns=["ID","Activity","Time stamp","Feed back"]) #新しいファイルは「ID」「Activity」「Time stamp」「Feed back」などの列を持つ空の表になる
        os.makedirs("dates",exit_ok=True) #datasファイルがない場合は作成する。ある場合は作成しない。
                                          #os.makedirs(): この関数は指定した名前のフォルダをdataフォルダに作成する。exist_ok=True: もしすでにdatasフォルダが存在していてもエラーを出さずにスルーする


    #IDの決定
    if active=="開始": #activeが開始の場合新しいIDを決定
        #開始の場合は新規IDを割り振る
        id=int(len(df)+1) #IDは現在のデータフレームの行数(len(df)+1)に1を足して決める。行数に1を足すことで、新しいIDを決める
    else:
        id=np.nan #開始以外のactiveの場合、IDはNan(値なし)となる

    #DataFrmeに追記処理する
    df=df.append({"ID":id, #df.appendで新しい行をデータフレームに追加する。ID：先ほど決めたID
                "Activity":activity, #開始や終了
                "Time stamp":datetime.now(), #現在の日付と時刻
                "Feed back":text #ユーザーが入力したテキスト(フィードバック)
                },igonre_index=True)

    #IDの補完処理
    df["ID"]=df["ID"].interpolate("ffill") #interpolate("ffill")(開始以外の活動で)はIDがNaN (値なし)を26行目のIDを使用して埋める
    #csvファイルの書き出し
    df.to_csv("datas/"+date+".csv",index=False) #datas/はdatasフォルダに保存する。15行目が実行されているので自動的に聖遺作される。datasには28行目が入る。index=False は、データフレームの インデックス（行番号） を保存しないようにするオプション

#補足：
#df は pandasのデータフレーム です。データフレームは、行（縦）と列（横）で構成される表のようなもの
#to_csv() は、データフレームを CSV形式で保存 するためのメソッド
