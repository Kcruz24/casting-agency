from flask import Blueprint, jsonify

from backend.auth.auth import AuthError

error_handlers = Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(500)
def internal_server_error(error):
    """
    This error handler displays an internal server
    error message formatted with json.

    :param error: The specific error to be displayed.
    :return: A success value, the error code, and the error message.
    """
    return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500


@error_handlers.app_errorhandler(404)
def resource_not_found(error):
    """
    This error handler displays a resource not found error message
    formatted with json.

    :param error: The specific error to be displayed.
    :return: A success value, the error code, and the error message.
    """
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource Not Found'
    }), 404


@error_handlers.app_errorhandler(422)
def unprocessable_entity(error):
    """
    This error handler displays an unprocessable entity error message
    formatted with json.

    :param error: The specific error to be displayed.
    :return: A success value, the error code, and the error message.
    """
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Entity'
    }), 422


@error_handlers.app_errorhandler(405)
def method_not_allowed(error):
    """
    This error handler displays a method not allowed error message
    formatted with json.

    :param error: The specific error to be displayed.
    :return: A success value, the error code, and the error message.
    """
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'Method Not Allowed'
    }), 405


@error_handlers.app_errorhandler(AuthError)
def server_error(error):
    """
    This error handler displays a server error message formatted with json.

    :param error: The specific error to be displayed.
    :return: A success value, the error code, and the error message.
    """
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code
