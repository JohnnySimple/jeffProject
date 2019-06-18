from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileField,FileRequired


#class for admin login form
class adminLogin(FlaskForm):
	admin_username = StringField('USERNAME',
		validators=[DataRequired(), Length(min=2, max=20)])
	admin_password = PasswordField('PASSWORD',
		validators=[DataRequired()])
	submit = SubmitField('LOGIN')


class postForm(FlaskForm):
	title = StringField('TITLE',
		validators=[DataRequired(), Length(min=2, max=200)])
	content = StringField('CONTENT',
		validators=[DataRequired()], widget=TextArea())
	date = DateField('DATE',
		validators=[DataRequired()])
	image = FileField(validators=[FileRequired()])
	submit = SubmitField('POST')

class commentForm(FlaskForm):
	name = StringField('NAME',
		validators=[DataRequired(), Length(min=2, max=100)])
	content = StringField('CONTENT',
		validators=[DataRequired()], widget=TextArea())
	submit = SubmitField('COMMENT')

class contactForm(FlaskForm):
	name = StringField('NAME',
		validators=[DataRequired(), Length(min=2, max=200)])
	email = StringField('EMAIL',
		validators=[DataRequired(), Email()])
	message = StringField('MESSAGE',
		validators=[DataRequired()], widget=TextArea())
	submit = SubmitField('SEND MESSAGE')

class subscriptionForm(FlaskForm):
	email = StringField('EMAIL',
		validators=[DataRequired(), Email()])
	submit = SubmitField('SUBSCRIBE')