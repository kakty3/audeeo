import os
import uuid
import tempfile

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from transliterate import slugify

from app import app, db, models, forms, ia_client, feed, q, tasks
from app.utils import is_audio

@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = forms.UploadFileForm()
    ia_identifier = app.config['INTERNET_ARCHIVE_IDENTIFIER']

    if upload_form.validate_on_submit():
        file = upload_form.file.data    
        if not is_audio(file):
            message = 'File is not audio'
            flash(message, 'error')
            app.logger.info(message)
            
            return redirect(request.url)

        # app.logger.info(type(file.stream))
        # app.logger.info(dir(file.stream))
        app.logger.info('fileno: %s', file.stream.fileno())
        job = q.enqueue(tasks.upload_file, file.stream.fileno(), ia_identifier)
        app.logger.info('Started job %s', job)

        # app.logger.info('Uploading file...')
        # file_key = uuid.uuid4().hex + os.path.splitext(secure_filename(file.filename))[1]
        # response = ia_client.upload(identifier=ia_identifier, file=file, key=file_key)
        
        # file_url = ia_client.get_file_url(ia_identifier, file_key)
        # message = 'File URL: {url}'.format(url=file_url)
        # app.logger.info(message)
        # flash(message, 'info')
        
        # app.logger.info('Adding record to db...')
        # basename = os.path.splitext(file.filename)[0]
        # title = secure_filename(slugify(basename) or basename)
        # file_size = int(response.request.headers['Content-Length'])
        # episode = models.Episode(title=title, url=file_url, file_size=file_size)
        # db.session.add(episode)
        # db.session.commit()

        # app.logger.info('Updating feed...')
        # feed.update_feed(ia_identifier)

    episodes = models.Episode.query.order_by(models.Episode.created_at.desc()).all()
    feed_url = ia_client.get_file_url(ia_identifier, feed.FEED_KEY)
    return render_template('index.html', episodes=episodes, upload_form=upload_form, feed_url=feed_url)
