import os
import uuid

from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

from .internet_archive import InternetArchive

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
ia_client = InternetArchive(
    access_key=app.config['IA_S3_ACCESS_KEY_ID'],
    secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
)

from . import views, models, forms

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'models': models, 'ia': ia_client}
