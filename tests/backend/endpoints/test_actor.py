import json
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.models.actor import Actor
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestActorEndpoints(TestCase):

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

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    # ##################### HOME ROUTE TESTS #####################

    def test_get_home(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['home_route'], True)

    def test_get_home_404_not_found(self):
        res = self.client().get('/home')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # ##################### ACTORS TESTS WITHOUT AUTH #####################

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_actors'])
        self.assertTrue(len(data['actors']))

    def test_get_actors_404_if_not_found(self):
        res = self.client().get('/actor')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_post_actor(self):
        res = self.client().post('/actors', json=self.actor)
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name='testName').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor)
        self.assertTrue(data['created'])
        self.assertTrue(data['new_actor'])

    def test_post_actor_405_if_not_allowed(self):
        res = self.client().post('/actors/3', json=self.actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_patch_actor(self):
        res = self.client().patch('/actors/14', json={'name': 'patch'})
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name='patch').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(actor)
        self.assertTrue(data['actor_before'])
        self.assertTrue(data['modified_actor'])

    def test_patch_actor_404_if_it_does_not_exist(self):
        res = self.client().patch('/actors/133', json={'name': 'asdf'})
        data = json.loads(res.data)

        actor = Actor.query.filter_by(name='asdf').one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(actor, None)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_delete_actor(self):
        res = self.client().delete('/actors/19')
        data = json.loads(res.data)

        deleted_actor = Actor.query.filter_by(id=13).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(deleted_actor, None)
        self.assertTrue(data['deleted_actor_id'])
        self.assertTrue(len(data['deleted_actor']))
        self.assertTrue(data['number_of_actors_before'])
        self.assertTrue(data['number_of_actors_after'])

    def test_delete_actor_404_if_actor_does_not_exist(self):
        res = self.client().delete('/actors/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')
