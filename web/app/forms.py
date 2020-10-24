from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField()


class RegistrationForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    role = SelectField("role", validators=[DataRequired()], choices=['Student', 'Professor'])
    password = StringField("password", validators=[DataRequired()])
    password_rep = StringField("password_rep", validators=[DataRequired(), EqualTo('password')])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField()

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None or 'innopolis' not in email.data:
            raise ValidationError('Please use a different email address.')

    def validate_role(self, role):
        if role.data not in ['Student', 'Professor']:
            raise ValidationError('Please use correct role.')