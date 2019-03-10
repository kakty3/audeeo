from sqlalchemy.sql.functions import now as sql_now
from sqlalchemy.sql.expression import text

from . import db


class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    url = db.Column(db.String(), unique=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=sql_now())
    pub_date = db.Column(db.DateTime(timezone=True), server_default=sql_now())
    file_size = db.Column(db.Integer, server_default=text('0'))

    def __repr__(self):
        return '<Title {}, url {}>'.format(self.title, self.url)
