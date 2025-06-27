from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, URL, ValidationError, Optional

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
    enable_2fa = BooleanField('Enable Two-Factor Authentication', default=False)
    submit = SubmitField('Sign Up')

class TwoFactorForm(FlaskForm):
    token = StringField('Token', validators=[
        DataRequired(), Length(min=6, max=6, message='Token must be exactly 6 characters long.')
    ])
    submit = SubmitField('Verify Token')

class RecipeSuggestionForm(FlaskForm):
    dietary = SelectField(
        'Dietary Requirements',
        choices=[
            ('', 'No Requirements'),
            ('vegetarian', 'Vegetarian'),
            ('vegan', 'Vegan'),
            ('gluten free', 'Gluten Free'),
            ('dairy free', 'Dairy Free'),
            ('pescatarian', 'Pescatarian'),
            ('ketogenic', 'Ketogenic'),
            ('paleo', 'Paleo'),
            ('lacto-vegetarian', 'Lacto-Vegetarian'),
            ('ovo-vegetarian', 'Ovo-Vegetarian'),
            ('whole30', 'Whole30')
        ],
        default=''
    )
    submit = SubmitField('Get Recipe Suggestions')

class EditProfileForm(FlaskForm):
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    dark_mode = BooleanField('Enable Dark Mode', default=False)
    enable_2fa = BooleanField('Enable Two-Factor Authentication', default=False)
    submit = SubmitField('Update Profile')

class SaveRecipeForm(FlaskForm):
    pass

class ReviewForm(FlaskForm):
    review = TextAreaField('Your Review', validators=[DataRequired(), Length(max=500)])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired()])
    submit = SubmitField('Post Review')