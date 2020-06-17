import sqlite3

with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE productId = 3')
    conn.commit()
conn.close()