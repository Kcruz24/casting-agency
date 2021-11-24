import json
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.models.movie import Movie
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestActorEndpoints(TestCase):

    def setUp(self):
        self.app = create_app()
        # self.app.app_context().push()
        self.client = self.app.test_client

        self.db_username = 'postgres'
        self.db_host = 'localhost:5432'
        self.db_name = 'casting_agency_test'

        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_username,
                                                               db_password,
                                                               self.db_host,
                                                               self.db_name)

        self.movie = {
            'title': 'testMovieName',
            'release_date': '2014-03-25'
        }

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_movies'])
        self.assertTrue(len(data['movies']))

    def test_get_movies_404_if_not_found(self):
        res = self.client().get('/movie')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_movie(self):
        res = self.client().post('/movies', json=self.movie)
        data = json.loads(res.data)

        movie = Movie.query.filter_by(title='testMovieName').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie)
        self.assertTrue(data['created_id'])
        self.assertTrue(data['new_movie'])

    def test_post_movie_405_if_not_allowed(self):
        res = self.client().post('/movies/3', json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_patch_movie(self):
        res = self.client().patch('/movies/11', json={'title': 'patchMovie'})
        data = json.loads(res.data)

        movie = Movie.query.filter_by(title='patchMovie').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(movie)
        self.assertTrue(data['old_movie'])
        self.assertTrue(data['modified_movie'])

    def test_patch_movie_404_if_it_does_not_exist(self):
        res = self.client().patch('/movies/133', json={'Title': 'asdf'})
        data = json.loads(res.data)

        movie = Movie.query.filter_by(title='asdf').one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(movie, None)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/11')
        data = json.loads(res.data)

        deleted_movie = Movie.query.filter_by(id=10).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_movie, None)
        self.assertTrue(len(data['deleted_movie']))
        self.assertTrue(data['number_of_movies_before'])
        self.assertTrue(data['number_of_movies_after'])

    def test_delete_movie_404_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')
