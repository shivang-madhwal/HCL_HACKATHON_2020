from flask import Flask, render_template, redirect, request, session, jsonify
import sqlite3

app = Flask(__name__,template_folder='templates')

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'], ))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = ?", (userId, ))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)

@app.route("/")
def index():
    loggedIn, firstName, noOfItems = getLoginDetails()
    if request.method == 'GET':
        return render_template('index.html')
        

@app.route("/catalog", methods = ['POST'])
def catalog():
    price = float(request.form['price'])
    return render_template('catalog.html',price = price)

@app.route("/ticket",methods=["POST"])
def ticket():
    price = float(request.form['price'])
    return render_template('ticket.html',price = price)

if __name__ == '__main__':
    app.run(debug = True)