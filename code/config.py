import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.urandom(24)
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'asl.db')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:readthesign@msds603-group-4-readthesign.caomeghbqkwn.us-west-2.rds.amazonaws.com/postgres' 
    SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key


