from flask import Blueprint

after_requests = Blueprint('after_requests', __name__)


@after_requests.after_app_request
def after_request(res):
    print('HEADERS BEFORE ADDING:', res.headers)

    res.headers.add("Access-Control-Allow-Headers",
                    "Content-Type, authorization, true")

    res.headers.add("Access-Control-Allow-Methods",
                    'GET, POST, PATCH, DELETE, OPTIONS')

    print('HEDAERS AFTER ADDING:', res.headers)

    return res
