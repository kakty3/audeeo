import os
import time
import uuid

from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from transliterate import slugify

from app import models, feed, ia_client, db
from app.internet_archive import InternetArchive


def upload_file(file_, ia_identifier):
    # ia_client = InternetArchive(
    #     access_key=os.environ['IA_S3_ACCESS_KEY_ID'],
    #     secret_key=os.environ['IA_S3_SECRET_ACCESS_KEY_ID'],
    # )
    # db = create_engine(os.environ['DATABASE_URL'])

    # file_key = uuid.uuid4().hex + os.path.splitext(secure_filename(file_.filename))[1]
    file_key = 'preved'
    response = ia_client.upload(identifier=ia_identifier, file=file_, key=file_key)
    file_url = ia_client.get_file_url(ia_identifier, file_key)

    basename = os.path.splitext(file_.filename)[0]
    title = secure_filename(slugify(basename) or basename)
    file_size = int(response.request.headers['Content-Length'])
    episode = models.Episode(title=title, url=file_url, file_size=file_size)
    db.session.add(episode)
    db.session.commit()

    feed.update_feed(ia_identifier)
