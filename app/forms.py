from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DecimalRangeField
from wtforms.validators import DataRequired, Email, Length, URL, Optional, NumberRange, EqualTo

class SignUpForm(FlaskForm):
    """Form for signing up / adding user"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class CreatePost(FlaskForm):
    """Create Post Form."""

    message = TextAreaField('Message', validators=[Length(min=50, max=200), DataRequired()])
    link = StringField('Link', validators=[Optional(), URL()])

class CreateComment(FlaskForm):
    """Comment on a post"""

    text = TextAreaField('Comment', validators=[DataRequired()])

class AgreementForm(FlaskForm):
    """How much a user agrees"""

    agreement = DecimalRangeField('Agreement', validators=[NumberRange(min=0, max=100)])

class CustomizeProfile(FlaskForm):
    """Add details about user profile"""

    username = StringField('Username', validators=[DataRequired()])
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=50)])
    profile_pic = StringField('Profile_Pic', validators=[Optional()])
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm = PasswordField('Confirm', validators=[EqualTo('password', 'Password mismatch')])

class deleteProfile(FlaskForm):
    """Verifies password"""
    password = PasswordField('Password', validators=[Length(min=6)])
    confirm = PasswordField('Confirm', validators=[EqualTo('password', 'Password mismatch')])