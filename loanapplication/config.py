import os
DEBUG = True

SECRET_KEY = os.urandom(20)
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/creditapp'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO=True
SECURITY_REGISTERABLE=True
SECURITY_PASSWORD_SALT='passwordsalt'
SECURITY_SEND_REGISTER_EMAIL=True
SECURITY_CONFIRMABLE=False
