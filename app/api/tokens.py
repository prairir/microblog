# Importing necessary modules and functions for the program
from flask import jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


# Defining a route to generate and return a token for the authenticated user
@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required     # Require basic authentication for accessing this route
def get_token():

    # Generate a new token for the authenticated user
    token = basic_auth.current_user().get_token()

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response object containing the generated token
    return jsonify({'token': token})


# Defining a route to revoke a token for the authenticated user
@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required     # Require token authentication for accessing this route
def revoke_token():

    # Revoke the token for the authenticated user
    token_auth.current_user().revoke_token()

    # Commit the changes to the database
    db.session.commit()

    # Return an empty response with status code 204 indicating successful completion of the request
    return '', 204
