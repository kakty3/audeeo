import os
import tempfile
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_login import current_user
from flask_security import login_required
from flask_sqlalchemy import SQLAlchemy
from transliterate import slugify
from werkzeug.utils import secure_filename

from audeeo import app, models, forms, ia_client, utils
from audeeo.database import db


FEED_KEY = 'feed.xml'

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    upload_form = forms.UploadFileForm()
    user_feed = current_user.feeds.first()

    if upload_form.validate_on_submit():
        file = upload_form.file.data
        if not utils.is_audio(file):
            message = 'Not audio file'
            flash(message, 'error')
            app.logger.info(message)
            
            return redirect(request.url)

        app.logger.info('Upload file')
        file_key = uuid.uuid4().hex + os.path.splitext(secure_filename(file.filename))[1]
        response = ia_client.upload(identifier=user_feed.ia_identifier, file=file, key=file_key)
        
        file_url = ia_client.get_file_url(user_feed.ia_identifier, file_key)
        message = 'Episode upoaded: {url}'.format(url=file_url)
        app.logger.info(message)
        flash(message, 'info')
        
        app.logger.info('Add episode to db')
        basename = os.path.splitext(file.filename)[0]
        title = secure_filename(slugify(basename) or basename)
        file_size = int(response.request.headers['Content-Length'])
        episode = models.Episode(title=title, url=file_url, file_size=file_size)
        user_feed.episodes.append(episode)
        db.session.add(episode)
        db.session.commit()

        app.logger.info('Update feed')
        user_feed_rss = user_feed.get_rss()
        # TODO: try use SpooledTemporaryFile
        with tempfile.TemporaryFile() as fp:
            fp.write(user_feed_rss)
            fp.seek(0)
            ia_client.upload(
                identifier=user_feed.ia_identifier,
                file=fp,
                key=FEED_KEY,
                force=True
            )

    feed_url = ia_client.get_file_url(user_feed.ia_identifier, FEED_KEY)
    
    return render_template(
        'index.html',
        episodes=user_feed.episodes,
        upload_form=upload_form,
        feed_url=feed_url)
