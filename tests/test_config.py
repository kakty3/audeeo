import os

import pytest

from audeeo import create_app


@pytest.fixture
def app():
    return create_app()

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
