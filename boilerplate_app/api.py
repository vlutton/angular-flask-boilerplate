from flask.ext.restless import APIManager
from flask.ext.restless import ProcessingException

# JWT imports
from datetime import timedelta
from flask_jwt import JWT, jwt_required, current_user

from boilerplate_app import app
from .models import db, user_datastore, User, Protected


def is_authorized(user, instance):
    if int(user.id) == int(instance):
        return True
    else:
        return False

# Flask-Restless API ==========================================================
# Make sure that the current user can only see their own stuff
@jwt_required()
def auth_user_func(instance_id=None, **kw):
    if not is_authorized(current_user, instance_id):
        raise ProcessingException(description='Not Authorized',
                                code=401)
@jwt_required()
def auth_admin_func(instance_id=None, **kw):
    raise ProcessingException(description='Only admins can access this view',
                            code=401)

@jwt_required()
def auth_func(instance_id=None, **kw):
    pass;

apimanager = APIManager(app, flask_sqlalchemy_db=db)

protected_blueprint = apimanager.create_api(Protected,
    methods=['GET', 'POST', 'DELETE', 'PUT'],
    url_prefix='/api/v1',
    preprocessors=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func]),
    collection_name='protected_data',
    include_columns=['id','name', 'description'])

user_blueprint = apimanager.create_api(User,
    methods=['GET', 'PUT'],
    url_prefix='/api/v1',
    preprocessors=dict(GET_SINGLE=[auth_user_func], GET_MANY=[auth_admin_func]),
    collection_name='user',
    include_columns=['id', 'username', 'data2', 'user_id'])
