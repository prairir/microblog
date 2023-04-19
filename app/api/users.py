from datetime import datetime, timedelta
from flask import jsonify, request, url_for, abort
from flask_login import login_user
import jwt
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    # Retrieve a user by their ID and return their dictionary representation.
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    # Retrieve a list of users and return them in a paginated response.
    # If page or per_page are not provided in the request, the defaults are 1 and 10 respectively.
    # The response contains links to the previous and next pages, if applicable.
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/<int:id>/followers', methods=['GET'])
@token_auth.login_required
def get_followers(id):
    # Retrieve a user's followers by their ID and return them in a paginated response.
    # If page or per_page are not provided in the request, the defaults are 1 and 10 respectively.
    # The response contains links to the previous and next pages, if applicable.
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followers, page, per_page,
                                   'api.get_followers', id=id)
    return jsonify(data)


@bp.route('/users/<int:id>/followed', methods=['GET'])
@token_auth.login_required
def get_followed(id):
    # Retrieve a user's followed users by their ID and return them in a paginated response.
    # If page or per_page are not provided in the request, the defaults are 1 and 10 respectively.
    # The response contains links to the previous and next pages, if applicable.
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(user.followed, page, per_page,
                                   'api.get_followed', id=id)
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    # Create a new user with the provided data.
    # If the required fields (username, email, password) are not present, return a 400 error.
    # If the username or email already exists, return a 400 error.
    # Return the newly created user's dictionary representation and a Location header with the URL to the user.

    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response


@bp.route('/login', methods=['POST'])
def login():
    # This function handles user login requests. It retrieves the user's login credentials from the request, checks that both the username and password fields are included, and then looks up the user's information in the database.
    # If the user exists, a JSON Web Token is generated and returned along with the user's information.
    # The user is also logged in using Flask-Login.

    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return bad_request('must include both username and password fields')

    user = User.query.filter_by(username=username).first()

    now = datetime.utcnow()
    expiration_time = now + timedelta(minutes=60)

    token = jwt.encode({'user_id': user.id, 'exp': expiration_time},
                       'your-secret-key', algorithm='HS256')

    response = jsonify({'access_token': token, 'user': user.to_dict()})
    login_user(user)
    response.status_code = 200
    return response


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    # This function handles user updates. It first checks that the current
    # authenticated user has permission to update the specified user by
    # comparing the IDs. If the authenticated user does not have permission,
    # a 403 error is returned. Otherwise, the user's information is updated
    # with the new data from the request, and the updated user information is
    # returned as a JSON object.

    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())
