from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User

class LoginForm(FlaskForm):
    email = StringField('Enter Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    remember = BooleanField('Remember Login Credentials')
    submit = SubmitField('Complete & Submit')
	
class RegistrationForm(FlaskForm):
    username = StringField('Enter Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Enter Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                     validators=[DataRequired(), EqualTo('password')]) # checks if password actually matches
    submit = SubmitField('Complete & Submit')

	# checks attempted new username with current usernames and returns error if already taken
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
		
        if user:
            raise ValidationError('Entered Username is already in use.')

	# checks if email has been taken
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
		
        if user:
            raise ValidationError('Entered Email is already in use.')

			
			
			
class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Profile Pic', validators=[FileAllowed(['jpg'])]) # only jpg allowed
    submit = SubmitField('Complete & Submit')

	# checks attempted new username with current usernames and returns error if already taken
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
			
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')
	
	# checks if email has been taken
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
			
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class PostForm(FlaskForm):
    title = StringField('Enter your Post Title here', validators=[DataRequired()])
    content = TextAreaField('Enter your Post Content here', validators=[DataRequired()])
    submit = SubmitField('Complete & Submit')