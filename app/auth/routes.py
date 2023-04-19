# Import necessary modules and functions
from app.auth.twilio_verify import check_verification_token, request_verification_token
from flask import render_template, redirect, url_for, flash, request, session
from werkzeug.urls import url_parse
from flask_login import login_user, login_required, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import Confirm2faForm, Disable2faForm, Enable2faForm, LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email


# Route for user login
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already authenticated, and redirect to index if so
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # Create LoginForm object
    form = LoginForm()
    # Validate form input if POST request
    if form.validate_on_submit():
        # Query database for User with matching username
        user = User.query.filter_by(username=form.username.data).first()
        # If user doesn't exist or password is incorrect, flash error and redirect to login page
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        # Get next page from query parameter, or set to index
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        # If two-factor authentication is enabled, request verification token and redirect to verification page
        if user.two_factor_enabled():
            request_verification_token(user.verification_phone)
            session['username'] = user.username
            session['phone'] = user.verification_phone
            return redirect(url_for(
                'auth.verify_2fa', next=next_page,
                remember='1' if form.remember_me.data else '0'))
        # Otherwise, log user in and redirect to next page
        login_user(user, remember=form.remember_me.data)
        return redirect(next_page)
    # Render login page with LoginForm object
    return render_template('auth/login.html', title=_('Sign In'), form=form)


# Route for two-factor authentication verification
@bp.route('/verify_2fa', methods=['GET', 'POST'])
def verify_2fa():
    # Create Confirm2faForm object
    form = Confirm2faForm()
    # Validate form input if POST request
    if form.validate_on_submit():
        # Get phone number from session
        phone = session['phone']
        # If verification token is valid, either update current user's verification phone or log user in and redirect to next page
        if check_verification_token(phone, form.token.data):
            if current_user.is_authenticated:
                current_user.verification_phone = phone
                db.session.commit()
                flash('Two-factor authentication is now enabled')
                return redirect(url_for('main.index'))
            else:
                username = session['username']
                user = User.query.filter_by(username=username).first()
                next_page = request.args.get('next')
                remember = request.args.get('remember', '0') == '1'
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('main.index')
                login_user(user, remember=remember)
                return redirect(next_page)
        # If verification token is invalid, append error to form and render verification page
        form.token.errors.append('Invalid token')
    # Render verification page
    return render_template('auth/verify_2fa.html', form=form)


# Route to enable two-factor authentication
@bp.route('/enable_2fa', methods=['GET', 'POST'])
@login_required
def enable_2fa():
    form = Enable2faForm()
    if form.validate_on_submit():
        # Save verification phone number to session
        session['phone'] = form.verification_phone.data
        # Request verification token
        request_verification_token(session['phone'])
        # Redirect to 2FA verification page
        return redirect(url_for('auth.verify_2fa'))
    # Render the enable 2FA template
    return render_template('auth/enable_2fa.html', form=form)


# Route to disable two-factor authentication
@bp.route('/disable_2fa', methods=['GET', 'POST'])
@login_required
def disable_2fa():
    form = Disable2faForm()
    if form.validate_on_submit():
        # Set the verification phone number to None
        current_user.verification_phone = None
        db.session.commit()
        # Flash a message indicating that 2FA has been disabled
        flash('Two-factor authentication is now disabled.')
        # Redirect to the homepage
        return redirect(url_for('main.index'))
    # Render the disable 2FA template
    return render_template('auth/disable_2fa.html', form=form)


# Route to log out the user
@bp.route('/logout')
def logout():
    # Call Flask-Login's logout_user() function to log out the user
    logout_user()
    # Redirect to the homepage
    return redirect(url_for('main.index'))


# Route to register a new user
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # If the user is already authenticated, redirect to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create a new user object
        user = User(username=form.username.data, email=form.email.data)
        # Set the user's password
        user.set_password(form.password.data)
        # Add the user to the database
        db.session.add(user)
        db.session.commit()
        # Flash a message indicating that registration was successful
        flash(_('Congratulations, you are now a registered user!'))
        # Redirect to the login page
        return redirect(url_for('auth.login'))
    # Render the registration form
    return render_template('auth/register.html', title=_('Register'), form=form)


# Route to request a password reset
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # If the user is already authenticated, redirect to the homepage
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        # Find the user with the provided email address
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send the user an email with instructions on how to reset their password
            send_password_reset_email(user)
        # Flash a message indicating that an email has been sent
        flash(_('Check your email for the instructions to reset your password'))
        # Redirect to the login page
        return redirect(url_for('auth.login'))
    # Render the password reset request form
    return render_template('auth/reset_password_request.html', title=_('Reset Password'), form=form)

# Route to authenticate a password reset


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Redirect user to the index page if they are already authenticated
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    # Verify the user's token
    user = User.verify_reset_password_token(token)
    if not user:
        # If the token is invalid, redirect the user to the index page
        return redirect(url_for('main.index'))

    # Create a new instance of the reset password form
    form = ResetPasswordForm()

    if form.validate_on_submit():
        # If the form is submitted and is valid, set the user's new password
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))

    # If the form is not submitted, or is not valid, render the reset password template
    return render_template('auth/reset_password.html', form=form)
