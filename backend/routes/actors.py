import sys

from flask import Blueprint, abort, jsonify, request

from backend.auth.auth import requires_auth
from backend.database.models.actor import Actor

actors_route = Blueprint('actors_route', __name__)


@actors_route.route('/actors')
@requires_auth('get:actors')
def get_actors(jwt):
    """
    This endpoint displays all the available actors in the database.

    :param jwt: The bearer token for the current role to be authenticated.
    :return: A success value, a list of actos and the quanity of available
    actors.
    """

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


@actors_route.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def post_actors(jwt):
    """
    This endpoint creates a new actor and store it into the database.

    :param jwt: The bearer token for the current role to be authenticated.
    :return: A success value, the newly created actor id, and the actor
    object itself.
    """

    error = False

    body = request.get_json()

    get_name = body.get('name')
    get_age = body.get('age')
    get_gender = body.get('gender')

    new_actor = None

    try:
        new_actor = Actor(name=get_name, age=get_age, gender=get_gender)
        new_actor.insert()

    except():
        error = True
        print(sys.exc_info())

    if not error:
        return jsonify({
            'success': True,
            'created': new_actor.id,
            'new_actor': new_actor.format()
        })
    else:
        abort(500)


@actors_route.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('patch:actors')
def patch_actor(jwt, actor_id):
    """
    This endpoint modifies the properties of a specific actor.

    :param jwt: The bearer token for the current role to be authenticated.
    :param actor_id: The actor id to be modified.
    :return: A success value, the actor object before modifications,
    and the actor object after modifications.
    """

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


@actors_route.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(jwt, actor_id):
    """
    This endpoint deletes a specific actor from the database.

    :param jwt: The bearer token for the current role to be authenticated.
    :param actor_id: The actor id to be deleted.
    :return: A success value, the deleted actor id, the deleted actor object
    , the quantity of actors before deletion, and the quantity of actors
    after deletion.
    """

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
