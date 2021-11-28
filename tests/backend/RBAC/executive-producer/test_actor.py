import json
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.models.actor import Actor
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestExecutiveProducerRoleActorsEndpoints(TestCase):

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
            'name': 'Testing Executive Name',
            'age': 39,
            'gender': 'male'
        }

        self.executive_producer_token = config('EXECUTIVE_PRODUCER_TOKEN')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_can_view_actors(self):
        res = self.client().get('/actors',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.executive_producer_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_actors'])
        self.assertTrue(len(data['actors']))

    def test_404_actors_not_found(self):
        res = self.client().get('/actor',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.executive_producer_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_can_create_actor(self):
        res = self.client().post('/actors',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.executive_producer_token)
                                 }, json=self.actor)
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name=self.actor['name']).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor)
        self.assertTrue(data['created'])
        self.assertTrue(data['new_actor'])

    def test_405_cannot_create_actor(self):
        res = self.client().post('/actors/3',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.executive_producer_token)
                                 }, json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_can_modify_actors(self):
        name_replacement = 'exec producer'
        res = self.client().patch('/actors/30',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.executive_producer_token)
                                  }, json={'name': f'{name_replacement}'})
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name=f'{name_replacement}')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor)
        self.assertTrue(data['actor_before'])
        self.assertTrue(data['modified_actor'])

    def test_404_modify_if_actor_does_not_exist(self):
        res = self.client().patch('/actors/10000',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.executive_producer_token)
                                  }, json={'name': ' director'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_can_delete_actors(self):
        res = self.client().delete('/actors/28',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.executive_producer_token)
                                   })
        data = json.loads(res.data)

        deleted_actor = Actor.query.filter_by(id=27).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_actor, None)
        self.assertTrue(data['deleted_actor_id'])
        self.assertTrue(data['deleted_actor'])
        self.assertTrue(data['number_of_actors_before'])
        self.assertTrue(data['number_of_actors_after'])

    def test_404_delete_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.executive_producer_token)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')
