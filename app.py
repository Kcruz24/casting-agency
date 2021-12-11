from flask import Flask
from flask_cors import CORS

from backend.database.setup import setup_db
from backend.errors.error_handlers import error_handlers
from backend.routes.actors import actors_route
from backend.routes.home import home_route
from backend.routes.movies import movies_route
from backend.setup.after_request import after_requests


def create_app(test_config=None):
    """
    This function creates and configure the app.

    :param test_config: invokes the test config if any.
    :return: The app instance.
    """
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    # AFTER REQUESTS
    app.register_blueprint(after_requests)

    # ENDPOINTS
    app.register_blueprint(home_route)
    app.register_blueprint(actors_route)
    app.register_blueprint(movies_route)

    # ERROR HANDLERS
    app.register_blueprint(error_handlers)

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
