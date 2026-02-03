from datetime import datetime
import pandas as pd
import numpy as np
import os

def format_work_time(td):
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}時間{minutes}分"


def record(activity, text=""):
    time_now = datetime.now()
    date = time_now.strftime("%Y-%m")
    time_str = time_now.strftime("%m-%d %H:%M:%S")
    filepath = f"datas/{date}.csv"

    # datas フォルダがなければ作成
    os.makedirs("datas", exist_ok=True)

    # CSV読み込みまたは新規作成
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
    else:
        df = pd.DataFrame(columns=["ID", "Activity", "Time stamp", "Feed back", "Work Time"])

    # IDの決定
    if activity == "開始":
        id_val = int(len(df) + 1)
    else:
        id_val = np.nan

    # 新しい行をDataFrameとして作成
    new_row = pd.DataFrame([{
        "ID": id_val,
        "Activity": activity,
        "Time stamp": time_str,
        "Feed back": text,
        "Work Time": ""
    }])

    # DataFrameに追加
    df = pd.concat([df, new_row], ignore_index=True)

    # ID補完（前方補完）
    df["ID"] = df["ID"].ffill()
    df = df.infer_objects(copy=False)
    df["ID"] = df["ID"].astype(int)

  # 終了時に差分（勤務時間）を計算して記録
    if activity == "終了":
      last_id = df["ID"].max()
      pair = df[df["ID"] == last_id]
      if len(pair) >= 2:
          start_time_str = pair.iloc[-2]["Time stamp"]
          end_time_str = pair.iloc[-1]["Time stamp"]
          # ここで文字列を datetime に変換（年は現在の年を使う）
          current_year = datetime.now().year
          start_time = datetime.strptime(f"{current_year}-{start_time_str}", "%Y-%m-%d %H:%M:%S")
          end_time = datetime.strptime(f"{current_year}-{end_time_str}", "%Y-%m-%d %H:%M:%S")
          work_time = end_time - start_time
          df.at[df.index[-1], "Work Time"] = format_work_time(work_time)

    # CSVに保存
    df.to_csv(filepath, index=False)
