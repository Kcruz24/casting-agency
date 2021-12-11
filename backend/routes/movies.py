from flask import Blueprint, abort, jsonify, request

from backend.auth.auth import requires_auth
from backend.database.models.movie import Movie

movies_route = Blueprint('movies_route', __name__)


@movies_route.route('/movies')
@requires_auth('get:movies')
def get_movies(jwt):
    """
    This endpoint displays the movies available in the database.

    :param jwt: The bearer token for the current role to be authenticated.
    :return: A success value, a list of movies, and the quantity of movies
    available in the database.
    """

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


@movies_route.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def post_movies(jwt):
    """
    This endpoint creates a new movie and stores it in the database.

    :param jwt: The bearer token for the current role to be authenticated.
    :return: A success value, the newly created movie object, and the
    newly created movie id.
    """

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


@movies_route.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('patch:movies')
def patch_movie(jwt, movie_id):
    """
    This endpoint modifies the properties of a specific movie.

    :param jwt: The bearer token for the current role to be authenticated.
    :param movie_id: The selected movie id.
    :return: A success value, the movie object before modifications, and
    the movie object after modifications.
    """

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


@movies_route.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(jwt, movie_id):
    """
    This endpoint deletes a specific movie from the database.

    :param jwt: The bearer token for the current role to be authenticated.
    :param movie_id: The selected movie id to be deleted.
    :return: A success value, the deleted movie object, the quantity of
    movies before deletion, and the quantity of movies after deletion.
    """

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
