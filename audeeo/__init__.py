import os

from flask import Flask

from audeeo import internet_archive, models
from audeeo.database import db

def create_app(config_filename):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config.from_pyfile(config_filename, silent=True)

    # Setup database
    db.init_app(app)

    # Setup Flask-Migrate
    from flask_migrate import Migrate
    migrate = Migrate()
    migrate.init_app(app, db=db, compare_type=True, compare_server_default=True)

    # Setup Flask-Security
    import flask_security
    user_datastore = flask_security.SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
    security = flask_security.Security()
    security.init_app(app, user_datastore)

    return app


app = create_app('config.py')

# Create InternetArchive client
ia_client = internet_archive.InternetArchive(
    access_key=app.config['IA_S3_ACCESS_KEY_ID'],
    secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
)

from audeeo import views

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'models': models, 'ia': ia_client}
