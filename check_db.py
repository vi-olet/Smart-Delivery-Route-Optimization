import sqlite3

conn = sqlite3.connect('delivery.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM routes")
rows = cursor.fetchall()
for row in rows:
    print(row)
conn.close()