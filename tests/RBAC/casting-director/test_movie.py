import json
import unittest
from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.setup import setup_db


class TestCastingDirectorRoleMoviesEndpoints(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.app.app_context().push()

        self.database_path = config('DATABASE_URL')

        self.movie = {
            'title': 'Spectre',
            'release_date': '2021-11-07',
        }

        self.casting_director_token = config('CASTING_DIRECTOR_TOKEN')

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def test_can_view_movies(self):
        res = self.client().get('/movies',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_director_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['all_movies'])
        self.assertTrue(len(data['movies']))

    def test_404_movies_not_found(self):
        res = self.client().get('/movie',
                                headers={'Authorization': 'Bearer {}'.format(
                                    self.casting_director_token)
                                })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_403_cannot_create_movie_permission_not_found(self):
        res = self.client().post('/movies',
                                 headers={'Authorization': 'Bearer {}'.format(
                                     self.casting_director_token)
                                 }, json=self.movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message']['code'], 'Forbidden')
        self.assertTrue(data['message']['description'], 'Permission not found')

    def test_can_modify_movies(self):
        res = self.client().patch('/movies/6',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.casting_director_token)
                                  }, json={'title': 'casting director movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['old_movie'])
        self.assertTrue(data['modified_movie'])

    def test_404_modify_if_movie_does_not_exist(self):
        res = self.client().patch('/movies/10000',
                                  headers={'Authorization': 'Bearer {}'.format(
                                      self.casting_director_token)
                                  }, json={'title': ' director'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    def test_403_cannot_delete_movie_permission_not_found(self):
        res = self.client().delete('/movies/1',
                                   headers={'Authorization': 'Bearer {}'.format(
                                       self.casting_director_token)
                                   })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'Forbidden')
        self.assertEqual(data['message']['description'], 'Permission not found')


if __name__ == '__main__':
    unittest.main()
