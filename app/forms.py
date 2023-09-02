from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField
from wtforms import (
    SubmitField,
    StringField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length, Optional
from wtforms.validators import EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email Address: password: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit_btn = SubmitField("Sign In")


class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
    confirm_password = StringField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit_btn = SubmitField("Register")


class PokemonCardForm(FlaskForm):
    card_name = StringField("Card Name", validators=[DataRequired()])
    abilities = TextAreaField("Abilities (JSON Format)", validators=[Optional()])
    artist = StringField("Artist", validators=[DataRequired(), Length(max=200)])
    ancientTrait = StringField(
        "Ancient Trait", validators=[Optional(), Length(max=200)]
    )
    attacks = TextAreaField("Attacks (JSON Format)", validators=[Optional()])
    weaknesses = TextAreaField("Weaknesses (JSON Format)", validators=[Optional()])
    submit = SubmitField("Submit")
