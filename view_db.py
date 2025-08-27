import sqlite3

# DB connect
conn = sqlite3.connect("digital_gold.db")
cursor = conn.cursor()

# Table ka data fetch
cursor.execute("SELECT * FROM purchases")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
