# Importing necessary modules
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User

# Defining the EditProfileForm class for user profile editing


class EditProfileForm(FlaskForm):
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[
                             Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    # Initializing the class with original_username
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # Validating the uniqueness of username
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

# Defining the EditPostForm class for post editing


class EditPostForm(FlaskForm):
    body = StringField(_l('Message'), validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    # Initializing the class with original_body
    def __init__(self, original_body, *args, **kwargs):
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.original_body = original_body

# Defining the EmptyForm class for submitting empty form


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# Defining the PostForm class for creating a new post


class PostForm(FlaskForm):
    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

# Defining the EditForm class for editing a post


class EditForm(FlaskForm):
    post = TextAreaField(_l('Edit post'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))

# Defining the SearchForm class for searching posts


class SearchForm(FlaskForm):
    q = StringField(_l('Search'), validators=[DataRequired()])

    # Initializing the class with formdata and meta
    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)

# Defining the MessageForm class for sending messages


class MessageForm(FlaskForm):
    message = TextAreaField(_l('Message'), validators=[
                            DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))
