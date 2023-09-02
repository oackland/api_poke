from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired


class InitialDataForm(FlaskForm):
    user_idel = StringField("Username", validators=[DataRequired()])
    team = SelectField(
        "Select a team",
        choices=[("team1", "Team 1"), ("team2", "Team 2"), ("team3", "Team 3")],
        validators=[DataRequired()],
    )
    pokemon = SelectField(
        "Select an initial Pokemon",
        choices=[("pokemon1", "Pikachu"), ("pokemon2", "Charmane")],
        validators=[DataRequired()],
    )


class QuestionnaireForm(FlaskForm):
    name = StringField("Name")
    gender = RadioField(
        "Gender", choices=[("male", "Male"), ("female", "Female"), ("other", "Other")]
    )
