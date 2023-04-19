import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, source_language, dest_language):
    """
    Translates text from the source language to the destination language using the Microsoft Translator API.

    Args:
        text (str): The text to be translated.
        source_language (str): The language of the original text.
        dest_language (str): The language to which the text is to be translated.

    Returns:
        str: The translated text, if the translation was successful; otherwise, an error message.
    """
    # Check if the Microsoft Translator API key is available
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')

    # Set the API key and region for the Microsoft Translator API request
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westus2'
    }

    # Make the API request to translate the text
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[
                {'Text': text}])

    # If the API request was unsuccessful, return an error message
    if r.status_code != 200:
        return _('Error: the translation service failed.')

    # Extract the translated text from the API response and return it
    return r.json()[0]['translations'][0]['text']
