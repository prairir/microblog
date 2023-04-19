from flask import render_template, current_app
from flask_babel import _
from app.email import send_email

# Sends a password reset email to a user containing a token to reset their password.


def send_password_reset_email(user):
    # Generate a token for resetting the user's password.
    token = user.get_reset_password_token()

    # Use the `send_email` function from the `email` module to send the reset password email to the user.
    # The email includes a subject, sender, recipients, and both text and HTML versions of the email body.
    send_email(_('[Microblog] Reset Your Password'),
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
