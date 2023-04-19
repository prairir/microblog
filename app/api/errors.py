# Importing necessary modules for the program
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


# Defining a function to generate error response for a given status code and message
def error_response(status_code, message=None):

    # Creating a dictionary containing error message corresponding to the provided status code
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}

    # If a message is provided, add it to the dictionary
    if message:
        payload['message'] = message

    # Create a JSON response object from the dictionary
    response = jsonify(payload)

    # Set the status code of the response object to the provided status code
    response.status_code = status_code

    # Return the response object
    return response


# Defining a function to generate bad request error response with a given message
def bad_request(message):

    # Call the error_response function with status code 400 and the provided message
    return error_response(400, message)
