import os

import flask_security
import pytest

from audeeo import create_app, models
from audeeo.database import db

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        # https://stackoverflow.com/questions/26350911/what-to-do-when-a-py-test-hangs-silently
        db.session.remove()
        db.drop_all()

def test_development_config(app):
    app.config.from_object('config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')

def test_testing_config(app):
    app.config.from_object('config.TestingConfig')
    assert app.config['TESTING']
    assert not app.config['PRESERVE_CONTEXT_ON_EXCEPTION']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')

def test_production_config(app):
    app.config.from_object('config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get('DATABASE_URL')

def test_ping(app):
    client = app.test_client()
    resp = client.get('/ping')
    data = resp.data.decode()
    assert resp.status_code == 200
    assert data == 'pong'
