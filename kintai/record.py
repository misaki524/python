from datetime import datetime #現在の日付と時刻を取得をするためのモジュール
import pandas as pd #データの表形式を操作するためのライブラリ。csvファイルの書き込みに使用
import numpy as np #数値計算をサポートするライブラリ
import os #ファイルやディレクトリの操作を行うモジュール。指定したディレクトリがない場合に作成

def record(activity,text=""): #record関数は何かした情報をcsvに記録。activity（活動内容）と text（任意のコメント）を受け取る。
    time_now=datetime.now() #datetime.now()で現在の日時を取得
    date=time_now.strftime("%Y-%m") #strftime("%Y-%m")で「年-月」の形式に変換
    filename=f"dates/{date}.csv"
    try:
        #日付の月のファイルを開く
        df=pd.read_csv(filename) #該当月のcsvファイルを読み込む
    except:
        #なかったら作成する
        df=pd.DataFrame(columns=["ID","Activity","Time stamp","Feed back"]) #新しいファイルは「ID」「Activity」「Time stamp」「Feed back」などの列を持つ空の表になる
        #datasファイルがない場合は作成する。ある場合は作成しない。
        #os.makedirs(): この関数は指定した名前のフォルダをdataフォルダに作成する。exist_ok=True: もしすでにdatasフォルダが存在していてもエラーを出さずにスルーする
        os.makedirs("dates",exist_ok=True)

    # IDの決定
    id = len(df) + 1  # 新しいIDは行数 + 1 とする。df の行数（つまり記録の数）を返す。

    new_data = pd.DataFrame([{ #pd.DataFrame() を使って1行のデータを作成。
        "ID": id, #新しいID
        "Activity": activity, #活動内容
        "Time stamp": datetime.now(), #現在の日時
        "Feed back": text #任意で渡されるフィードバック
    }])

    #既存の df に新しいデータ new_data を 結合。df が3行だとした場合、新しい行を追加すると4行目になる
    #ignore_index=True によって、新しい行が追加されるときに インデックス（行番号）をリセット
    df = pd.concat([df, new_data], ignore_index=True)

    #csvファイルの書き出し
    os.makedirs("dates",exist_ok=True) #dates というフォルダが存在しない場合に新しく作成。もし既に存在していれば、エラーを出さずにそのまま進む
    df.to_csv(filename,index=False) #dates/はdatesフォルダに保存する。15行目が実行されているので自動的に聖遺作される。datasには28行目が入る。index=False は、データフレームの インデックス（行番号） を保存しないようにするオプション

    #新しく追加されたデータの ID を返す。
    return id



#補足：
#df は pandasのデータフレーム です。データフレームは、行（縦）と列（横）で構成される表のようなもの
#to_csv() は、データフレームを CSV形式で保存 するためのメソッド
