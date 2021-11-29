import json
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestExecutiveProducerRoleMoviesEndpoints(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.db_username = 'postgres'
        self.db_host = 'localhost:5432'
        self.db_name = 'casting_agency_test'

        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_username,
                                                               db_password,
                                                               self.db_host,
                                                               self.db_name)

        self.movie = {
            'title': 'Spectre',
            'release_date': '2021-11-07',
        }

        self.executive_producer_token = config('EXECUTIVE_PRODUCER_TOKEN')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_can_view_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.executive_producer_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_movies_not_found(self):
        res = self.client().get('/movie',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.executive_producer_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_can_create_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.executive_producer_token)
                                 }, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_movie'])
        self.assertTrue(data['created_id'])

    def test_405_cannot_create_movie(self):
        res = self.client().post('/movies/3',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.executive_producer_token)
                                 }, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_can_modify_movies(self):
        title_replacement = 'Up'
        res = self.client().patch('/movies/6',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.executive_producer_token)
                                  }, json={'title': title_replacement})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['old_movie'])
        self.assertTrue(data['modified_movie'])

    def test_404_cannot_modify_movie_that_doesnt_exist(self):
        res = self.client().patch('/movies/600',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.executive_producer_token)
                                  }, json={'titlee': 'test mod'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_movie(self):
        res = self.client().delete('/movies/6',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.executive_producer_token)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_movie'])
        self.assertTrue(data['number_of_movies_before'])
        self.assertTrue(data['number_of_movies_after'])

    def test_422_cannot_delete_movie(self):
        res = self.client().delete('/movies/600',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.executive_producer_token)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
