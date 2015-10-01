
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user, logout_user
from .errors import ValidationError
from werkzeug.security import generate_password_hash, \
     check_password_hash

from savalidation import ValidationMixin, watch_session
from boilerplate_app import app

# Create database connection object
db = SQLAlchemy(app)

# Define Flask-security models ===============================================
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin, ValidationMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def check_unique_email(self, new_email):
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        else:
            return True

    def check_unique_username(self, new_username):
        if self.query.filter_by(username=new_username).first() is not None:
            return False
        else:
            return True

    def import_data(self, data):
        try:
            self.username = data['username']
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        try:
            self.email = data['email']
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        try:
            self.password = data['password']
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        return self

class Protected(db.Model):
    __tablename__ = 'protected'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(255))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
