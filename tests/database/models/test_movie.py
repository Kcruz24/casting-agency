import datetime
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from backend.app import create_app
from backend.database.models.movie import Movie
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestMovie(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.app_context().push()
        self.client = self.app.test_client()

        self.db_username = 'postgres'
        self.db_host = 'localhost:5432'
        self.db_name = 'casting_agency_test'

        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_username,
                                                               db_password,
                                                               self.db_host,
                                                               self.db_name)

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_movie_created(self):
        movie = Movie(title='The Prestige',
                      release_date=datetime.date(2006, 10, 20))
        movie.insert()

        movie_from_db = Movie.query.filter(Movie.title == 'The Prestige')

        self.assertTrue(isinstance(movie, Movie))
        self.assertTrue(movie_from_db)
