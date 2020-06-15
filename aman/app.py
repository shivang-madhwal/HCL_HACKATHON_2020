from flask import Flask, render_template, redirect, request, session, jsonify , url_for
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename
from random import randint
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__,template_folder='templates')
app.secret_key = 'amanyadav'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Machine Learning - Cosine Similarities
ds = pd.read_csv("tickets-new.csv")
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['description'])

cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

results = {}
for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
    similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]

    results[row['id']] = similar_items[1:]
def item(id):
    return ds.loc[ds['id'] == id]['description'].tolist()[0].split(' - ')[0]

def recommend(item_id, num):
    recs = results[item_id][:num]
    result = []
    for rec in recs:
        result.append(item(rec[1])+'.png')
    return result

# generate tickets number
def ticketNum(date):
    year, month, day = date[2:4], date[5:7], date[8:10]
    pre = randint(1000,9999)
    mod = pre%3
    if mod == 0:
        number = str(pre)+month+day
    elif mod == 1:
        number = str(pre)+day+year
    else:
        number = str(pre)+year+month
    return int(number)

# get Login details from database
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

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    con.close()
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
    return render_template('index.html',firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems)

# Ticket List
@app.route("/catalog", methods = ['GET','POST'])
def catalog():
    loggedIn, firstName, noOfItems = getLoginDetails()
    entry = float(request.args.get('entry'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, description, image FROM products')
        itemData = cur.fetchall() 
    itemData = parse(itemData) 
    conn.close()
    return render_template('catalog.html',price = entry,firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems,itemData = itemData)

# Ticket Page
@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    price = request.args.get('entry')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT productId, name, description, image FROM products WHERE productId = ?', (productId, ))
        productData = cur.fetchone()
    conn.close()
    rec = recommend(item_id = int(productId),num = 5)
    return render_template("ticket.html", data=productData,price=price,firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems,suggest = rec)
# use this commented section before line 122 for ticket suggestions
# we are getting something like [[(1, 'PUBG', '101.png')], [], [], [], []] so we will need 3D array
"""     suggest = []
    for tic in rec:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT productId, name, image FROM products WHERE image = ?', (tic, ))
            k = cur.fetchall()
            suggest.append(k)
    conn.close() """

@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        price = float(request.args.get('price'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'], ))
            userId = cur.fetchone()[0]
            cur.execute("SELECT dob FROM users WHERE email = ?", (session['email'], ))
            dob = cur.fetchone()[0]
            ticketNo = ticketNum(dob)
            try:
                cur.execute("INSERT INTO kart (userId, productId, price, ticketNo) VALUES (?, ?, ?, ?)", (userId, productId, price, ticketNo))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('index'))

@app.route("/payment")
def payment():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        email = session['email']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
            userId = cur.fetchone()[0]
            cur.execute("INSERT INTO sales SELECT * FROM kart WHERE userId = ?",(userId,))
            conn.commit()
            cur.execute("DELETE FROM kart WHERE userId = ?",(userId,))
            conn.commit()
        conn.close()
        return render_template('paymentsuccessful.html')

@app.route("/myTickets")
def myTickets():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, sales.price, products.image, sales.ticketNo FROM products, sales WHERE products.productId = sales.productId AND sales.userId = ?", (userId, ))
        items = cur.fetchall()
    conn.close()
    return render_template("mytickets.html", items = items, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)


#cart
@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        cur.execute("SELECT products.productId, products.name, kart.price, products.image, kart.ticketNo FROM products, kart WHERE products.productId = kart.productId AND kart.userId = ?", (userId, ))
        products = cur.fetchall()
    totalPrice = 0
    conn.close()
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

# remove from cart
@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    price = float(request.args.get('price'))
    ticketNo = int(request.args.get('ticketNo'))
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
        userId = cur.fetchone()[0]
        try:
            cur.execute("DELETE FROM kart WHERE userId = ? AND productId = ? AND price = ? AND ticketNo=?", (userId, productId,price,ticketNo))
            conn.commit()
            msg = "removed successfully"
        except:
            conn.rollback()
            msg = "error occured"
    conn.close()
    return redirect(url_for('cart'))

@app.route("/custom")
def customTicket():
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template('customticket.html',loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

# Login
@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

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

@app.route("/firstlogin", methods = ['POST', 'GET'])
def firstlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('choice'))
        else:
            error = 'Invalid Email / Password'
            return render_template('login.html', error=error)

@app.route("/choice",methods = ['POST','GET'])
def choice():
    if request.method == 'GET':
        return render_template("choice.html")
    if request.method == 'POST':
        pre1 = request.form['heroes']
        pre2 = request.form['TV Series']
        pre3 = request.form['Anime']
        pre4 = request.form['Cartoon']
        pre = pre1+','+pre2+','+pre3+','+pre4
        email = session['email']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = ?", (email, ))
            userId = cur.fetchone()[0]
            cur.execute("UPDATE users SET preferences = ? WHERE userId = ?", (pre,userId))
            conn.commit()
        conn.close()
        return  redirect(url_for('index'))
    
    

# registration
@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

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
        return render_template("firstlogin.html", error=msg)

@app.route("/terms")
def terms():
    return render_template('terms.html')
    
@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True)