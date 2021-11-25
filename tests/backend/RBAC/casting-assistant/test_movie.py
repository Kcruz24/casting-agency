import json
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.models.actor import Actor
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestCastingAssistantRoleActorsEndpoints(TestCase):

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
            'title': 'Endgame',
            'release_date': '2024-08-18',
        }

        self.casting_assistant_token = config('CASTING_ASSISTANT_TOKEN')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    # ##################### MOVIES TESTS WITH AUTH #####################

    def test_can_view_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        print('DATA HERE:', data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_movies'])
        self.assertTrue(len(data['movies']))

    def test_401_authorization_not_present_in_headers(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        print('Data:', data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'Authorization not present in headers')
        self.assertEqual(data['description'],
                         'Unable to get authorization from header')

    def test_401_header_malformed(self):
        res = self.client().get('/movies',
                                headers={'Authorization': '{}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        print('DATA HERE', data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'header_malformed')
        self.assertEqual(data['description'], 'Authorization header length '
                                              'not equal to 2')

    def test_401_bearer_keyword_not_found(self):
        res = self.client().get('/movies',
                                headers={'Authorization': 'other {}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        print('DATA HERE', data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'bearer keyword not found')
        self.assertEqual(data['description'], 'The bearer keyword was not '
                                              'found in the authorization '
                                              'header')

    def test_403_cant_create_movie(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.casting_assistant_token)
                                 },
                                 json=self.movie)
        data = json.loads(res.data)

        print('Data', data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'Forbidden')
        self.assertEqual(data['description'], 'Permission not found')

    def test_403_cant_modify_movie(self):
        res = self.client().patch('/movies/6',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.casting_assistant_token)
                                  },
                                  json={'name': 'John'})
        data = json.loads(res.data)

        print('Data', data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'Forbidden')
        self.assertEqual(data['description'], 'Permission not found')

    def test_403_cant_delete_movie(self):
        res = self.client().delete('/movies/6',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.casting_assistant_token)
                                   })
        data = json.loads(res.data)

        print('Data', data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['code'], 'Forbidden')
        self.assertEqual(data['description'], 'Permission not found')
