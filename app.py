from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import datetime


app = Flask("__main__", template_folder=os.getcwd()+'/templates', static_folder=os.getcwd()+"/static")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost:3306/library"
app.config['secret_key'] = "aohdkjadka`231231jhdakljhdkjahdkj"
app.secret_key = "aohdkjadka`231231jhdakljhdkjahdkj"
app.config['UPLOAD_FOLDER'] = './static/img/'
app.config["DEBUG"] = True
db = SQLAlchemy(app)

exec(open("models.py").read())

if __name__ == "__main__":
    app.run()
