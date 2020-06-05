from flask import Flask, render_template, redirect, request, session, jsonify , url_for
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__,template_folder='templates')
app.secret_key = 'amanyadav'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# get Login details from database
def getLoginDetails():
    global loggedIn, firstName, noOfItems
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

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for k in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

# Home page
@app.route("/")
def index():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, description, image FROM products')
        itemData = cur.fetchall() 
    itemData = parse(itemData) 

    return render_template('index.html',firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems,itemData = itemData)

# Ticket List
@app.route("/catalog", methods = ['GET','POST'])
def catalog():
    entry = float(request.args.get('entry'))
    return render_template('catalog.html',price = entry,firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems)

# Ticket Page
@app.route("/ticket",methods=["POST"])
def ticket():
    price = float(request.form['price'])
    return render_template('ticket.html',price = price)

# Login
@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('index'))
        else:
            error = 'Invalid Email / Password'
            return render_template('login.html', error=error)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')


@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName'].title()
        lastName = request.form['lastName'].title()
        dob = request.form['dob']

        with sqlite3.connect('database.db') as con:
            try:
                cur = con.cursor()
                cur.execute('INSERT INTO users (password, email, firstName, lastName, dob) VALUES (?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, dob))

                con.commit()

                msg = "Registered Successfully"
            except:
                con.rollback()
                msg = "Error occured"
        con.close()
        return render_template("login.html", error=msg)

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route("/productDescription")
def productDescription():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, price, description, image, stock FROM products WHERE productId = ?', (productId, ))
        productData = cur.fetchone()
    conn.close()
    return render_template("productDescription.html", data=productData)

if __name__ == '__main__':
    app.run(debug = True)