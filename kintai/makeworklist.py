import pandas as pd
import datetime
import dateutil

def make_work_list(i=0):
    #月の確認
    month=datetime.datetime.today()
    #前月分を出力したい場合(i=1)のための処理、差を取る
    month=month-dateutil.relativedlta.relativedlta(months=i)
    #整形
    month=month.strftime("%Y-%m")

    #対象ファイルを指定
    try:
        df=pd.read_csv("datas/"+month+".csv")
    except:
        print("ファイルがありませんでした")
        return

    #出力用DataFrame
    result=pd.DataFrame(columns=["day","start","end","feedback"])

    #ファイルの整形
    df["Time stamp"]=pd.to_datetime(df["Time stamp"].str[:16])

    #ユニークなcase_idを抽出
    case_ids=df["ID"].unique()

    #集計