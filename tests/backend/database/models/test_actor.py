from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.models.actor import Actor
from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestActor(TestCase):

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

    def test_actor_created(self):
        actor = Actor(name='Kevin', age=22, gender='male')
        actor.insert()

        actor_from_db = Actor.query.filter(Actor.name == 'Kevin').one()

        self.assertTrue(isinstance(actor, Actor))
        self.assertTrue(actor_from_db)
