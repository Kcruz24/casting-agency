import json
from functools import wraps
from urllib.request import urlopen

from decouple import config
from flask import request
from jose import jwt

AUTH0_DOMAIN = config('AUTH0_DOMAIN')
ALGORITHMS = config('ALGORITHMS')
API_AUDIENCE = config('API_AUDIENCE')


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'Authorization not present in headers',
            'description': 'Unable to get authorization from header'
        }, 401)

    auth_header = request.headers['Authorization']
    auth_header_split = auth_header.split(' ')

    if len(auth_header_split) != 2:
        raise AuthError({
            'code': 'header_malformed',
            'description': 'Authorization header length not equal to 2'
        }, 401)
    elif auth_header_split[0].lower() != 'bearer':
        raise AuthError({
            'code': 'bearer keyword not found',
            'description': 'The bearer keyword was not found in the '
                           'authorization header'
        }, 401)

    token = auth_header_split[1]
    print('Passed get_token_auth_header')
    return token


def check_permissions(permission, payload):
    print('getting into check_permissions')
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'Forbidden',
            'description': 'Permission not found'
        }, 403)

    print('Passed check_permissions')


def verify_decode_jwt(token):
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )

            print('Passed verify_decode_jwt')

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token is expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Incorrect claims. Please check the audience '
                               'and issuer'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropiate key'
    }, 400)


# Decorator method

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()

            payload = verify_decode_jwt(jwt)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
