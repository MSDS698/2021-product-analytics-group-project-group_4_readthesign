import os 
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

# Initialization 
# Create an app instance that handles requests

app = Flask(__name__)
app.secret_key = os.urandom(24)


app.config.from_object(Config)
db = SQLAlchemy(app)
db.create_all()
db.session.commit()


login_manager = LoginManager()
login_manager.init_app(app)

bootstrap = Bootstrap(app)

from app import routes
from app import classes 
