import json
import os

from flask import Flask, render_template, request, flash, redirect
from models import db, connect_db, Coins
from helpers import count_coins, validate_form, generate_response

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///make-change'))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

##########
# Routes #
##########

@app.route("/")
def homepage():
    """Show homepage."""

    coins = Coins.query.order_by(Coins.value.desc()).all()

    return render_template("base.html", coins = coins)

@app.route("/exchange", methods=["POST"])
def exchange_for_coins():
    """Run helper function to exchange for coins."""

    amount = request.form["currency"]
    data = count_coins(amount)

    flash(data)

    return redirect("/")

@app.route("/coins/add", methods=["POST"])
def add_new_coin():
    """Add a new coin to data base"""

    data = request.get_json()
    errors = validate_form(data)
    resp = generate_response(data)

    if len(errors) > 0:
        # returns python object as Json string
        return json.dumps({'error': errors})
    else: 
        name = data["name"]
        value = data["value"]
        new_coin = Coins(name = name, value = value)
            
        db.session.add(new_coin)
        db.session.commit()

        flash(f"New coin added! {name}: {value}")
        return resp


@app.route("/coins/remove/<int:coin_id>", methods=["POST"])
def remove_coin(coin_id):
    """Remove one coin from database"""

    coin = Coins.query.get(coin_id)

    db.session.delete(coin)
    db.session.commit()

    return redirect("/")




#################
# After Request #
#################

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req