import os

from decouple import config
from flask_sqlalchemy import SQLAlchemy

db_uri = config('DATABASE_URL')
if db_uri.startswith('postgres://'):
    db_uri = db_uri.replace('postgres://', 'postgresql://', 1)

db = SQLAlchemy()
SECRET_KEY = os.urandom(32)


def setup_db(app, db_path=db_uri):
    app.config["SQLALCHEMY_DATABASE_URI"] = db_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    db.app = app
    db.init_app(app)
    db.create_all()
