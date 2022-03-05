from flask.helpers import url_for
from werkzeug.utils import redirect
from . import login_bp
from flask import render_template, request, session, flash
from ...models.user import User
from .forms import (
    LoginForm, RegistrationForm,
    ResetPasswordForm, VerifyCodeForm, NewPasswordForm)
from .utils import (
    user_found, hash_password,
    get_role_id, random_characters,
    gmail_code, check_email_registration,
    save_new_password, get_role)


@login_bp.route('/login', methods=['GET', 'POST'])
def login() -> str:
    form = LoginForm()
    reg_form = RegistrationForm()
    if request.method == 'POST':
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        if user_found(email_address, password):
            session['role'] = get_role(email_address)
            session['status'] = 'logged-in'
            session['email_address'] = email_address
            if session['role'] == 'collector':
                return redirect(url_for('dashboard.collector_dashboard'))
            else:
                return redirect(url_for('dashboard.donor_dashboard'))
        else:
            flash(f'User not found.', 'error')
            return render_template('/login/base.html', form=form, reg_form=reg_form)
    elif 'email_address' in session:
        if session['role'] == 'collector':
            return redirect(url_for('dashboard.collector_dashboard'))
        else:
            return redirect(url_for('dashboard.donor_dashboard'))
    return render_template('/login/base.html', form=form, reg_form=reg_form)


@login_bp.route('/create account', methods=['GET', 'POST'])
def register() -> str:
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        user_role = request.form.get('account_type')
        user_role = get_role_id(user_role)
        street = request.form.get('street')
        barangay = request.form.get('barangay')
        city = request.form.get('city')
        org_name = request.form.get('org_name')
        about = request.form.get('about')
        email_address = request.form.get('email_address')
        password = request.form.get('password')
        password = hash_password(password)
        User(
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email_address,
            password=password,
            phone_number=phone_number,
            street=street,
            barangay=barangay,
            city=city,
            org_name=org_name,
            about=about,
            user_role=user_role
        ).add_new()
        session['email_address'] = email_address
        session['role'] = request.form.get('account_type')
    else:
        flash('Registration failed. E-mail, Phone Number, and Organization Name must be unique.', 'info')
    return redirect(url_for('login.login'))


@login_bp.route('/reset password', methods=['GET', 'POST'])
def reset_password() -> str:
    form = ResetPasswordForm()
    reg_form = RegistrationForm()
    if request.method == 'POST':
        email = request.form.get('email_address')
        registered_email = check_email_registration(email)
        if registered_email:
            session['email'] = email
            reset_code = random_characters()
            session['reset_code'] = reset_code
            gmail_code(reset_code, email)
            code_form = VerifyCodeForm()
            return render_template('/login/enter_code.html', email=session['email'], form=code_form, reg_form=reg_form)
        else:
            flash(f'That email address is not registered.', 'info')
            return render_template('/login/get_email.html', form=form, reg_form=reg_form)
    return render_template('/login/get_email.html', form=form, reg_form=reg_form)


@login_bp.route('/verify code', methods=['POST'])
def verify_code():
    form = NewPasswordForm()
    reg_form = RegistrationForm()
    if request.method == 'POST':
        user_input = request.form.get('code')
        if user_input == session['reset_code']:
            return render_template('/login/new_password.html', form=form, reg_form=reg_form)
        else:
            flash(f'Incorrect code.', 'info')
            return render_template('/login/enter_code.html', form=form, reg_form=reg_form, email=session['email'])


@login_bp.route('/check new password', methods=['POST'])
def check_new_password():
    form = NewPasswordForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        new_password = request.form.get('new_password')
        save_new_password(session['email'], new_password)
        return redirect(url_for('login.login'))
    else:
        form = NewPasswordForm()
        flash(f'Password did not match. Try again', 'info')
        return render_template('/login/new_password.html', form=form)


@login_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.login'))
