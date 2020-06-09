import sqlite3

with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.execute('SELECT * FROM sales')
    itemData = cur.fetchall()


for i in itemData:
    print(i)