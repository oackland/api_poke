#  Copyright (c) 2023 Oackland Toro
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.

import requests
from flask import render_template, request
from .forms import PlayerForm
from . import battle
from ...models import Pokemon, db, User, InitialData
from flask import redirect, url_for, session
from flask_login import current_user
from pokemontcgsdk import Card

BASE_URL = "https://api.pokemontcg.io/v2/cards?q=name:gardevoir"


@battle.route("/battlefield")
def battlefield():
    response = requests.get(BASE_URL)
    data = response.json()
    cards = data["data"][:3]

    return render_template("battlefield.html", cards=cards)


from flask import render_template


@battle.route("/players", methods=["GET", "POST"])
def players():
    # Retrieve all users from the "User" table
    users = User.query.all()

    if request.method == "POST":
        selected_pokemon_id = request.form.get("selected_pokemon")

    return render_template("player_form.html", users=users)


@battle.route("/selectmine", methods=["GET", "POST"])
def my_pokemons():
    if request.method == "POST":
        selected_pokemon_id = request.form.get("selected_pokemon")

        selected_pokemon = Pokemon.query.filter_by(id=selected_pokemon_id).first()
        session["opponent"] = selected_pokemon
        print(selected_pokemon)
        user_id = current_user.id
        username2 = User.query.filter_by(id=user_id).first()
        username = username2.first_name
        user_pokemons = Pokemon.query.filter_by(user_id=user_id).all()
        return render_template(
            "self_selection_pokemons.html",
            user_pokemons=user_pokemons,
            username=username,
        )


@battle.route("/<username>/pokemons", methods=["GET", "POST"])
def user_pokemons(username):
    user = User.query.filter_by(first_name=username).first()

    user_pokemons = Pokemon.query.filter_by(user_id=user.id).all()

    return render_template(
        "user_pokemons.html", user_pokemons=user_pokemons, username=username
    )


@battle.route("/winner", methods=["GET"])
def winner():
    my_pokemon = session["my_pokemon"]

    query = f"supertype:pokemon name:{my_pokemon.name}"
    my_card = Card.where(q=query)[0]

    opp_pokemon = session["opponent"]

    query = f"supertype:pokemon name:{opp_pokemon.name}"
    opp_card = Card.where(q=query)[0]
    my_total = int(my_card.hp) if my_card.hp else 0
    my_total += sum(
        [int(attack.damage) if attack.damage else 0 for attack in my_card.attacks]
    )

    opp_total = int(opp_card.hp) if opp_card.hp else 0
    opp_total += sum(
        [int(attack.damage) if attack.damage else 0 for attack in opp_card.attacks]
    )

    if my_total > opp_total:
        winner_name = my_card.name
    elif opp_total > my_total:
        winner_name = opp_card.name
    else:
        winner_name = "It's a tie!"

    return render_template("winner.html", winner=winner_name)


@battle.route("/fight", methods=["GET", "POST"])
def fight():
    if request.method == "POST":
        selected_pokemon_id = request.form.get("selected_pokemon")

        selected_pokemon = Pokemon.query.filter_by(id=selected_pokemon_id).first()
        session["my_pokemon"] = selected_pokemon
    my_pokemon = session["my_pokemon"]

    query = f"supertype:pokemon name:{my_pokemon.name}"
    my_card = Card.where(q=query)[0]

    opp_pokemon = session["opponent"]

    query = f"supertype:pokemon name:{opp_pokemon.name}"
    opp_card = Card.where(q=query)[0]

    return render_template(
        "fight.html",
        my_card=my_card,
        mypokemon=my_pokemon,
        opp_pokemon=opp_pokemon,
        opp_card=opp_card,
    )
