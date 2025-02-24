import pandas as pd #データの処理や操作を行うためのライブライリ
import datetime
import dateutil #日付や時刻を簡単に操作するための拡張ライブラリ

def make_work_list(i=0):
    #月の確認
    month=datetime.datetime.today() #今日の日付の(現在)を取得
    #前月分を出力したい場合(i=1)のための処理、差を取る
    month=month-dateutil.relativedelta.relativedelta(months=i) #i(引数)の値に応じて前月(i=1の場合)に日付を調整する。i=0ならその月のデータ
    #整形。「年月」のフォーマットに変換
    month=month.strftime("%Y-%m")

    #対象ファイルを指定
    try:
        df=pd.read_csv("datas/"+month+".csv") #「2025-02」のような年月が格納されているので、この部分で「datas/2025-02.csv」というファイルを読み込む
    except:
        print("ファイルがありませんでした")
        return

    #出力用DataFrame
    result=pd.DataFrame(columns=["day","start","end","feedback"]) #result という新しい空の DataFrame を作成。columnsでday","start","end","feedback"を列で格納

    #df（元のCSVファイルを読み込んだDataFrame）を日付形式に変換
    df["Time stamp"]=pd.to_datetime(df["Time stamp"].str[:16]) #.str[:16] で、「YYYY-MM-DD HH:MM」部分だけを取り出して、pd.to_datetime() を使って日付時刻型（datetime型）に変換

    #ユニークなcase_idを抽出
    case_ids=df["ID"].unique() #.unique() メソッドを使って、重複しないユニークなIDをリストとして取り出します。これにより、各ケースごとに処理を行うことができる

    #集計
    for case_id in case_ids: #繰り返し処理。case_ids が [101, 102, 103] の場合、ループは case_id = 101, case_id = 102, case_id = 103 となり、各ケースごとに処理。
        #取り消しがあったら記憶しない
        if "取り消し" in list(df[df["ID"]==case_id]["Activity"]): #case_id に対応するデータの「Activity」列に「取り消し」が含まれているかチェックしています。「取り消し」があった場合、その case_id のデータはスキップし計算を重複しないようにする
            continue

        result = result.append({
          #[:10] で日付部分（YYYY-MM-DD）のみを取り出し、「day」列に格納します。
          #[-8:] で時刻部分（HH:MM:SS）のみを取り出し、「start」および「end」列に格納します。
          #iloc[行番号, 列番号] で、指定した行番号や列番号にアクセス
          "day": str(df[df["ID"] == case_id][df["Activity"] == "開始"]["Time stamp"].iloc[-1])[:10], #df[df["ID"] == case_id] で、現在の case_id に対応する行（データ）だけを取り出し。
          "start": str(df[df["ID"] == case_id][df["Activity"] == "開始"]["Time stamp"].iloc[-1])[-8:],
          "end": str(df[df["ID"] == case_id][df["Activity"] == "終了"]["Time stamp"].iloc[-1])[-8:],
          "freeback": str(df[df["ID"] == case_id][df["Activity"] == "開始"]["Time stamp"].iloc[-1])}
          ,ignore_index=True) #result に追加。append() を使って新しい行を追加するたびに result が更新

    #差分計算。それぞれ終了時刻と開始時刻を datetime 型に変換total_seconds() を使って、終了時刻と開始時刻の差を「秒」単位で計算し、その後 60 で割って「分」単位に変換。
    result ["time(min)"]=(pd.to_datetime(result["end"]))-pd.to_datetime(result["start"]).dt.total_seconds()
    #勤務時間が「分単位」で計算され、result["time(min)"]に格納
    result["time(min)"]=result["time(min)"]/60
    #曜日計算
    #result["day"] には日付（YYYY-MM-DD)が格納されている。
    #pd.to_datetime(result["day"]) でその日付を datetime 型に変換し、.dt.day_name() を使って曜日（例えば「月曜日」や「火曜日」など）を取得。
    #曜日情報を result["date"] に格納。
    result["date"]=pd.to_datetime(result["day"]).dt.day_name()
    #reindex() を使って、表示する列の順番を変更
    result=result.reindex(columns=["day","date","start","end","time(min)","feedback"])
    #ファイル名は month 変数（例：2025-02）に基づいて「2025-02出勤簿.xlsx」のように作成
    result.to_excel("/Users/kikuchi/python/python/kintai/{}_出勤簿.xlsx".format(month))


#補足：
#９行目の補足
#iは引数として渡された値に基づいて日付を調整。
#i=0だと何もしない(そのまま現在日付)
#i=1だと1ヶ月前の日付に調整
#i=2だと2ヶ月前の日付に調整
#monthからiヶ月引いた日付の計算