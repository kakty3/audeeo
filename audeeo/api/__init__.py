from flask import Flask, Blueprint, make_response
from flask_restful import Api, url_for

from .episode import EpisodeResource

from audeeo import rest


api_bp = Blueprint('api', __name__)

api = Api(
    api_bp,
    errors = {
        'ResourceDoesNotExist' : {
            'message': 'A resource with that ID no longer exists.',
            'status': 410,
        },
        'ValidationError': {
            'message': 'Invalid request',
            'status': 400,
        }
    }
)

@api.representation('application/json')
def output_json(result, code, headers=None):
    if type(result) == rest.rest_result.RestResult:
        result = result.schema.dumps(result.data, many=result.total != None)
    # Flask-Restful's error handling clashes w/ Marshmallow,
    # so resulting dict is a mess of original request data & FR's error fields.
    # because of that, if error - leave only 'message' and 'status' fields
    if code >= 400:
        result = {k: result.get(k) for k in ('message', 'status')}
    response = make_response(result, code)
    response.headers.extend(headers or {})
    return response

api.add_resource(EpisodeResource, '/episode/', '/episode/<int:episode_id>')
