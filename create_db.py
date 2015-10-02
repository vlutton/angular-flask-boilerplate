from config import SQLALCHEMY_DATABASE_URI
from boilerplate_app.app import db
import os.path
db.create_all()
