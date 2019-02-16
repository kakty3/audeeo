from app import db

class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String())
    url = db.Column(db.String(), unique=True)

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url

    def __repr__(self):
        return '<Filename {}, url {}>'.format(self.filename, self.url)
