import json
import unittest
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
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

        self.actor = {
            'name': 'testName',
            'age': 77,
            'gender': 'other'
        }

        self.casting_assistant_token = config('CASTING_ASSISTANT_TOKEN')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    # ##################### ACTORS TESTS WITH AUTH #####################

    def test_can_view_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        print('DATA HERE:', data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_actors_not_found(self):
        res = self.client().get('/actor',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_401_authorization_not_present_in_headers(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        print('Data:', data)
        print('Status code test', res.status_code)
        print('Data code', data['message']['code'])
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'],
                         'Authorization not present in headers')
        self.assertEqual(data['message']['description'],
                         'Unable to get authorization from header')

    def test_401_header_malformed(self):
        res = self.client().get('/actors',
                                headers={'Authorization': '{}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        print('DATA HERE', data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'header_malformed')
        self.assertEqual(data['message']['description'],
                         'Authorization header length '
                         'not equal to 2')

    def test_401_bearer_keyword_not_found(self):
        res = self.client().get('/actors',
                                headers={'Authorization': 'other {}'.format(
                                    self.casting_assistant_token)
                                })
        data = json.loads(res.data)

        print('DATA HERE', data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'bearer keyword not found')
        self.assertEqual(data['message']['description'],
                         'The bearer keyword was not '
                         'found in the authorization '
                         'header')

    def test_403_cant_create_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.casting_assistant_token)
                                 },
                                 json=self.actor)
        data = json.loads(res.data)

        print('Data', data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        self.assertEqual(data['message']['description'], 'Permission not found')

    def test_403_cant_modify_actor(self):
        res = self.client().patch('/actors/6',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.casting_assistant_token)
                                  },
                                  json={'name': 'John'})
        data = json.loads(res.data)

        print('Data', data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        self.assertEqual(data['message']['description'], 'Permission not found')

    def test_403_cant_delete_actor(self):
        res = self.client().delete('/actors/6',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.casting_assistant_token)
                                   })
        data = json.loads(res.data)

        print('Data', data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        self.assertEqual(data['message']['description'], 'Permission not found')


if __name__ == '__main__':
    unittest.main()
