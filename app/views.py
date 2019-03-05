import os
import uuid
import tempfile

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from transliterate import slugify

from . import app, db, models, forms, ia_client, feed_generator
from .utils import is_audio


@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = forms.UploadFileForm()
    update_feed_form = forms.UpdateFeedForm()

    if upload_form.validate_on_submit():
        file = upload_form.file.data
        if not is_audio(file):
            message = 'File is not audio'
            flash(message, 'error')
            app.logger.info(message)
            
            return redirect(request.url)

        app.logger.info('Uploading file...')
        file_key = uuid.uuid4().hex + os.path.splitext(secure_filename(file.filename))[1]
        response = ia_client.upload(identifier=app.config['INTERNET_ARCHIVE_IDENTIFIER'], file=file, key=file_key)
        app.logger.info('Upload results %s', response)
        
        file_url = ia_client.get_public_url(app.config['INTERNET_ARCHIVE_IDENTIFIER'], file_key)
        message = 'File URL: {url}'.format(url=file_url)
        app.logger.info(message)
        flash(message, 'info')
        
        basename = os.path.splitext(file.filename)[0]
        title = secure_filename(slugify(basename) or basename)
        
        f = models.File(filename=title, url=file_url)
        db.session.add(f)
        db.session.commit()

    files = models.File.query.all()
    return render_template('index.html', files=files, upload_form=upload_form, update_feed_form=update_feed_form)


@app.route('/update-feed', methods=['POST'])
def update_feed():
    feed_ia_key = 'feed.xml'
    feed = feed_generator.generate_feed()
    
    with tempfile.TemporaryFile() as fp:
        fp.write(feed)
        fp.seek(0)
        response = ia_client.upload(
            identifier=app.config['INTERNET_ARCHIVE_IDENTIFIER'],
            file=fp,
            key=feed_ia_key,
            force=True
        )
    app.logger.info('Upload feed: %s', response)

    file_url = ia_client.get_public_url(app.config['INTERNET_ARCHIVE_IDENTIFIER'], feed_ia_key)
    message = 'Feed URL: {url}'.format(url=file_url)
    app.logger.info(message)
    flash(message, 'info')
    
    return redirect(url_for('index'))    
