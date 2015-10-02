from config import SQLALCHEMY_DATABASE_URI
from boilerplate_app.models import db
import os.path

db.create_all()
