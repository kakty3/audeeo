import os

import click
import flask
import flask_marshmallow
import flask_migrate
import flask_security

from audeeo import internet_archive, models, views, settings
from audeeo.database import db
from audeeo.api import api_bp


def create_app(config_object=settings):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    # Order matters: Initialize SQLAlchemy before Marshmallow
    # https://flask-marshmallow.readthedocs.io/en/latest/
    db.init_app(app)
    flask_marshmallow.Marshmallow(app)

    migrate = flask_migrate.Migrate()
    migrate.init_app(app, db=db, compare_type=True, compare_server_default=True)

    user_datastore = flask_security.SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
    app.security = flask_security.Security()
    app.security.init_app(app, user_datastore)

    app.ia_client = internet_archive.InternetArchive(
        access_key=app.config['IA_S3_ACCESS_KEY_ID'],
        secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
    )

    app.register_blueprint(views.bp)
    app.register_blueprint(api_bp)
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
