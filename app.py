import os
import sys

from flask import Flask, render_template, flash, redirect, abort, request, \
    jsonify
from flask_cors import CORS

from backend.database.models.actor import Actor
from backend.database.models.movie import Movie
from backend.database.setup import setup_db
from backend.forms.actor_form import ActorForm


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
    def create_actor_submission():

        if request.method == 'GET':
            form = ActorForm()

            return render_template('forms/new_actor.html', form=form)

        error = False
        form = ActorForm()

        if form.validate_on_submit():
            try:
                new_actor = Actor()
                form.populate_obj(new_actor)

                new_actor.insert()

                flash(f'{new_actor.name} was successfully created!')
            except():
                error = True
                print(sys.exc_info())
                flash(
                    'Something went wrong when trying to create a new actor!')

            if not error:
                return redirect('/actors')
            else:
                abort(500)

    return app
