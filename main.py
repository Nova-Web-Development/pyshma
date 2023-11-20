from flask import Flask, render_template, request, redirect, jsonify, g
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

# @app.route('/api/users')
# def get_users():
#     cur = get_db().cursor()
#     cur.execute('''SELECT * FROM users WHERE 1;''')
#     res = cur.fetchall()
#     return jsonify(res)

# @app.route('/api/getinfo', methods=['GET'])
# def is_registered():
#     email = request.args.get('email')
#     values = (email,)
#     cur = get_db().cursor()
#     cur.execute('''SELECT * FROM users WHERE email = ?;''', values)
#     res = cur.fetchall()
#     return jsonify(res)

@app.route('/user_info')
@login_required
def example():
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
    return render_template('user_info.html', isAuth=True, status=statuses[get_status(user_id)], user_name=res[0][1], email=res[0][1], image=get_image(res[0][0]))

def get_status(user_id):
    cur = get_db().cursor()
    cur.execute('''SELECT status FROM statuses WHERE user_id = ?;''', str(user_id))
    res = cur.fetchall()
    return str(res[0][0])

def get_image(user_id):
    cur = get_db().cursor()
    cur.execute('''SELECT image FROM images WHERE user_id = ?;''', str(user_id))
    res = cur.fetchall()
    return str(res[0][0])

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
        return render_template('load_image.html', isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('load_image.html', isAuth=False)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = hashlib.md5(request.form['password1'].encode()).hexdigest()
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
        return render_template('register.html', isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
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
        return render_template('login.html', isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('login.html', isAuth=False)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('index.html', isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
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
        return redirect('/')
    if current_user.is_authenticated:
        return render_template('form.html', isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
    else:
        return render_template('form.html', isAuth=False)

@app.route('/loadimage', methods=['POST', 'GET'])
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
        return render_template('load_image.html', isAuth=True, user_name=userlogin.get_name(), image=get_image(userlogin.get_id()))
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
        return render_template('lk.html', isAuth=True, status=statuses[get_status(userlogin.get_id())], user_name=userlogin.get_name(), email=userlogin.get_email(), image=get_image(userlogin.get_id()))
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
        if current_user.is_authenticated:
            return render_template('apanel.html', isAuth=True, tickets=res, users=res1, user_name=userlogin.get_name(), email=userlogin.get_email(), image=get_image(userlogin.get_id()))
        else:
            return render_template('apanel.html', isAuth=False)

if __name__ == '__main__':
    app.teardown_appcontext(close_db)
    app.secret_key = generateToken()
    app.run(debug=True)


