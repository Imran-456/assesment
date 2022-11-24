from src import app, bcrypt, db
from src.models.db_models import user
from src.utils.const import *
from flask import request, jsonify
from src.utils.helper import *
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime, timedelta


@app.route('/api/v1/register', methods=["POST"])
def register():
    """
    This route handles the registration of new users
    """
    # Gets data from the request
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    # validates name
    if not validate_name(name):
        return jsonify(name_validation_error_message)

    # Validates password
    if not validate_password(password):
        return jsonify(password_validation_error_message)

    # Validates password
    email_validation, flag = validate_email(email)

    if email_validation is False:
        if flag == 'Flag1':
            return jsonify(email_validation_error_message)
        else:
            return jsonify(email_duplication_error_message)

    # Hashing the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Creating a new user
    new_user = user(name=name, email=email, password=hashed_password)

    # Adding the user to DB
    db.session.add(new_user)
    db.session.commit()

    # Response
    return jsonify(successful_register_message)


@app.route('/api/v1/login', methods=["POST"])
def login():
    """
    This route handles the login of users
    """
    # Gets data from the request
    email = request.json.get("email")
    password = request.json.get("password")

    # Fetches the user by email.
    current_user = user.query.filter_by(email=email).one_or_none()

    if current_user is None:
        response = jsonify(Failed_login_message), 401
    else:
        # checks if the password is correct or not
        if bcrypt.check_password_hash(current_user.password, password):
            # Registers the access token for current session
            access_token = create_access_token(
                identity=current_user.id, expires_delta=timedelta(minutes=3))

            response = jsonify(message=successful_login_message,
                               access_token=access_token), 200
        else:
            response = jsonify(Failed_password_login_message), 401

    # Response
    return response
