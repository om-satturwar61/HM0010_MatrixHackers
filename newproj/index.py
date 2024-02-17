from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "MatrixHackers"

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['user_db']
collection = db['users']

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/register', methods=['POST'])
# def register():
#     username = request.form['username']
#     password = request.form['password']
    
#     # Hash the password before storing it
#     hashed_password = generate_password_hash(password)
    
#     # Check if username already exists
#     if collection.find_one({'username': username}):
#         return 'Username already exists'
    
#     # Insert the user data into MongoDB
#     user_data = {'username': username, 'password': hashed_password}
#     collection.insert_one(user_data)
    
#     return redirect(url_for('index'))

@app.route('/login', methods=['POST','GET'])
def login():

    if  request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        
        # Retrieve user data from MongoDB
        user_data = collection.find_one({'user_name': username})
        
        # if user_data and check_password_hash(user_data['password'], password):
        if user_data and password == user_data["password"]:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'
    return render_template("/login.html")

@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return render_template("welcome.html",name=session['username'])

    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
