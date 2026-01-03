import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    user="app",
    password="apppass",
    database="vet_reservation",
)

print("✅ MySQL 接続OK")
conn.close()