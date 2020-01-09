
from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import ModelSchema

from audeeo import models
from audeeo.database import db
from audeeo.rest import exceptions
from audeeo.rest.rest_result import RestResult


class EpisodeSchema(ModelSchema):
    class Meta:
        model = models.Episode

class EpisodeResource(Resource):
    schema = EpisodeSchema()
    model = models.Episode
    default_per_page = 10

    def list(self, query, pagination):
        total = db.session.query(self.model).filter_by(**query).count()
        items = db.session.query(self.model). \
               filter_by(**query).paginate(**pagination, error_out=False).items
        return RestResult(items, self.schema, total=total)

    def retrieve(self, episode_id):
        episode = db.session.query(self.model).get(episode_id)
        if not episode:
            raise exceptions.ResourceDoesNotExist
        return RestResult(episode, self.schema)

    def get(self, episode_id=None):
        if episode_id:
            return self.retrieve(episode_id)

        query = dict(request.args)
        pagination = {
            'page': int(query.pop('page')) if query.get('page') else 1,
            'per_page': int(query.pop('per_page')) if query.get('per_page') else self.default_per_page
        }
        self.schema.validate(data=query, session=db.session, partial=True)

        return self.list(query, pagination)

    def post(self):
        deserialized = self.schema.load(request.json, session=db.session)
        db.session.add(deserialized)
        db.session.commit()
        return RestResult(deserialized, self.schema)

    def put(self, episode_id=None):
        if not episode_id:
            raise exceptions.ResourceDoesNotExist

        errors = self.schema.validate(request.json, session=db.session)
        if errors:
            raise ValidationError(errors)

        res = db.session.query(self.model).get(episode_id)
        for key, val in request.json.items():
            setattr(res, key, val)
        db.session.add(res)
        db.session.commit()
        return RestResult(res, self.schema)

    def delete(self, episode_id=None):
        if not episode_id:
            raise exceptions.ResourceDoesNotExist
        deleted = db.session.query(self.model).filter_by(id=episode_id).delete()
        db.session.commit()
        if not deleted:
            raise exceptions.ResourceDoesNotExist
        return RestResult({}, self.schema)
