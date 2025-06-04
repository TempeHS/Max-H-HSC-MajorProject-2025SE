from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, URL, ValidationError


def validate_password(form, field):
    password = field.data
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit.')
    if not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least one letter.')
    if len(password) < 6:
        raise ValidationError('Password must be at least 6 characters long.')

def validate_location(form, field):
    location = field.data
    if len(location) > 100:
        raise ValidationError('Location must be at most 100 characters long.')
    if not any(char.isupper() for char in location):
        raise ValidationError('Location must contain at least one uppercase letter.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=25), Regexp(r'^[a-zA-Z0-9_]+$', message='Username must contain only letters, numbers, and underscores.')
    ])
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=25), Regexp(r'^[a-zA-Z0-9_]+$', message='Username must contain only letters, numbers, and underscores.')
    ])
    email = StringField('Email', validators=[
        Email(message='Invalid email address.')
    ])
    password = PasswordField('Password', validators=[DataRequired(), validate_password])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password', message='Passwords must match.')
    ])
    location = StringField('Location', validators=[
        DataRequired(), validate_location
    ])
    submit = SubmitField('Sign Up')

class TwoFactorForm(FlaskForm):
    token = StringField('Token', validators=[
        DataRequired(), Length(min=6, max=6, message='Token must be exactly 6 characters long.')
    ])
    submit = SubmitField('Verify Token')

class RecipeSuggestionForm(FlaskForm):
    dietary = StringField('Dietary Requirements (comma separated)')
    submit = SubmitField('Get Recipe Suggestions')