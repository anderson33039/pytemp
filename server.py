from flask import Flask, redirect, session, render_template, request, jsonify
import mysql.connector
import json

PORT = 2025
app = Flask(__name__)
app.secret_key = "my_secret_key"

def dbconnect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="datapy"
    )

@app.route('/')
def root():
    return render_template('index.html') #render_template makes "templates" folder the root

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    conn = dbconnect()
    cursor = conn.cursor()

    cursor.execute('SELECT id, password FROM users WHERE username=%s',(username,))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    #conditional statement if the user is null
    if user is None:
        #sending return with an HTML element
        return '<h1>NO USER FOUND.</h1><br><a href="/">go back</a>'
    
    user_id, passw = user
    #checking password
    if password == passw:
        session['user_id'] = user_id
        session['username'] = username
        return redirect('/dashboard') #directs to dashboard
    else:
        #if password is wrong, will return this statement
        return f'<h1>WRONG PASSWORD!</h1><a href="/">go back</a>{passw}'
    


@app.route('/dashboard') #handles dashboard route
def dashboard():
    return render_template('dashboard/dashboard.html')

@app.route('/datagather')
def datagather():
    with open('data/config.json', 'r') as f:
        g_data = json.load(f)
        return jsonify(g_data)

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

if __name__ == '__main__':
    app.run(port=PORT, debug=True)