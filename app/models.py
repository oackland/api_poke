from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    caption = db.Column(db.String)
    img_url = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, caption, img_url, user_id):
        self.title = title
        self.caption = caption
        self.img_url = img_url
        self.user_id = user_id
        self.date_created = datetime.utcnow()


class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))
    description = db.Column(db.String(300))

    def __init__(self, user_id, name, type, description):
        self.user_id = user_id
        self.name = name
        self.type = type
        self.description = description


class PokemonCard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id")
    )  # Corrected foreign key definition
    abilities = db.Column(db.JSON)
    artist = db.Column(db.String())
    ancientTrait = db.Column(db.String())
    attacks = db.Column(db.JSON)
    weaknesses = db.Column(db.JSON)

    def __init__(self, user_id, abilities, artist, ancientTrait, attacks, weaknesses):
        self.user_id = user_id
        self.abilities = abilities
        self.artist = artist
        self.ancientTrait = ancientTrait
        self.attacks = attacks
        self.weaknesses = weaknesses


class InitialData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    team = db.Column(db.String)
    user_idel = db.Column(db.String)
    user_idmove = db.Column(db.String)
    level = db.Column(db.Integer)
    xp = db.Column(db.Integer)
    items = db.Column(db.JSON)
    pokemon = db.Column(db.JSON)

    def __init__(
        self, user_id, level, xp, items, pokemon, team, user_idel, user_idmove
    ):
        self.user_id = user_id
        self.level = level
        self.xp = xp
        self.items = items
        self.pokemon = pokemon
        self.team = team
        self.user_idel = user_idel
        self.user_idmove = user_idmove


class GiftRegistry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipients = db.Column(db.JSON)
    senders = db.Column(db.JSON)
    gifts = db.Column(db.JSON)

    def __init__(self, recipients, senders, gifts):
        self.recipients = recipients
        self.senders = senders
        self.gifts = gifts


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    gender = db.Column(db.String(10))

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
