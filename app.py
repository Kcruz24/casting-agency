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
    def get_actors():
        try:
            all_actors = Actor.query.order_by(Actor.id).all()
            format_actors = [actor.format() for actor in all_actors]

            if len(all_actors) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'actors': format_actors,
                'all_actors': len(all_actors)
            })
        except():
            abort(500)

    @app.route('/actors', methods=['POST'])
    def post_actors():

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

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def patch_actor(actor_id):

        try:
            actor = Actor.query.get_or_404(actor_id)
            old_actor = actor
            old_actor_formatted = actor.format()

            body = request.get_json()

            if body.get('name') is None:
                actor.name = old_actor.name
            else:
                actor.name = body.get('name')

            if body.get('age') is None:
                actor.age = old_actor.age
            else:
                actor.age = body.get('age')

            if body.get('gender') is None:
                actor.gender = old_actor.gender
            else:
                actor.gender = body.get('gender')

            actor.update()

            return jsonify({
                'success': True,
                'actor_before': old_actor_formatted,
                'modified_actor': actor.format(),
            })
        except():
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def delete_actor(actor_id):

        try:
            all_actors_before_delete = Actor.query.all()
            deleted_actor = Actor.query.get_or_404(actor_id)

            deleted_actor.delete()

            all_actors_after_delete = Actor.query.all()

            return jsonify({
                'success': True,
                'deleted_actor_id': deleted_actor.id,
                'deleted_actor': deleted_actor.format(),
                'number_of_actors_before': len(all_actors_before_delete),
                'number_of_actors_after': len(all_actors_after_delete)
            })
        except():
            abort(422)

    # ##################### MOVIES #####################

    @app.route('/movies')
    def get_movies():
        try:
            all_movies = Movie.query.all()
            format_movies = [movie.format() for movie in all_movies]

            if len(all_movies) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': format_movies,
                'all_movies': len(all_movies)
            })
        except():
            abort(500)

    @app.route('/movies', methods=['POST'])
    def post_movies():

        body = request.get_json()

        get_title = body.get('title')
        get_release_date = body.get('release_date')

        try:
            new_movie = Movie(title=get_title, release_date=get_release_date)
            new_movie.insert()

            return jsonify({
                'success': True,
                'new_movie': new_movie.format(),
                'created_id': new_movie.id
            })
        except():
            abort(422)
    return app
