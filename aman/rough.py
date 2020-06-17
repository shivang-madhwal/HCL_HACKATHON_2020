import sqlite3

with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.execute('DELETE FROM sales WHERE userId = 2')
    conn.commit()
conn.close()