from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("login", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField()
