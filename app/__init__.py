from flask import Flask 
import os 
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialization 
#  create an app instance that handles requests 

app = Flask(__name__)
app.secret_key = os.urandom(24)

# routes.py needs to import "application" variable in __init__.py (Altough it violates PEP8 standards)

app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()
db.session.commit()


login_manager = LoginManager()
login_manager.init_app(app)

from app import routes
from app import classes 

