#  Copyright (c) 2023 Oackland Toro
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.

import requests
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required
from ...models import Pokemon, db, User, InitialData
import json
from sqlalchemy import func

from . import main


#                                    ######################################
#                                    #####                              #####
#                                    ####           Home Page           ####
#                                    #####                              #####
#                                    ######################################


@main.route("/")
@main.route("/index")
def home():
    return render_template("index.html")


#                                    ######################################
#                                    #####                              #####
#                                    ####           Projects            ####
#                                    #####                              #####
#                                    ######################################


@main.route("/projects")
def projects():
    return render_template("projects.html")


#                                    ######################################
#                                    #####                              #####
#                                    ####        Pokemon game           ####
#                                    #####                              #####
#                                    ######################################


@main.route("/game")
@login_required
def game():
    return render_template("game.html", pokemon_data="pikachu", error_message=None)


#                                    ######################################
#                                    #####                              #####
#                                    ####        display card            ####
#                                    #####                              #####
#                                    ######################################


@main.route("/fetch_pokemon_data", methods=["GET", "POST"])
def fetch_pokemon_data():
    try:
        pokemon_name = request.form.get("pokemonName")

        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}/")
        response.raise_for_status()
        data = response.json()

        pokemon_data = {
            "name": data["name"],
            "hp": data["stats"][0]["base_stat"],
            "defense": data["stats"][2]["base_stat"],
            "attack": data["stats"][1]["base_stat"],
            "sprite_url": data["sprites"]["front_shiny"],
            "ability": data["abilities"][0]["ability"]["name"],
        }

        return render_template(
            "game.html", pokemon_data=pokemon_data, error_message=None
        )

    except requests.exceptions.RequestException as e:
        error_message = f"Error fetching Pokémon data: {str(e)}"
        return render_template(
            "game.html", pokemon_data=None, error_message=error_message
        )


#                                    ######################################
#                                    #####                              #####
#                                    ####           pokemon card         ####
#                                    #####                              #####
#                                    ######################################
from flask_login import current_user


@main.route("/save", methods=["POST"])
def save_card():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    user_id = current_user.id
    name = request.form.get("name")
    type = request.form.get("type")
    description = request.form.get("set")

    user_pokemons_count = Pokemon.query.filter_by(user_id=user_id).count()
    if user_pokemons_count >= 5:
        flash("Can't save more than five pokemons per person.")
        return redirect(url_for("main.pokedex"))

    pokemon = Pokemon(user_id=user_id, name=name, type=type, description=description)
    db.session.add(pokemon)
    db.session.commit()

    username = User.query.get(user_id).first_name

    return render_template("success.html", card=pokemon, username=username)


@main.route("/view_team_pokemons")
def view_team_pokemons():
    user_id = current_user.id

    initial_data = InitialData.query.filter_by(user_id=user_id).first()
    if not initial_data:
        return "User's team data not found"

    team_users = InitialData.query.filter_by(team=initial_data.team).all()
    user_ids = [user.user_id for user in team_users]

    pokemons = Pokemon.query.filter(Pokemon.user_id.in_(user_ids)).all()

    team_pokemons = []
    for pokemon in pokemons:
        url = f"https://api.pokemontcg.io/v2/cards?q=name:{pokemon.name}"
        response = requests.get(url)
        try:
            if response.status_code == 200:
                json_data = response.json()
                if "data" in json_data and len(json_data["data"]) > 0:
                    card_data = json_data["data"][0]
                    pokemon_dict = {
                        "name": pokemon.name,
                        "type": pokemon.type,
                        "description": pokemon.description,
                        "id": pokemon.id,
                        "image": card_data["images"]["small"],
                    }
                    team_pokemons.append(pokemon_dict)
        except:
            return "Something Went Wrong in API CALL"

    usernames = User.query.filter(Pokemon.user_id.in_(user_ids)).all()

    return render_template(
        "team_pokemons.html", team_pokemons=team_pokemons, usernames=usernames
    )


@main.route("/view_self_pokemons")
def view_self_pokemons():
    user_id = current_user.id

    initial_data = InitialData.query.filter_by(user_id=user_id).first()
    if not initial_data:
        return "User's team data not found"

    username = User.query.get(user_id).first_name

    pokemons = Pokemon.query.filter(Pokemon.user_id == user_id).all()
    self_pokemons = []
    for pokemon in pokemons:
        url = f"https://api.pokemontcg.io/v2/cards?q=name:{pokemon.name}"
        response = requests.get(url)
        try:
            if response.status_code == 200:
                json_data = response.json()
                if "data" in json_data and len(json_data["data"]) > 0:
                    card_data = json_data["data"][0]
                    pokemon_dict = {
                        "name": pokemon.name,
                        "type": pokemon.type,
                        "description": pokemon.description,
                        "id": pokemon.id,
                        "image": card_data["images"]["small"],
                    }
                    self_pokemons.append(pokemon_dict)
        except:
            return "Something Went Wrong in API CALL"

    return render_template(
        "self_pokemons.html", self_pokemons=self_pokemons, username=username
    )


from flask import request


@main.route("/delete_pokemon/<int:pokemon_id>", methods=["POST"])
def delete_pokemon(pokemon_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    pokemon = Pokemon.query.get_or_404(pokemon_id)

    db.session.delete(pokemon)
    db.session.commit()

    return redirect(url_for("main.pokedex"))


@main.route("/pokedex", methods=["GET", "POST"])
def pokedex():
    card_data = None
    if request.method == "POST":
        name = request.form.get("name")
        url = f"https://api.pokemontcg.io/v2/cards?q=name:{name}"
        response = requests.get(url)
        if response.status_code == 200:
            json_data = response.json()
            if "data" in json_data and len(json_data["data"]) > 0:
                card_data = json_data["data"][0]
                return render_template("pokedex.html", card=card_data)
            else:
                card_data = "No card found"
    return render_template("pokedex.html", card=card_data)


#                                    ######################################
#                                    #####                              #####
#                                    ####       END OF SECTION           ####
#                                    #####                              #####
#                                    ######################################
#
#             ]
#             session.modified = True
#
#     return render_template("pokedex.html", cards=session["cards"])
