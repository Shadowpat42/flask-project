# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class CreateUserForm(FlaskForm):
    first_name = StringField("Имя: ", validators=[DataRequired()])
    last_name = StringField("Фамилия:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    submit = SubmitField("Отправить")


class CreatePostForm(FlaskForm):
    author_id = StringField("ID пользователя:", validators=[DataRequired()])
    text = TextAreaField(
        "Текст поста",
        validators=[DataRequired()],
        render_kw={"rows": 10, "style": "width: 75%;"},
    )
    submit = SubmitField("Отправить")


class CreateReactionForm(FlaskForm):
    user_id = StringField("ID пользователя:ㅤ", validators=[DataRequired()])
    reaction = StringField("Реакция:ㅤㅤㅤㅤㅤ", validators=[DataRequired()])
    submit = SubmitField("Отправить")
