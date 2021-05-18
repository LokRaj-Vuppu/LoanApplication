from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_uploads import UploadSet,configure_uploads,IMAGES,TEXT,UploadNotAllowed
#from werkzeug import secure_filename, FileStorage
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
# from celery import Celery
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# WKHTMLTOPDF_PATH = 'C:/Program Files (x86)/Odoo 12.0/thirdparty/wkhtmltopdf'

Session = sessionmaker()
session = Session()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config.from_pyfile('config.py')
# app.config['CELERY_BROKER_URL'] = 'amqp://localhost//'
# app.config['CELERY_RESULT_BACKEND'] = 'amqp://localhost//'
app.config.from_pyfile('mail_config.py')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
# admin = Admin(app)

app.config['UPLOADED_IMAGES_DEST'] = 'uploads/images'

docimages = UploadSet('images', IMAGES)
configure_uploads(app, docimages)
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message_category = 'info'
#
#
#
#
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)
mail = Mail(app)




from loanapplication import routes
