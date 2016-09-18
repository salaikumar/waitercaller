from flask import Flask
from flask import request
from flask import render_template
# Login Extension
from flask_login import LoginManager
from flask_login import login_required

from flask_login import login_user
from flask_login import logout_user
from mockdbhelper import MockDBHelper as DBHelper
from user import User

from flask import redirect
from flask import url_for

#  Password Helper imports
from passwordhelper import PasswordHelper

#  DB Helper instance
DB = DBHelper()

# Password Helper instance
PH = PasswordHelper()

#  Creating a  Flask App instance
app = Flask(__name__)
#  Set a secret key for you application
app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM'

login_manager = LoginManager(app)
@app.route("/")
def  home():
     return render_template("home.html")

@app.route("/account")
@login_required
def account():
    return "You're logged in"

@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password, stored_user['salt'], stored_user['hashed']):
        user = User(email)
        login_user(user, remember=True)
        return redirect(url_for('account'))
    # user_password = DB.get_user(email)
    # if user_password and user_password == password:
    #     user = User(email)
    #     login_user(user)
    #     return redirect(url_for('account'))
        # return account()
    return home()

# Register function
@app.route("/register" , methods=["POST"])
def register():
    email = request.form.get("email")
    password = request.form.get("password")
    confirmpass = request.form.get("password2")
    if not password == confirmpass:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed  = PH.get_hash(password + salt)
    DB.add_user(email, salt, hashed)
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
