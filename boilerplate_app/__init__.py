import os
from flask import Flask, render_template, request, url_for, redirect, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, logout_user
from flask.ext.restless import APIManager
from flask.ext.restless import ProcessingException
from flask.ext.login import user_logged_in
from flask.ext.cors import CORS
from flask_mail import Mail, Message


# JWT imports
from datetime import timedelta
from flask_jwt import JWT, jwt_required

from .errors import ValidationError

# Create app
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_CONFIG') or
                           'config')
mail = Mail(app)
CORS(app)

from .models import db, user_datastore

# creates the JWT Token authentication  ======================================
jwt = JWT(app)
@jwt.authentication_handler
def authenticate(username, password):
    user = user_datastore.find_user(email=username)
    if user is not None:
        if not user.is_active():
            abort(401)
        if username == user.email and user.check_password(password):
            return user
    return None

@jwt.user_handler
def load_user(payload):
    user = user_datastore.find_user(id=payload['user_id'])
    return user

from .api import protected_blueprint, user_blueprint
from .user import registration
app.register_blueprint(registration, url_prefix='/users')


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "error": "Unauthorized",
        "description": "Please check your email to activate your account.",
        "status_code": 401
    }), 401

db.create_all()
db.session.commit()
