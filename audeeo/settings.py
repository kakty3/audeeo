import sys

from environs import Env, EnvError

env = Env()

try:
    ENV = env.str('FLASK_ENV', default='production')
    DEBUG = ENV == 'development'
    TESTING = env.bool('FLASK_TESTING', default=False)

    CSRF_ENABLED = True
    SECRET_KEY = env.str('FLASK_SECRET_KEY')

    SECURITY_PASSWORD_SALT = SECRET_KEY
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False

    SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IA_S3_ACCESS_KEY_ID = env.str('IA_S3_ACCESS_KEY_ID')
    IA_S3_SECRET_ACCESS_KEY_ID = env.str('IA_S3_SECRET_ACCESS_KEY_ID')
except EnvError as e:
    sys.exit('Error: {}'.format(e))
