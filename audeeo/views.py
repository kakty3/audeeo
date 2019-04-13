import os
import tempfile
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_security import login_required
from flask_sqlalchemy import SQLAlchemy
from transliterate import slugify
from werkzeug.utils import secure_filename

from audeeo import app, models, forms, ia_client, feed, utils
from audeeo.database import db


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    ia_identifier = app.config['INTERNET_ARCHIVE_IDENTIFIER']
    upload_form = forms.UploadFileForm()

    if upload_form.validate_on_submit():
        file = upload_form.file.data
        if not utils.is_audio(file):
            message = 'File is not audio'
            flash(message, 'error')
            app.logger.info(message)
            
            return redirect(request.url)

        app.logger.info('Uploading file...')
        file_key = uuid.uuid4().hex + os.path.splitext(secure_filename(file.filename))[1]
        response = ia_client.upload(identifier=ia_identifier, file=file, key=file_key)
        
        file_url = ia_client.get_file_url(ia_identifier, file_key)
        message = 'File URL: {url}'.format(url=file_url)
        app.logger.info(message)
        flash(message, 'info')
        
        app.logger.info('Adding record to db...')
        basename = os.path.splitext(file.filename)[0]
        title = secure_filename(slugify(basename) or basename)
        file_size = int(response.request.headers['Content-Length'])
        episode = models.Episode(title=title, url=file_url, file_size=file_size)
        db.session.add(episode)
        db.session.commit()

        app.logger.info('Updating feed...')
        feed.update_feed(ia_identifier, ia_client)

    episodes = models.Episode.query.order_by(models.Episode.created_at.desc()).all()
    feed_url = ia_client.get_file_url(ia_identifier, feed.FEED_KEY)
    return render_template('index.html', episodes=episodes, upload_form=upload_form, feed_url=feed_url)
