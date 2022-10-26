from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os


app = Flask("__main__", template_folder=os.getcwd()+'/templates', static_folder=os.getcwd()+"/static")
app.config["DEBUG"] = True
db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run()