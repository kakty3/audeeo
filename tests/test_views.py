import pytest

from audeeo import create_app
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

def test_ping(app):
    client = app.test_client()
    resp = client.get('/ping')
    data = resp.data.decode()
    assert resp.status_code == 200
    assert data == 'pong'
