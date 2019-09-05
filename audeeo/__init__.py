import os

from flask import Flask
from flask_migrate import Migrate
import flask_security

from audeeo import internet_archive, models, views
from audeeo.database import db


def create_app():
    app = Flask(__name__)
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
    app.security = flask_security.Security()
    app.security.init_app(app, user_datastore)

    app.ia_client = internet_archive.InternetArchive(
        access_key=app.config['IA_S3_ACCESS_KEY_ID'],
        secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
    )

    app.register_blueprint(views.bp)
    register_shellcontext(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {'db': db, 'models': models, 'ia': app.ia_client}

    app.shell_context_processor(shell_context)


from audeeo import views

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'models': models, 'ia': ia_client}
