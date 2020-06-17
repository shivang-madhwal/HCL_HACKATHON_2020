import sqlite3
con = sqlite3.connect('database.db')
cursor = con.cursor()

title = 'Death Note'
descr = 'The character is L from DEATH NOTE anime'
file = '334.png'
sno = 48
count = cursor.execute('INSERT INTO products (productId,name,description,image) VALUES (?,?,?,?)',(sno,title,descr,file))
con.commit()
cursor.close()