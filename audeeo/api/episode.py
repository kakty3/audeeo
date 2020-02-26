
from flask import request
from flask_restful import Resource
from marshmallow.exceptions import ValidationError
from marshmallow_sqlalchemy import ModelSchema

from audeeo import models, rest
from audeeo.database import db


class EpisodeSchema(ModelSchema):
    class Meta:
        model = models.Episode

class EpisodeResource(Resource):
    schema = EpisodeSchema()
    model = models.Episode
    default_per_page = 10

    def list(self, query, pagination):
        query = db.session.query(self.model).filter_by(**query)
        total = query.count()
        items = query.paginate(**pagination, error_out=False).items
        return rest.RestResult(items, self.schema, total=total)

    def retrieve(self, episode_id):
        episode = db.session.query(self.model).get(episode_id)
        if not episode:
            raise rest.exceptions.ResourceDoesNotExist
        return rest.RestResult(episode, self.schema)

    def get(self, episode_id=None):
        if episode_id:
            return self.retrieve(episode_id)

        query = dict(request.args)
        pagination = {
            'page': int(query.pop('page', 1)) ,
            'per_page': int(query.pop('per_page', self.default_per_page))
        }
        self.schema.validate(data=query, session=db.session, partial=True)
        return self.list(query, pagination)

    def post(self):
        deserialized = self.schema.load(request.json, session=db.session)
        db.session.add(deserialized)
        db.session.commit()
        return rest.RestResult(deserialized, self.schema)

    def put(self, episode_id=None):
        if not episode_id:
            raise rest.exceptions.ResourceDoesNotExist

        errors = self.schema.validate(request.json, session=db.session)
        if errors:
            raise ValidationError(errors)

        res = db.session.query(self.model).get(episode_id)
        for key, val in request.json.items():
            setattr(res, key, val)
        db.session.add(res)
        db.session.commit()
        return rest.RestResult(res, self.schema)

    def delete(self, episode_id=None):
        if not episode_id:
            raise rest.exceptions.ResourceDoesNotExist

        deleted = db.session.query(self.model).filter_by(id=episode_id).delete()
        db.session.commit()
        if not deleted:
            raise rest.exceptions.ResourceDoesNotExist

        return rest.RestResult({}, self.schema)
