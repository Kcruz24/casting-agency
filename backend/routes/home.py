from flask import Blueprint, jsonify

home_route = Blueprint('home_route', __name__)


@home_route.route('/')
def home():
    """
    This is the home route, its purpose is to show that the API is working
    properly.

    :return: a success value and home route confirmation
    """

    return jsonify({
        'success': True,
        'home_route': True
    })
