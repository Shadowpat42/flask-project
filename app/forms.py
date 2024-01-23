# forms.py
from app import USERS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateUserForm(FlaskForm):
    first_name = StringField("Имя: ", validators=[DataRequired()])
    last_name = StringField("Фамилия:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    submit = SubmitField("Отправить")
