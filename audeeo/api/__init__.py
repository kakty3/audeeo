from flask import Flask, Blueprint, make_response
from flask_restful import Api, url_for

from .episode import EpisodeResource

from audeeo import rest


api_bp = Blueprint('api', __name__)

api = Api(
    api_bp,
    errors = {
        'ResourceDoesNotExist' : {
            'message': "A resource with that ID no longer exists.",
            'status': 410,
        },
        'ValidationError': {
            'status:': 400,
        }
    }
)

@api.representation('application/json')
def output_json(result, code, headers=None):
    serialized = result.schema.dumps(result.data, many=result.total != None)
    response = make_response(serialized, code)
    response.headers.extend(headers or {})
    return response

api.add_resource(EpisodeResource, '/episode/', '/episode/<int:episode_id>')
