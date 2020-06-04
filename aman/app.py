from flask import Flask, render_template, redirect, request, session, jsonify

app = Flask(__name__,template_folder='templates')

@app.route("/")
def index():
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