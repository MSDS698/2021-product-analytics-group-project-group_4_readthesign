from app import *
from config import Config
from flask_sqlalchemy import SQLAlchemy 

def UserFromDB(username):
	user = classes.User.query.filter_by(username=username).first()
	return user

# def test_db_presence():
# 	db = SQLAlchemy()
# 	engine = db.create_engine(Config.SQLALCHEMY_DATABASE_URI, {})
# 	inspect = db.inspect(engine)
# 	assert (inspect.has_Table("user"))

# def test_api_call():
#     """
#     unit test for app.py
#     """
#     assert app is not None
def test_User():

	assert UserFromDB("Efrem").username == "Efrem"

