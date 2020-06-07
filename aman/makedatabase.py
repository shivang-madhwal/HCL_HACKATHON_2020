import sqlite3
con = sqlite3.connect('database.db')
cursor = con.cursor()
sqlite_insert_query = """INSERT INTO products
            (productId,name,description,image)
            VALUES
            (4,'Naruto','Yellow','Ticket042.png')"""


count = cursor.execute(sqlite_insert_query)
con.commit()
cursor.close()