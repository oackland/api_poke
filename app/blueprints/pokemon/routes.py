from ...models import db
from . import pokemon


@pokemon.route("/thank-you")
def thank_you():
    return render_template("thank_You.html")


from flask import render_template
from .forms import InitialDataForm
from ...models import InitialData
from flask_login import current_user


@pokemon.route("/questionnaire", methods=["GET", "POST"])
def questionnaire():
    form = InitialDataForm()

    if form.validate_on_submit():
        user_id = current_user.id
        new_data = InitialData(
            user_id=user_id,
            level=1,
            xp=0,
            items={},
            pokemon=form.pokemon.data,
            team=form.team.data,
            user_idel=form.user_idel.data,
            user_idmove="",
        )
        db.session.add(new_data)
        db.session.commit()

        user_id = current_user.id

        initial_data = InitialData.query.filter_by(user_id=user_id).first()
        print(initial_data.team)

        return render_template("thank_You.html")

    return render_template("questionnaire.html", form=form)
