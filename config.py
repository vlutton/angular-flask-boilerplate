import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'api.sqlite')
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/boilerplate'
USE_TOKEN_AUTH = True

# mail params
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ['GMAIL_USERNAME']
MAIL_PASSWORD = os.environ['GMAIL_PASSWORD']

# flask security config
SECRET_KEY = "super-secret"
SECURITY_REGISTERABLE = True
SECURITY_REGISTER_URL = '/auth/register'
SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = 'add_salt'

JWT_EXPIRATION_DELTA = timedelta(days=3)
