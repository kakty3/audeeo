import os
import uuid

import click
from flask import Flask, request, flash, redirect, url_for, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import redis
import rq
from werkzeug.utils import secure_filename

from .internet_archive import InternetArchive

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_pyfile('config.py', silent=True)
db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True, compare_server_default=True)
ia_client = InternetArchive(
    access_key=app.config['IA_S3_ACCESS_KEY_ID'],
    secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
)
redis_conn = redis.from_url(os.environ['REDIS_URL'])
q = rq.Queue(connection=redis_conn)

from . import views, models, forms

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'models': models, 'ia': ia_client}

@app.cli.command()
def run_worker():
    redis_url = app.config['REDIS_URL']
    redis_connection = redis.from_url(redis_url)
    with rq.Connection(redis_connection):
        worker = rq.Worker(['default'])
        worker.work()
