from flask import Flask, render_template, request, redirect, session, jsonify
from flask_cors import CORS # type: ignore

app = Flask(_name_)
app.secret_key = 'supersecret'
CORS(app)

# In-memory user store
users = {}

# Dummy product list
products = [
    {'id': 1, 'name': 'Banana', 'price': '29', 'image': 'https://i.imgur.com/HsZxKQ8.png'},
    {'id': 2, 'name': 'Carrot', 'price': '38', 'image': 'https://i.imgur.com/7DOIPhb.png'},
    {'id': 3, 'name': 'Coriander', 'price': '138.4', 'image': 'https://i.imgur.com/KWxyZ3e.png'}
]

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users and users[uname] == pwd:
            session['user'] = uname
            return redirect('/')
        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if uname in users:
            return "Username exists. <a href='/signup'>Try another</a>"
        users[uname] = pwd
        return redirect('/login')
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/api/products')
def get_products():
    return jsonify(products)

if _name_ == '_main_':
    app.run(debug=True)
