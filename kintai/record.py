from datetime import datetime #現在の日付と時刻を取得をするためのモジュール
import pandas as pd #データの表形式を操作するためのライブラリ。csvファイルの書き込みに使用
import numpy as np #数値計算をサポートするライブラリ
import os #ファイルやディレクトリの操作を行うモジュール。指定したディレクトリがない場合に作成

def record(active,text=""):
    time_now=datetime.now()
    date=time_now.strftime("%Y-%m")
    #該当月のcsvファイルを読み込む
    try:
        #日付の月のファイルを開く
        df=pd.read_csv("datas/"+date+".csv")
    except:
        #なかったら作成する
        df=pd.DataFrame(columns=["ID","Activity","Time stamp","Feed back"])
        #datasファイルがない場合は作成する。ある場合は作成しない
        os.makedirs("dates",exit_ok=True)

    #IDの決定
    if active=="開始":
        #開始の場合は新規IDを割り振る
        id=int(len(df)+1)
    else:
        id=np.nan

    #DataFrmeに追記処理する
    df=df.append({"ID":id
                "Activity":activity,
                "Time stamp":datetime.now(),
                "Feed back":text},
                igonre_index=True)

    #IDの補完処理
    df["ID"]=df["ID"].interpolate("ffill")
    #csvファイルの書き出し
    df.to_csv("datas/"+date+".csv",index=False")
