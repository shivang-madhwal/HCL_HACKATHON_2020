import sqlite3

#Open database
conn = sqlite3.connect('database.db')

conn.execute('''CREATE TABLE lottery
		(lotteryID INTEGER,
        entry REAL,
        price REAL
		)''')



conn.close()