from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests
import hashlib
from uuid import uuid4
from random import randint as r


API_IMGBB = '370326a03e29ac5d740481d473e46b20'

app = Flask(__name__)
app.config['MYSQL_USER'] = 'adskayd6_novadev'
app.config['MYSQL_PASSWORD'] = 'h98Jals12djhI91'
app.config['MYSQL_HOST'] = 'adskayd6.beget.tech'
app.config['MYSQL_DB'] = 'adskayd6_novadev'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL(app)


def generateToken(length=20) -> str:
    lettersLow = 'abcdefghigklmnopqrstuvwxyz'
    lettersHigh = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    nums = '1234567890'
    string = ""
    for i in range(length):
        a = r(1, 3) == 1
        if a == 1:
            string += lettersLow[r(0, len(lettersLow) - 1)]
        elif a == 2:
            string += lettersHigh[r(0, len(lettersHigh) - 1)]
        else:
            string += nums[r(0, len(nums) - 1)]
    return string


@app.route('/api/getusers')
def get_users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users WHERE 1;''')
    res = cur.fetchall()
    # return render_template('index.html')
    return jsonify(res)


@app.route('/api/getinfo', methods=['GET'])
def isRegistered():
    email = request.args.get('email')
    values = (email)
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users WHERE email == %s;''', values)
    res = cur.fetchall()
    return list(res)


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = hashlib.md5(request.form['password1'].encode()).hexdigest()
        cur = mysql.connection.cursor()
        values = (user_name, email, password)
        cur.execute('''INSERT INTO users (nickname, email, password) VALUES (%s, %s, %s);''', values)
        mysql.connection.commit()
        return redirect('/')
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        values = (email, password)
        res = requests.get('http://localhost:5000/api/getusers').json()[0]
        if res:
            if password == res['password']:
                values = (int(res['id']), generateToken())
                print(values)
                cur.execute('''INSERT INTO tokens (user_id, token) VALUES (%s, %s);''', values)
                mysql.connection.commit()
                return redirect('/')
            else:
                return redirect('/login')

    return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        values = (request.form['user_id'], request.form['company'], request.form['price'])
        cur.execute('''INSERT INTO tickets (user_id, company, price) VALUES (%s, %s, %s);''', values)
        mysql.connection.commit()
        return redirect('/')
    return render_template('form.html')


@app.route('/api/loadimage', methods=['POST', 'GET'])
def load_image():
    if request.method == 'POST':
        image_path = request.files['ticket']
        upload_url = "https://api.imgbb.com/1/upload"
        files = {'image': (image_path.filename, image_path, image_path.mimetype)}
        data = {'key': API_IMGBB}
        response = requests.post(url=upload_url, files=files, data=data)
        response_data = response.json()
        image_url = response_data.get("data", {}).get("url")
        cur = mysql.connection.cursor()
        values = (123, image_url)
        cur.execute('''INSERT INTO tickets_code (user_id, link) VALUES (%s, %s);''', values)
        mysql.connection.commit()
        return redirect('/')
    return render_template('load_image.html')


if __name__ == '__main__':
    app.run(debug=True)
