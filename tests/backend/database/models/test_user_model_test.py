from unittest import TestCase

from decouple import config
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from backend.database.models.user_model_test import UserModelTest

from backend.database.setup import setup_db

db_password = config('PASSWORD')


class TestUserModelTest(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.app_context().push()

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
            print('metadata from test: ', self.db.metadata.tables)

    def test_model_test_bench_created(self):
        testModel = UserModelTest()
        testModel.insert()

        find_test_model = UserModelTest.query.filter_by(
            name='Test').one_or_none()

        self.assertTrue(find_test_model)
