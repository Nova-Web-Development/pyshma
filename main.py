from flask import Flask, render_template, request, redirect, jsonify, g, url_for
import sqlite3
import requests
import hashlib
from uuid import uuid4
from random import randint as r
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin

API_IMGBB = '370326a03e29ac5d740481d473e46b20'
app = Flask(__name__)

app.config['DATABASE'] = 'database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().fromDB(user_id, get_db())

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
    return db

def close_db(e=None):
    db = getattr(app, '_database', None)
    if db is not None:
        db.close()

def generateToken(length=20) -> str:
    lettersLow = 'abcdefghigklmnopqrstuvwxyz'
    lettersHigh = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nums = '1234567890'
    string = ""
    for i in range(length):
        a = r(1, 3)
        if a == 1:
            string += lettersLow[r(0, len(lettersLow) - 1)]
        elif a == 2:
            string += lettersHigh[r(0, len(lettersHigh) - 1)]
        else:
            string += nums[r(0, len(nums) - 1)]
    return string

@app.route('/api/users')
def get_users():
    cur = get_db().cursor()
    cur.execute('''SELECT * FROM users WHERE 1;''')
    res = cur.fetchall()
    return jsonify(res)

# @app.route('/api/getinfo', methods=['GET'])
# def is_registered():
#     email = request.args.get('email')
#     values = (email,)
#     cur = get_db().cursor()
#     cur.execute('''SELECT * FROM users WHERE email = ?;''', values)
#     res = cur.fetchall()
#     return jsonify(res)

# Корзина
cart = {}

@app.route('/clear')
@login_required
def clear():
    userlogin.clear_checkout()
    global cart
    cart = {}

@app.route('/user_info')
@login_required
def user_info():
    if get_status(userlogin.get_id()) == "0":
        return redirect('/lk')

    statuses = {
        "0": "Сотрудник",
        "1": "Администратор",
        "2": "Директор",
        "3": "Разработчик"
    }

    user_id = request.args.get('user_id')
    cur = get_db().cursor()
    cur.execute('''SELECT * FROM users WHERE id = ?''', (user_id))
    res = cur.fetchall()
    return render_template('user_info.html', lvl=get_status(userlogin.get_id()),
                           isAuth=True, status=statuses[get_status(user_id)], user_name=userlogin.get_name(),
                           username=res[0][1], email=res[0][2], image=get_image(userlogin.get_id()),
                           image_user=get_image(res[0][0]))

@app.route('/change_status')
@login_required
def change_status():
    if get_status(userlogin.get_id()) == "0":
        return redirect('/lk')

    user_id = request.args.get('user_id')
    status = request.args.get('status')
    cur = get_db().cursor()
    cur.execute('''UPDATE statuses SET status = ? WHERE user_id = ?;''', (status, user_id))
    get_db().commit()
    return '200'


def get_status(user_id):
    cur = get_db().cursor()
    cur.execute('''SELECT status FROM statuses WHERE user_id = ?;''', str(user_id))
    res = cur.fetchall()
    return str(res[0][0])

def get_statuses():
    cur = get_db().cursor()
    cur.execute('''SELECT * FROM statuses WHERE 1;''')
    res = cur.fetchall()
    return res

def get_image(user_id):
    cur = get_db().cursor()
    cur.execute('''SELECT image FROM images WHERE user_id = ?;''', str(user_id))
    res = cur.fetchall()
    return str(res[0][0])

def get_dishes():
    cur = get_db().cursor()
    cur.execute('''SELECT name, price FROM first WHERE 1;''')
    first = list(cur.fetchall())
    cur.execute('''SELECT name, price FROM second WHERE 1;''')
    second = list(cur.fetchall())
    cur.execute('''SELECT name, price FROM salads WHERE 1;''')
    salads = list(cur.fetchall())
    cur.execute('''SELECT name, price FROM drinks WHERE 1;''')
    drinks = list(cur.fetchall())
    cur.execute('''SELECT name, price FROM garnirs WHERE 1;''')
    garnirs = list(cur.fetchall())

    return first, second, salads, drinks, garnirs

def get_first(id):
    cur = get_db().cursor()
    cur.execute('''SELECT name, price FROM first WHERE id = ?;''', str(id+1))
    res = cur.fetchall()
    return list(res)[0][0], list(res)[0][1]

def get_second(id):
    cur = get_db().cursor()
    cur.execute('''SELECT name, price FROM second WHERE id = ?;''', str(id+1))
    res = cur.fetchall()
    return list(res)[0][0], list(res)[0][1]

def get_salad(id):
    cur = get_db().cursor()
    cur.execute('''SELECT name, price FROM salads WHERE id = ?;''', str(id+1))
    res = cur.fetchall()
    return list(res)[0][0], list(res)[0][1]

def get_drink(id):
    cur = get_db().cursor()
    cur.execute('''SELECT name, price FROM drinks WHERE id = ?;''', str(id+1))
    res = cur.fetchall()
    return list(res)[0][0], list(res)[0][1]

def get_garnir(id):
    cur = get_db().cursor()
    cur.execute('''SELECT name, price FROM garnirs WHERE id = ?;''', str(id+1))
    res = cur.fetchall()
    return list(res)[0][0], list(res)[0][1]

def get_orders():
    cur = get_db().cursor()
    cur.execute('''SELECT * FROM orders WHERE isDone = 0;''')
    return cur.fetchall()

def get_finished():
    cur = get_db().cursor()
    cur.execute('''SELECT * FROM orders WHERE isGet = 0;''')
    return cur.fetchall()

@app.route('/add_order')
@login_required
def add_order():
    user_id=userlogin.get_id()
    first_id = request.args.get('first')
    second_id = request.args.get('second')
    salad_id = request.args.get('salad')
    drink_id = request.args.get('drink')
    garnir_id = request.args.get('garnir')

    # return get_first(int(first_id))

    first, price1 = get_first(int(first_id))
    second, price2 = get_second(int(second_id))
    salad, price3 = get_salad(int(salad_id))
    drink, price4 = get_drink(int(drink_id))
    garnir, price5 = get_garnir(int(garnir_id))

    total_price = sum([price1, price2, price3, price4, price5])

    # cur = get_db().cursor()
    values = (user_id, first, second, garnir, salad, drink, total_price)
    # cur.execute('''INSERT INTO orders (user_id, first, second, garnir, salad, drink, total_price) VALUES (?, ?, ?, ?, ?, ?, ?);''', values)
    # get_db().commit()
    userlogin.add_to_basket(first=first, second=second, salad=salad, garnir=garnir, drink=drink)

@app.route('/test')
@login_required
def test():
    return userlogin.get_products()

@app.route('/change_image', methods=['POST', 'GET'])
@login_required
def change_image():
    if request.method == 'POST':
        image_path = request.files['ticket']
        upload_url = "https://api.imgbb.com/1/upload"
        files = {'image': (image_path.filename, image_path, image_path.mimetype)}
        data = {'key': API_IMGBB}
        response = requests.post(url=upload_url, files=files, data=data)
        response_data = response.json()
        image_url = response_data.get("data", {}).get("url")
        cur = get_db().cursor()
        values = (image_url, userlogin.get_id())
        cur.execute('''UPDATE images SET image = ? WHERE user_id = ?;''', values)
        get_db().commit()
        return redirect('/')
    if current_user.is_authenticated:
        return render_template('load_image.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('load_image.html', isAuth=False)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        cur = get_db().cursor()
        cur.execute('''SELECT * FROM users WHERE 1''')
        res = cur.fetchall()
        if len(res) > 0:
            last_id = str(res[-1][0]+1)
        else:
            last_id = "1"
        values = (last_id, user_name, email, password)
        cur.execute('''INSERT INTO users (id, nickname, email, password) VALUES (?, ?, ?, ?);''', values)
        cur.execute('''INSERT INTO statuses (user_id, status) VALUES (?, ?);''', (last_id, 0))
        cur.execute('''INSERT INTO images (user_id, image) VALUES (?, ?);''', (last_id, 'https://gamedev.ru/files/images/ieju7eh0-vu.jpg'))
        get_db().commit()
        return redirect('/login')
    if current_user.is_authenticated:
        return render_template('register.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('register.html', isAuth=False)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        cur = get_db().cursor()
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        values = (email,)
        cur.execute('''SELECT * FROM users WHERE email = ?;''', values)
        res = cur.fetchall()
        if res:
            if password == res[0][3]:
                user = {
                    'user_id': res[0][0],
                    'user_name': res[0][1],
                    'email': res[0][2],
                    'password': res[0][3],
                    'status': get_status(res[0][0]),
                    'image': get_image(res[0][0])
                }
                global userlogin
                userlogin = UserLogin().create(user)
                login_user(userlogin)
                get_db().commit()
                return redirect('/lk')
            else:
                return redirect('/login')
    if current_user.is_authenticated:
        return render_template('login.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('login.html', isAuth=False)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('index.html', isAuth=False)

@app.route('/form', methods=['POST', 'GET'])
@login_required
def form():
    if request.method == 'POST':
        cur = get_db().cursor()
        values = (str(userlogin.get_id()), request.form['company'], request.form['price'])
        cur.execute('''INSERT INTO tickets (user_id, company, price) VALUES (?, ?, ?);''', values)
        get_db().commit()
        return redirect('/lk')
    if current_user.is_authenticated:
        return render_template('form.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('form.html', isAuth=False)

@app.route('/done')
@login_required
def done():
    id = request.args.get('id')
    dish = request.args.get('dish')

    cur = get_db().cursor()
    cur.execute('''UPDATE orders SET isDone = 1 WHERE id = ? AND dishes = ?;''', (id, dish))
    get_db().commit()

@app.route('/finished')
@login_required
def finished():
    id = request.args.get('id')
    dish = request.args.get('dish')

    cur = get_db().cursor()
    cur.execute('''UPDATE orders SET isGet = 1 WHERE id = ? AND dishes = ?;''', (id, dish))
    get_db().commit()

def get_products_from_db():
    cur = get_db().cursor()
    cur.execute('''SELECT id, name, price FROM products;''')
    res = cur.fetchall()
    return res

# products = {
#     1: {'name': 'Бизнес ланч', 'price': 100},
#     2: {'name': 'Борщ', 'price': 200},
#     3: {'name': 'Хурма', 'price': 300}
# }



@app.route('/create_order')
@login_required
def creating_an_order():
    products = {}
    for i in get_products_from_db():
        products[i[0]] = {'name': i[1], 'price': i[2]}
    
    return render_template('basket.html', products=products)

@app.route('/add')
@login_required
def add():
    userlogin.add_to_checkout(request.args.get('dish'))


@app.route('/add_to_cart', methods=['POST'])
@login_required
def add_to_cart():
    products = {}
    for i in get_products_from_db():
        products[i[0]] = {'name': i[1], 'price': i[2]}

    product_id = int(request.form['product_id'])
    if product_id == 1:
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        return redirect('/business_lanch')
    if product_id in products:
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
    return redirect(url_for('creating_an_order'))

@app.route('/wait')
@login_required
def wait():
    return render_template('wait.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()), id=userlogin.get_id())

@app.route('/addict', methods=['POST', 'GET'])
@login_required
def create_pred_order():
    products = {}
    for i in get_products_from_db():
        products[i[0]] = {'name': i[1], 'price': i[2]}
    
    total_price = 0
    cart_items = []
    for product_id, quantity in cart.items():
        product = products[product_id]
        total_price += product['price'] * quantity
        cart_items.append({'name': product['name'], 'quantity': quantity, 'price': product['price']})
    if request.method == 'POST':
        # if not (userlogin.get_checkout() == [] and userlogin.get_products() == []):
        products = ', '.join(userlogin.get_checkout() + userlogin.get_products())

        cur = get_db().cursor()
        cur.execute('''INSERT INTO orders (id, dishes, total_price, isDone, isGet) VALUES (?, ?, ?, 0, 0);''', (userlogin.get_id(), products, total_price))
        get_db().commit()
        return redirect('/wait')
        
        # else:
        #     return redirect('/addict')

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/business_lanch', methods=['POST', 'GET'])
@login_required
def create_pred_order1():
    first, second, salads, drinks, garnirs = get_dishes()
    return render_template('create_pred_order.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()),
                               first=first, second=second, salads=salads, drinks=drinks, garnirs=garnirs, id=userlogin.get_id())

@app.route('/load_image', methods=['POST', 'GET'])
@login_required
def load_image():
    if request.method == 'POST':
        image_path = request.files['ticket']
        upload_url = "https://api.imgbb.com/1/upload"
        files = {'image': (image_path.filename, image_path, image_path.mimetype)}
        data = {'key': API_IMGBB}
        response = requests.post(url=upload_url, files=files, data=data)
        response_data = response.json()
        image_url = response_data.get("data", {}).get("url")
        cur = get_db().cursor()
        values = (userlogin.get_id(), image_url)
        cur.execute('''INSERT INTO tickets_code (user_id, link) VALUES (?, ?);''', values)
        get_db().commit()
        return redirect('/')
    if current_user.is_authenticated:
        return render_template('load_image.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('load_image.html', isAuth=False)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/lk')
@login_required
def lk():
    statuses = {
        "0": "Сотрудник",
        "1": "Администратор",
        "2": "Директор",
        "3": "Разработчик"
    }

    if current_user.is_authenticated:
        return render_template('lk.html', lvl=get_status(userlogin.get_id()),
                               isAuth=True, status=statuses[get_status(userlogin.get_id())],
                               user_name=userlogin.get_name(), email=userlogin.get_email(),
                               image=get_image(userlogin.get_id()))
    else:
        return render_template('lk.html', isAuth=False)

@app.route('/apanel')
@login_required
def apanel():
    if get_status(userlogin.get_id()) == "0":
        return redirect('/lk')
    else:
        cur = get_db().cursor()
        cur.execute('''SELECT * FROM tickets WHERE 1''')
        res = cur.fetchall()
        cur.execute('''SELECT id, nickname, email FROM users WHERE 1''')
        res1 = cur.fetchall()
        cur.execute('''SELECT nickname FROM users WHERE 1''')
        res2 = cur.fetchall()
        nicknames = []
        for i in res2:
            nicknames.append(i[0])

        spends = {}
        for i in res:
            try:
                spends[i[0]] += i[2]
            except:
                spends[i[0]] = i[2]

        if current_user.is_authenticated:
            return render_template(
                'apanel.html', spends=spends, lvls=get_statuses(),
                nicknames=nicknames, lvl = get_status(userlogin.get_id()),
                isAuth=True, tickets=res, users=res1, user_name=userlogin.get_name(),
                email=userlogin.get_email(), image=get_image(userlogin.get_id()), orders = get_orders(), finished=get_finished())
        else:
            return render_template('apanel.html', isAuth=False)

if __name__ == '__main__':
    app.teardown_appcontext(close_db)
    app.secret_key = generateToken()
    app.run(debug=True)


