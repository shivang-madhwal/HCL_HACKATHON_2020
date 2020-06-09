import sqlite3

#Open database
conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE sales
		(userId INTEGER,
		productId INTEGER,
		price REAL,
		ticketNo INTEGER,
		FOREIGN KEY(userId) REFERENCES users(userId),
		FOREIGN KEY(productId) REFERENCES products(productId)
		)''')



conn.close()