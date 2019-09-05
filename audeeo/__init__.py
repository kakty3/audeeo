import os

import click
from flask import Flask
from flask_migrate import Migrate
import flask_security

from audeeo import internet_archive, models, views
from audeeo.database import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)

    migrate = Migrate()
    migrate.init_app(app, db=db, compare_type=True, compare_server_default=True)

    user_datastore = flask_security.SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
    app.security = flask_security.Security()
    app.security.init_app(app, user_datastore)

    app.ia_client = internet_archive.InternetArchive(
        access_key=app.config['IA_S3_ACCESS_KEY_ID'],
        secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
    )

    app.register_blueprint(views.bp)
    register_shellcontext(app)
    register_commands(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {'db': db, 'models': models, 'ia': app.ia_client}

    app.shell_context_processor(shell_context)


@click.command(name='test')
def run_tests():
    import pytest
    pytest.main(['-s', 'tests'])

def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(run_tests)
