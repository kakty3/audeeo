import os
import uuid
import tempfile

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from transliterate import slugify

from . import app, db, models, forms, ia_client, feed
from .utils import is_audio


@app.route('/', methods=['GET', 'POST'])
def index():
    upload_form = forms.UploadFileForm()

    if upload_form.validate_on_submit():
        file = upload_form.file.data
        if not is_audio(file):
            message = 'File is not audio'
            flash(message, 'error')
            app.logger.info(message)
            
            return redirect(request.url)

        ia_identifier = app.config['INTERNET_ARCHIVE_IDENTIFIER']
        app.logger.info('Uploading file...')
        file_key = uuid.uuid4().hex + os.path.splitext(secure_filename(file.filename))[1]
        response = ia_client.upload(identifier=ia_identifier, file=file, key=file_key)
        app.logger.info('Upload results %s', response)
        
        file_url = ia_client.get_public_url(ia_identifier, file_key)
        message = 'File URL: {url}'.format(url=file_url)
        app.logger.info(message)
        flash(message, 'info')
        
        app.logger.info('Adding record to db...')
        basename = os.path.splitext(file.filename)[0]
        title = secure_filename(slugify(basename) or basename)
        f = models.File(filename=title, url=file_url)
        db.session.add(f)
        db.session.commit()

        app.logger.info('Updating feed...')
        feed.update_feed(ia_identifier)

    files = models.File.query.order_by(models.File.created_at.desc()).all()
    return render_template('index.html', files=files, upload_form=upload_form)
