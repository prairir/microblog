# A function to determine whether the client wants a JSON response or not
def wants_json_response():
    # Check if the request accepts JSON and its weight is higher than HTML
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

# Error handler for 404 not found errors


@bp.app_errorhandler(404)
def not_found_error(error):
    # Check if the client wants a JSON response
    if wants_json_response():
        # Return a JSON response for API errors
        return api_error_response(404)
    # Otherwise, render a template for the HTML response
    return render_template('errors/404.html'), 404

# Error handler for 500 internal server errors


@bp.app_errorhandler(500)
def internal_error(error):
    # Rollback the session to ensure data consistency
    db.session.rollback()
    # Check if the client wants a JSON response
    if wants_json_response():
        # Return a JSON response for API errors
        return api_error_response(500)
    # Otherwise, render a template for the HTML response
    return render_template('errors/500.html'), 500
