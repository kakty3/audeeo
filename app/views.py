import os
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from transliterate import slugify

from . import app, db, models, forms, ia_client
from .utils import is_audio


@app.route('/', methods=['GET', 'POST'])
def index():
    form = forms.UploadFileForm()

    if form.validate_on_submit():
        file = form.file.data
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
    return render_template('index.html', files=files, form=form)
