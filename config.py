import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.getenv('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    INTERNET_ARCHIVE_IDENTIFIER = 'podcast-hosting-test-Ia8gi'
    IA_S3_ACCESS_KEY_ID = os.getenv('IA_S3_ACCESS_KEY_ID')
    IA_S3_SECRET_ACCESS_KEY_ID = os.getenv('IA_S3_SECRET_ACCESS_KEY_ID')


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
