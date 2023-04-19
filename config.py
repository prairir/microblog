import os
from dotenv import load_dotenv

# Get the absolute path of the directory where this file is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Load the environment variables from the .env file
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # Set the Flask app's secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # Set the database URI for SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # Disable modifications of SQLAlchemy models by Flask-SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set the Twilio account SID, auth token, and verify service ID
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_ACCOUNT_TOKEN')
    TWILIO_VERIFY_SERVICE_ID = os.environ.get('TWILIO_VERIFY_SERVICE_ID')

    # Set whether to log to stdout
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # Set the email server settings
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Set the email address of the admin
    ADMINS = ['your-email@example.com']

    # Set the supported languages
    LANGUAGES = ['en', 'es']

    # Set the Microsoft Translator API key
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    # Set the Elasticsearch URL
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')

    # Set the Redis URL
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'

    # Set the number of posts to show per page
    POSTS_PER_PAGE = 25
