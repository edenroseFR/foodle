from flask.app import Flask
from flask_wtf import FlaskForm
from .validators import UniqueEmail
from wtforms import (StringField, PasswordField,
    SubmitField, EmailField, TelField, RadioField, TextAreaField)
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    email_address = EmailField('E-mail',
        validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
        validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name *',
        validators=[DataRequired(), Length(min=2, max=50)])
    middle_name = StringField('Middle Name',
        validators=[Length(min=0, max=50)])
    last_name = StringField('Last Name *',
        validators=[DataRequired(), Length(min=2, max=50)])
    phone_number = TelField('Phone Number *',
        validators=[DataRequired(), Length(min=11, max=11)])
    account_type = RadioField('Account Type',
        choices=[('indiv-donor', 'Individial Donor'), 
                 ('org-donor', 'Organization Donor'), 
                 ('collector', 'Collector')])
    street = StringField('Street *',
        validators=[DataRequired(), Length(min=5, max=50)])
    barangay = StringField('Barangay *',
        validators=[DataRequired(), Length(min=5, max=50)])
    city = StringField('City *',
        validators=[DataRequired(), Length(min=5, max=50)])
    org_name = StringField('Organization Name',
        validators=[Length(min=0, max=100)])
    about = TextAreaField('About',
        validators=[Length(min=0, max=250)])
    email_address = EmailField('E-mail *',
        validators=[DataRequired(), Email(), UniqueEmail()])
    password = PasswordField('Password *',
        validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirm Password *',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
            

class ResetPasswordForm(FlaskForm):
    email_address = EmailField('E-mail',
        validators=[DataRequired(), Email()])
    submit = SubmitField('Get Reset Code')


class VerifyCodeForm(FlaskForm):
    code = StringField('Reset Code',
        validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewPasswordForm(FlaskForm):
    new_password = PasswordField('New Password',
        validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Submit')


                                    

