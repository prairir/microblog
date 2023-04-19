from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User


class LoginForm(FlaskForm):
    # LoginForm class for the login form.
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class Confirm2faForm(FlaskForm):
    # Confirm2faForm class for the two-factor authentication token verification form.
    token = StringField('Token')
    submit = SubmitField('Verify')


class Enable2faForm(FlaskForm):
    # Enable2faForm class for the two-factor authentication enable form.
    verification_phone = StringField('Phone', validators=[DataRequired()])
    submit = SubmitField('Enable 2FA')


class Disable2faForm(FlaskForm):
    # Disable2faForm class for the two-factor authentication disable form.
    submit = SubmitField('Disable 2FA')


class RegistrationForm(FlaskForm):
    # RegistrationForm class for the user registration form.
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        # Validates that the username is not already taken.
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        # Validates that the email is not already in use.
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    # ResetPasswordRequestForm class for the password reset request form.
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    # ResetPasswordForm class for the password reset form.
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
