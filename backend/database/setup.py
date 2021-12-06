import os

from decouple import config
from flask_sqlalchemy import SQLAlchemy

database_username = 'postgres'
database_password = config('PASSWORD')
database_name = 'casting_agency_test'
database_host = 'localhost:5432'

# database_path = "postgresql://{}:{}@{}/{}".format(database_username,
#                                                   database_password,
#                                                   database_host,
#                                                   database_name)

database_path = config('DATABASE_URL')
db = SQLAlchemy()
SECRET_KEY = os.urandom(32)


def setup_db(app, db_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.app = app
    db.init_app(app)
    db.create_all()
