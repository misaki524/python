import mysql.connector

# データベース接続
connection = mysql.connector.connect(
    host='127.0.0.1',  # localhost の代わりに 127.0.0.1 を使用
    user='root',  # ユーザー名
    password='animal',  # パスワード
    database='mysql'  # データベース名
)

# 接続確認
if connection.is_connected():
    print("データベースに接続しました")

# 新しいデータベース作成
cursor = connection.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS new_database")  # 新しいデータベース名
print("新しいデータベース 'new_database' を作成しました")

# 作成したデータベースを使用する
cursor.execute("USE new_database")  # 新しく作成したデータベースを選択
print("新しいデータベース 'new_database' を選択しました")

# 必要なテーブルやデータを作成することができます。
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sample_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        age INT
    )
""")
print("サンプルテーブル 'sample_table' を作成しました")

# ここでデータ挿入などの操作を行うことができます。

# 接続を閉じる
cursor.close()
connection.close()
