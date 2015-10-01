import os
from datetime import datetime
from flask import redirect, render_template, flash, url_for, request, Blueprint, jsonify, g, current_app as app
from .models import db, User, user_datastore
from .errors import bad_request, ValidationError
from itsdangerous import URLSafeTimedSerializer
from .emails import send_confirmation_email, send_email

registration = Blueprint('users', __name__)

@registration.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(str(e))

@registration.route('/email', methods=['POST'])
def check_email():
    data = request.get_json(force=True)
    if not User().check_unique_email(data['email']):
        return validation_error('Email already exists. Please register with a new email.')
    else:
        return jsonify({'valid': 'true'})

@registration.route('/username', methods=['POST'])
def check_username():
    data = request.get_json(force=True)
    if not User().check_unique_username(data['username']):
        return validation_error('Username already exists. Please register with a new username.')
    else:
        return jsonify({'valid': 'true'})


@registration.route('/', methods=['POST'])
def register_user():
    data = request.get_json(force=True)
    if not User().check_unique_email(data['email']):
        return validation_error('Email already exists. Please register with a new email.')
    elif not User().check_unique_username(data['username']):
        return validation_error('Username already exists, please try another username')
    else:
        user = user_datastore.create_user(email=data['email'], password=data['password'])
        user.set_password(data['password'])
        user.active = False
        user.username = data['username']
        db.session.commit()

    email_token = generate_confirmation_token(user.email)
    confirm_url = url_for('.confirm_email', token=email_token, _external=True)
    send_confirmation_email(confirm_url, user)
    return jsonify({'id': user.id, 'message': 'User successfully created, please check your email to activate your account'})

def generate_confirmation_token(email):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

@registration.route('/confirm/<token>')
def confirm_email(token):
	email = confirm_token(token)
	user = User.query.filter_by(email=email).first_or_404()
	if user.email == email:
		user.active = True
		user.confirmed_at = datetime.utcnow()
		db.session.add(user)
		db.session.commit()
		flash('You have confirmed your account. Thanks!', 'success')
	else:
		flash('The confirmation link is invalid or has expired.', 'danger')
	return render_template("confirm.html")

def confirm_token(token, expiration=3600):
	serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
	try:
	    email = serializer.loads(
	        token,
	        salt=app.config['SECURITY_PASSWORD_SALT'],
	        max_age=expiration
	    )
	except:
	    return validation_error("Token is not verified!")
	return email
