import sqlite3
from datetime import datetime

# データベースに接続
conn = sqlite3.connect("instance/app.db")
cursor = conn.cursor()

# タイムスタンプがNULLの投稿に現在時刻を設定
now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute("UPDATE post SET timestamp = ? WHERE timestamp IS NULL", (now,))

# 変更を保存
conn.commit()

# 結果を確認
cursor.execute("SELECT id, content, timestamp FROM post")
rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Content: {row[1]}, Timestamp: {row[2]}")

# 接続を閉じる
conn.close()
