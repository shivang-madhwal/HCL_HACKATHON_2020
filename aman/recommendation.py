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

    suggest = []
    for tic in rec:
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute('SELECT productId, name, image FROM products WHERE image = ?', (tic, ))
            k = cur.fetchall()
            suggest.append(k)
    conn.close()
    # we are getting something like [[(1, 'PUBG', '101.png')], [], [], [], []] so we will need 3D array
    return render_template("ticket.html", data=productData,price=price,firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems,suggest = suggest)



# in html

        {% for tic in suggest %}
        {%for i in tic %}
        <div class="lg:w-1/5 md:w-1/2 p-4 w-full" style="width: 17%; height: auto; display: inline-block;">
          <a class="rounded overflow-hidden">
            <a href="/productDescription?productId={{i[0]}}&entry={{price}}">
              <img alt="{{i[2]}} " src={{ url_for('static', filename='uploads/' + i[2]) }} />
            </a>
          </a>
            <h2 " class="text-white title-font text-lg font-medium" style="text-align: center; margin-top: 5px;">{{i[1]}}</h2>
        </div>
      {% endfor %}
      {% endfor %}