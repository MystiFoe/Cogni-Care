from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set the secret key for flash messages

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["login"]
collection = db["T_login"]

def is_valid_login(username, password):
    # Check if the username exists in the database
    user = collection.find_one({"email": username})

    if user:
        # Verify the password
        hashed_password = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return True  # Username and password are valid
        else:
            return False  # Password is incorrect
    else:
        return False  # Username does not exist

@app.route("/", methods=["GET", "POST"])
def login():
    login_result = None  # Initialize login result variable
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        if is_valid_login(username, password):
            flash("Login successful!", "success")
            login_result = "Login Successful"
            # You can customize the response and redirection here
            return redirect(url_for("questions"))
        else:
            flash("Invalid login credentials. Please try again.", "danger")
            login_result = "Login Not Successful"

    return render_template("Login.html", login_result=login_result)

@app.route("/questions")
def questions():
    return render_template("questions.html")

if __name__ == "__main__":
    app.run(debug=True)
