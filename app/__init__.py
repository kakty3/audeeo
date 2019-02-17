import os
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

from .internet_archive import InternetArchive, get_ia_public_url
from .utils import is_audio


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
if os.path.isdir('instance'):
    app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

from . import views, models
