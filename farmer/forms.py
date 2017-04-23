from flask_wtf import FlaskForm 
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo, ValidationError

from models import User

class EditForm(FlaskForm):
	username = StringField('Your Username: ')
	email = StringField('Your e-mail: ')
	region= StringField('Your Region: ')

class AddDiseaseForm(FlaskForm):
	name = StringField('name', validators=[DataRequired()])
	category = SelectField('category', validators=[DataRequired()], choices=[('Primary', 'Primary'),('Secondary','Secondary')])
	symptoms = TextAreaField('symptoms', validators=[DataRequired()])
	remedy = TextAreaField('remedy', validators=[DataRequired()])
	submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Your Username: ', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField('Log In')

class SignupForm(FlaskForm):
	username = StringField('Username',
							validators=[
							DataRequired(), Length(3, 80),
							#Regexp('^[A-Za-z0-9_]{3,}S',
							#	message='Usernames consist of numbers, letters,''and underscores.')
							])
	password = PasswordField('Password',
					validators=[
					DataRequired(),
					EqualTo('password2', message='Passwords must match.')])
	password2 = PasswordField('Confirm Password', validators=[DataRequired()])
	email = StringField('Email',
				validators=[DataRequired(), Length(1, 120), Email()])

	def validate_email(self, email_field):
		if User.query.filter_by(email=email_field.data).first():
			raise ValidationError('There is already a user with this email address.')

	def validate_username(self, username_field):
		if User.query.filter_by(username=username_field.data).first():
			raise ValidationError('This username is already taken')
