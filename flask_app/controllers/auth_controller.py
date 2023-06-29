from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models import user
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/login', methods=['GET'])
def login_form():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login_authenticate():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password", "error")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "error")
        return redirect('/login')
    
    session['user_id'] = user_in_db.id
    return redirect("/dashboard")


@app.route("/register", methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        flash("You have some errors in your registration!!!", "reg_error")
        return redirect("/login")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form["email"],
        "phone_number": request.form['phone_number'],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    
    return redirect("/dashboard")
    

@app.route("/register", methods=["GET"])
def register_form():
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect('/login')

