from flask import Flask 
import os 

# Initialization 
#  create an app instance that handles requests 

app = Flask(__name__)
# application.secret_key = os.urandom(24)

# routes.py needs to import "application" variable in __init__.py (Altough it violates PEP8 standards)

from app import routes