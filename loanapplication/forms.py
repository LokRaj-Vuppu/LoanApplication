# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators, DateField
# from wtforms.fields.html5 import EmailField
# from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#
# from loanapplication import db
# from loanapplication.models import customer
#
# class RegistrationForm(FlaskForm):
#     username = StringField('Username',
#                            validators=[DataRequired(), Length(min=2, max=20)])
#
#     email = EmailField('Email address',
#                        [validators.DataRequired(), validators.Email()])
#
#     password = PasswordField('Password', validators=[DataRequired()])
#
#     confirm_password = PasswordField('Confirm Password',
#                                      validators=[DataRequired(),
#                                                  EqualTo('password')])
#     submit = SubmitField('Sign Up')
#
#
#
#     def validate_email(self, email):
#         user = customer.query.filter_by(email=email.data).first()
#         if user:
#             raise ValidationError('That email is taken. Please choose a different one.')
#
# class LoginForm(FlaskForm):
#     email = EmailField('Email address',
#                        [validators.DataRequired(), validators.Email()])
#
#     password = PasswordField('Password', validators=[DataRequired()])
#
#     remember = BooleanField('Remember Me')
#
#     submit = SubmitField('Login')
