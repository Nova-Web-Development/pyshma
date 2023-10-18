from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import requests


API_IMGBB = '370326a03e29ac5d740481d473e46b20'

app = Flask(__name__)
app.config['MYSQL_USER'] = 'adskayd6_novadev'
app.config['MYSQL_PASSWORD'] = 'h98Jals12djhI91'
app.config['MYSQL_HOST'] = 'adskayd6.beget.tech'
app.config['MYSQL_DB'] = 'adskayd6_novadev'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

mysql = MySQL(app)


@app.route('/getusers')
def get_users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM users WHERE 1''')
    res = cur.fetchall()
    # return render_template('index.html')
    return list(res)


@app.route('/register')
def register():
    return 'Register'

@app.route('/login')
def login():
    return 'Login'


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


@app.route('/loadimage', methods=['POST', 'GET'])
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