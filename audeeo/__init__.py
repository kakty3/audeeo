import os

from flask import Flask
from flask_security import Security, SQLAlchemySessionUserDatastore
from flask_migrate import Migrate

from audeeo import internet_archive, models
from audeeo.database import db

# Create app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_pyfile('config.py', silent=True)

# # Setup database
db.init_app(app)

# Setup Flask-Migrate
migrate = Migrate(app, db, compare_type=True, compare_server_default=True)

# Create InternetArchive client
ia_client = internet_archive.InternetArchive(
    access_key=app.config['IA_S3_ACCESS_KEY_ID'],
    secret_key=app.config['IA_S3_SECRET_ACCESS_KEY_ID'],
)

from audeeo import views

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, models.User, models.Role)
security = Security(app, user_datastore)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'models': models, 'ia': ia_client}
