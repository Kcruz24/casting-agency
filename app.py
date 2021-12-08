import os
import sys

from flask import Flask, flash, abort, request, jsonify, render_template
from flask_cors import CORS

from backend.auth.auth import requires_auth, AuthError
from backend.database.models.actor import Actor
from backend.database.models.movie import Movie
from backend.database.setup import setup_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
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
    @requires_auth('get:actors')
    def get_actors(jwt):
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
    @requires_auth('post:actors')
    def post_actors(jwt):

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
    @requires_auth('patch:actors')
    def patch_actor(jwt, actor_id):

        try:
            actor = Actor.query.get_or_404(actor_id)
            old_actor = actor
            old_actor_formatted = actor.format()

            body = request.get_json()

            actor.name = body.get('name', old_actor.name)
            actor.age = body.get('age', old_actor.age)
            actor.gender = body.get('gender', old_actor.gender)

            actor.update()

            return jsonify({
                'success': True,
                'actor_before': old_actor_formatted,
                'modified_actor': actor.format(),
            })
        except():
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):

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
    @requires_auth('get:movies')
    def get_movies(jwt):
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
    @requires_auth('post:movies')
    def post_movies(jwt):

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

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(jwt, movie_id):

        try:
            movie = Movie.query.get_or_404(movie_id)
            old_movie = movie
            old_movie_formatted = old_movie.format()

            body = request.get_json()

            movie.title = body.get('title', old_movie.title)
            movie.release_date = body.get('release_date',
                                          old_movie.release_date)

            movie.update()

            return jsonify({
                'success': True,
                'old_movie': old_movie_formatted,
                'modified_movie': movie.format()
            })
        except():
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):

        try:
            all_movies_before_delete = Movie.query.all()

            deleted_movie = Movie.query.get_or_404(movie_id)
            deleted_movie.delete()

            all_movies_after_delete = Movie.query.all()

            return jsonify({
                'success': True,
                'deleted_movie': deleted_movie.format(),
                'number_of_movies_before': len(all_movies_before_delete),
                'number_of_movies_after': len(all_movies_after_delete)
            })
        except:
            abort(422)

    # ##################### ERROR HANDLERS #####################

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(AuthError)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    return app


app = create_app()
if __name__ == '__main__':
    app.run()
