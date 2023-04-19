from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    """
    A helper function to send emails asynchronously.

    Parameters:
    app (Flask): The Flask application object
    msg (flask_mail.Message): The email message to send

    Returns:
    None
    """
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    """
    Sends an email to one or more recipients asynchronously or synchronously.

    Parameters:
    subject (str): The subject line of the email
    sender (str): The email address of the sender
    recipients (list): A list of email addresses of the recipients
    text_body (str): The plain text content of the email
    html_body (str): The HTML content of the email
    attachments (list, optional): A list of file attachments to include in the email
    sync (bool, optional): If True, the email will be sent synchronously. If False, the email will be sent asynchronously

    Returns:
    None
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()
