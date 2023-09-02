from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class PlayerForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Add Player")
