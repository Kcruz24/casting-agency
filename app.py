import os
import sys

from flask import Flask, flash, abort, request, \
    jsonify
from flask_cors import CORS

from backend.database.models.actor import Actor
from backend.database.models.movie import Movie
from backend.database.setup import setup_db


def create_app(test_config=None):
    # create and configure the app
    template_dir = os.path.abspath('frontend/templates')
    app = Flask(__name__, template_folder=template_dir)
    setup_db(app)

    CORS(app, resources={r"*": {"origins": "*"}})

    @app.after_request
    def after_request(res):
        res.headers.add("Access-Control-Allow-Headers",
                        "Content-Type, authorization, true")

        res.headers.add("Access-Control-Allow-Methods",
                        'GET, POST, PATCH, DELETE, OPTIONS')

        return res

    @app.route('/')
    def home():
        return jsonify({
            'success': True,
            'home_route': True
        })

    @app.route('/actors')
    def actors():
        try:
            get_actors = Actor.query.order_by(Actor.id).all()
            format_actors = [actor.format() for actor in get_actors]

            if len(get_actors) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'actors': format_actors,
                'all_actors': len(get_actors)
            })
        except():
            abort(500)

    @app.route('/movies')
    def movies():
        try:
            get_movies = Movie.query.all()
            format_movies = [movie.format() for movie in get_movies]

            if len(get_movies) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': format_movies,
                'all_movies': len(get_movies)
            })
        except():
            abort(500)

    @app.route('/actors/create', methods=['GET', 'POST'])
    def create_actor():

        if request.method == 'GET':
            return jsonify({
                'success': True,
                'request_method': request.method
            })

        error = False

        body = request.get_json()

        get_name = body.get('name', None)
        get_age = body.get('age', None)
        get_gender = body.get('gender', None)

        new_actor = None

        try:
            new_actor = Actor(name=get_name, age=get_age, gender=get_gender)
            new_actor.insert()

            flash(f'{new_actor.name} was successfully created!')
        except():
            error = True
            print(sys.exc_info())
            flash(
                'Something went wrong when trying to create a new actor!')

        if not error:
            return jsonify({
                'success': True,
                'created': new_actor.id,
                'new_actor': new_actor.format()
            })
        else:
            abort(500)

    return app
