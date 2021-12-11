import json
import unittest
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from backend.app import create_app
from backend.database.setup import setup_db


class TestCastingDirectorRoleActorsEndpoints(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = config('DATABASE_URL')

        self.actor = {
            'name': 'Testing Name actor',
            'age': 31,
            'gender': 'other'
        }

        self.casting_director_token = config('CASTING_DIRECTOR_TOKEN')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_can_view_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_director_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_actors_not_found(self):
        res = self.client().get('/actor',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_director_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_can_create_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.casting_director_token)
                                 }, json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['new_actor'])

    def test_405_cannot_create_actor(self):
        res = self.client().post('/actors/3',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.casting_director_token)
                                 }, json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_can_modify_actors(self):
        res = self.client().patch('/actors/30',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.casting_director_token)
                                  }, json={'name': 'casting director'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_before'])
        self.assertTrue(data['modified_actor'])

    def test_404_modify_if_actor_does_not_exist(self):
        res = self.client().patch('/actors/10000',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.casting_director_token)
                                  }, json={'name': ' director'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_can_delete_actors(self):
        res = self.client().delete('/actors/29',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.casting_director_token)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_actor_id'])
        self.assertTrue(data['deleted_actor'])
        self.assertTrue(data['number_of_actors_before'])
        self.assertTrue(data['number_of_actors_after'])

    def test_404_delete_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.casting_director_token)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')


if __name__ == '__main__':
    unittest.main()
