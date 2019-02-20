import os
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from .internet_archive import InternetArchive

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
if os.path.isdir('instance'):
    app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
ia_client = InternetArchive(
    access_key=os.environ['IA_S3_ACCESS_KEY_ID'],
    secret_key=os.environ['IA_S3_SECRET_ACCESS_KEY_ID'],
)

from . import views, models, forms
