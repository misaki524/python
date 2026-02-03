
# 出勤簿作成用モジュール
import pandas as pd
import datetime
import dateutil
import os


def make_work_list(i=0):
	"""
	指定月（i=0:今月, i=1:先月, ...）の出勤簿をExcelで出力する
	"""
	# 月の計算
	month = datetime.datetime.today() - dateutil.relativedelta.relativedelta(months=i)
	month_str = month.strftime("%Y-%m")

	# 対象ファイルのパス
	csv_path = f"datas/{month_str}.csv"
	if not os.path.exists(csv_path):
		print(f"ファイルがありませんでした: {csv_path}")
		return

	# CSV読み込み
	df = pd.read_csv(csv_path)

	# 出力用DataFrame
	result = pd.DataFrame(columns=["day", "start", "end", "feedback"])

	# 日付整形
	df["Time stamp"] = pd.to_datetime(df["Time stamp"].str[:16])

	# ユニークなIDごとに集計
	for case_id in df["ID"].unique():
		# 取り消しがあればスキップ
		if "取り消し" in df[df["ID"] == case_id]["Activity"].values:
			continue
		# 開始・終了・フィードバック取得
		start_row = df[(df["ID"] == case_id) & (df["Activity"] == "開始")]
		end_row = df[(df["ID"] == case_id) & (df["Activity"] == "終了")]
		if start_row.empty or end_row.empty:
			continue
		day = str(start_row["Time stamp"].iloc[-1])[:10]
		start = str(start_row["Time stamp"].iloc[-1])[-8:]
		end = str(end_row["Time stamp"].iloc[-1])[-8:]
		feedback = str(end_row["Feed back"].iloc[-1])
		# appendの代わりにconcat推奨
		result = pd.concat([
			result,
			pd.DataFrame([{"day": day, "start": start, "end": end, "feedback": feedback}])
		], ignore_index=True)

	# 差分計算（分単位）
	result["time(min)"] = (pd.to_datetime(result["end"]) - pd.to_datetime(result["start"])) .dt.total_seconds() / 60
	# 曜日計算
	result["date"] = pd.to_datetime(result["day"]).dt.day_name()
	# 表示順変更
	result = result.reindex(columns=["day", "date", "start", "end", "time(min)", "feedback"])

	# 出力先パス（ユーザー名自動取得）
	downloads_dir = os.path.expanduser("~/Downloads")
	out_path = os.path.join(downloads_dir, f"{month_str}_出勤簿.xlsx")
	result.to_excel(out_path, index=False)
	print(f"出勤簿を出力しました: {out_path}")
