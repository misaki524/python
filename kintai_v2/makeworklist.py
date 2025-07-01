import pandas as pd
import datetime
import dateutil

def make_work_list(self,sender):

	#月の確認
	month = datetime.datetime.today()
	#前月分を出力したい場合(i=1)のための処理、差をとる
	month = month - dateutil.relativedelta.relativedelta(months=i)
	#整形
	month = month.strftime("%Y-%m")

	#対象ファイルを指定
	try:
		df = pd.read_csv("datas/"+month+".csv")
	except:
		print("ファイルがありませんでした")
		return

	#出力用DataFrame
	result = pd.DataFrame(columns=["day","start","end","feedback"])

	#ファイルの整形
	df["Time stamp"] = pd.to_datetime(df["Time stamp"].str[:16])

	#ユニークなcase_idを抽出
	case_ids = df["ID"].unique()

	#集計
	for case_id in case_ids:
		#取り消しがあったら記録しない
		if "取り消し" in list(df[df["ID"]==case_id]["Activity"]):
			continue

		#TimeStampが汚いので複雑なコードになってます
		result = result.append({
			"day":str(df[df["ID"]==case_id][df["Activity"]=="開始"]["Time stamp"].iloc[-1])[:10],
			"start":str(df[df["ID"]==case_id][df["Activity"]=="開始"]["Time stamp"].iloc[-1])[-8:],
			"end":str(df[df["ID"]==case_id][df["Activity"]=="終了"]["Time stamp"].iloc[-1])[-8:],
			"feedback":str(df[df["ID"]==case_id][df["Activity"]=="終了"]["Feed back"].iloc[-1])}
			,ignore_index=True)

	#差分計算
	result["time(min)"] = (pd.to_datetime(result["end"]) - pd.to_datetime(result["start"])).dt.total_seconds()
	#分表示に
	result["time(min)"] = result["time(min)"]/60
	#曜日計算
	result["date"] = pd.to_datetime(result["day"]).dt.day_name()
	#表示順変更
	result = result.reindex(columns=["day","date","start","end","time(min)","feedback"])

	#出力
	result.to_excel("/Users/user_name.Downloads/{}_出勤簿.xlsx".format(month))
