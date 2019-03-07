import datetime

from . import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    url = db.Column(db.String(), unique=True)
    created_at = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Filename {}, url {}>'.format(self.filename, self.url)
