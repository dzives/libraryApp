from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime
import bcrypt


app = Flask("__main__", template_folder=os.getcwd()+'/templates', static_folder=os.getcwd()+"/static")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/library"
app.config['secret_key'] = "aohdkjadka`231231jhdakljhdkjahdkj"
app.secret_key = "aohdkjadka`231231jhdakljhdkjahdkj"
app.config['UPLOAD_FOLDER'] = './static/img/'
app.config["DEBUG"] = True
db = SQLAlchemy(app)


# MAX PASSWORD LENGTH = 72
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def check_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), hash.encode())


@app.route("/")
def handle_home():
    return render_template("index.html", user=session.get("user"))


@app.route("/login", methods=["GET", "POST"])
def handle_login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if User.query.filter_by(email=email).first():
            hashed = User.query.filter_by(email=email).first().password
            if check_password(password, hashed):
                session["user"] = User.query.filter_by(email=email).first().username
                return redirect(url_for("handle_home"))
            else:
                flash("Sorry, the password you entered is incorrect.", "error")
                return redirect(url_for("handle_login"))
        else:
            flash("The email you entered is not registered. Please check your email and try again.", "error")
            return redirect(url_for("handle_login"))
    else:
        return render_template("login.html", user=session.get("user"))


@app.route("/logout")
def handle_logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("handle_login"))


@app.route("/register", methods=["GET", "POST"])
def handle_register():
    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = hash_password(request.form["password"])
        firstName = request.form["firstName"]
        lastName = request.form["lastName"]
        phoneNumber = request.form["number"]
        address = request.form["address"]
        psc = request.form["zipcode"]
        city = request.form["city"]
        matchMail = (bool(User.query.filter_by(email=email).all() == []) and len(User.query.filter_by(email=email).all()) <= 1)
        matchUsername = (bool(User.query.filter_by(username=username).all() == []) and len(User.query.filter_by(username=username).all()) <= 1)
        if matchMail and matchUsername:
            db.session.add(User(email=email, username=username, password=password, firstName=firstName,
                                lastName=lastName, phoneNumber=phoneNumber, address=address, psc=psc, city=city))
            db.session.commit()
            session["user"] = username
        elif not matchMail and not matchUsername:
            flash("This email and username is already registered", "error")
            return redirect(url_for("handle_register"))
        elif not matchMail:
            flash("This email is already registered", "error")
            return redirect(url_for("handle_register"))
        elif not matchUsername:
            flash("This username is already registered", "error")
            return redirect(url_for("handle_register"))
        return redirect(url_for("handle_home"))
    else:
        return render_template("register.html")


@app.route("/books")
def handle_books():
    return render_template("books.html", user=session.get("user"))


exec(open("models.py").read())

if __name__ == "__main__":
    app.run()
