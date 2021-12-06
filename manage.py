from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

import app
from backend.database.setup import db

app = app.create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
