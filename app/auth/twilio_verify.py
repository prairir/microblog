from flask import current_app
from twilio.rest import Client, TwilioException


def _get_twilio_verify_client():
    # function to get Twilio Verify client object
    return Client(
        current_app.config['TWILIO_ACCOUNT_SID'],
        current_app.config['TWILIO_AUTH_TOKEN']).verify.services(
            current_app.config['TWILIO_VERIFY_SERVICE_ID'])


def request_verification_token(phone):
    # function to request verification token via Twilio Verify
    verify = _get_twilio_verify_client()
    try:
        verify.verifications.create(to=phone, channel='sms')
    except TwilioException:
        verify.verifications.create(to=phone, channel='call')


def check_verification_token(phone, token):
    # function to check verification token via Twilio Verify
    verify = _get_twilio_verify_client()
    try:
        result = verify.verification_checks.create(to=phone, code=token)
    except TwilioException:
        # return False if there is an exception
        return False
    # return True if verification is approved
    return result.status == 'approved'
