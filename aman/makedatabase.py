import sqlite3
con = sqlite3.connect('database.db')
cursor = con.cursor()
sno = 3
title = 'John Wick'
descr = 'brown'
file = '301.png'
count = cursor.execute('INSERT INTO products (productId,name,description,image) VALUES (?,?,?,?)',(sno,title,descr,file))
con.commit()
cursor.close()