from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure the MongoDB connection
app.config['MONGO_URI'] = 'mongodb://localhost:27017/login'
mongo = PyMongo(app)

@app.route('/')
def login():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']

        # Check if the email is already registered
        existing_user = mongo.db.T_login.find_one({'email': email})

        if existing_user is None:
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create a new user document
            user_data = {'username': username, 'email': email, 'mobile': mobile, 'password': hashed_password}
            mongo.db.T_login.insert_one(user_data)
            flash('Signup successful!', 'success')
            return redirect(url_for('questions'))  # Redirect to the "questions" page
        else:
            flash('Email already exists. Please login.', 'danger')
            return redirect(url_for('login'))

@app.route('/questions')
def questions():
    return render_template('questions.html')

if __name__ == '__main__':
    app.run(debug=True)
