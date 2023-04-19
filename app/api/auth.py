# Import necessary modules and classes
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.models import User
from app.api.errors import error_response

# Create instances of the authentication classes
basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

# Define a function to verify user credentials for basic authentication


@basic_auth.verify_password
def verify_password(username, password):
    # Get the user with the given username from the database
    user = User.query.filter_by(username=username).first()
    # If the user exists and the provided password is correct, return the user
    if user and user.check_password(password):
        return user

# Define an error handler for basic authentication


@basic_auth.error_handler
def basic_auth_error(status):
    # Return an error response with the given status code
    return error_response(status)

# Define a function to verify a token for token authentication


@token_auth.verify_token
def verify_token(token):
    # Check if the token is valid by calling a method on the User model
    return User.check_token(token) if token else None

# Define an error handler for token authentication


@token_auth.error_handler
def token_auth_error(status):
    # Return an error response with the given status code
    return error_response(status)
