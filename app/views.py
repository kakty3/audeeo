import os
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from transliterate import slugify

from . import app, db, models
from .internet_archive import InternetArchive, get_ia_public_url
from .utils import is_audio


INERNET_ARCHIVE_ITEM_NAME = 'podcast-hosting-test-Ia8gi'


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        files = db.session.query(models.File).order_by(models.File.id)
        return render_template('index.html', files=files)

    # check if POST request has the file part
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if not is_audio(file):
        message = 'File is not audio'
        flash(message, 'error')
        app.logger.info(message)
        return redirect(request.url)

    upload_destination = request.form['uploadDestionation']
    if upload_destination == 'local':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_url = url_for('uploaded_file', filename=filename)  
        flash('File uploaded to {}'.format(file_url), 'info')
    
    elif upload_destination == 'internet_archive':
        ia = InternetArchive(
            access_key=os.environ['IA_S3_ACCESS_KEY_ID'],
            secret_key=os.environ['IA_S3_SECRET_ACCESS_KEY_ID'],
        )
        file.name = uuid.uuid4().hex + os.path.splitext(file.filename)[1]
        response = ia.upload(item=INERNET_ARCHIVE_ITEM_NAME, filepath=file)
        app.logger.info('Upload results %s', response)
        
        file_url = get_ia_public_url(INERNET_ARCHIVE_ITEM_NAME, file.name)
        flash('File uploaded to {url}'.format(url=file_url), 'info')
        
        basename = os.path.splitext(file.filename)[0]
        title = slugify(basename) or basename
        uploaded_file = models.File(filename=title, url=file_url)
        db.session.add(uploaded_file)
        db.session.commit()
    else:
        flash('Invalid upload destination: {}'.format(upload_destination), 'error')

    return redirect(request.url)
