from random import randint
import sqlite3

def ticketNum(date):
    month, day = date[5:7] , date[8:10]
    pre = str(randint(1000,9999))
    number = pre+month+day
    return int(number)


with sqlite3.connect('database.db') as conn:
    cur = conn.cursor()
    cur.execute("SELECT userId FROM users WHERE email = ?", ("amansy04@gmail.com", ))
    userId = cur.fetchone()[0]
    cur.execute("SELECT dob FROM users WHERE email = ?", ("amansy04@gmail.com", ))
    dob = cur.fetchone()[0]
    ticketNo = ticketNum(dob)
    print(userId,dob,ticketNo)