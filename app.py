import json
from operator import index
import os

from flask import Flask, render_template, request, flash, redirect, session, g
from models import db, connect_db, Coins
from sqlalchemy.exc import IntegrityError
from helpers import count_coins, validate_form

CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///make-change'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

###############
# Home Routes #
###############

@app.route("/")
def homepage():
    """Show homepage."""
    return render_template("index.html")

@app.route("/exchange", methods=["POST"])
def exchange_for_coins():
    """Run helper functions to determin currnecy, exchange for coins."""
    amount = request.form["currency"]

    data = count_coins(amount)

    flash(data)
    return redirect("/")

@app.route("/api/coins", methods={"POST"})
def add_new_coin():
    data = request.get_json()

    errors = validate_form(data)

    if len(errors) > 0:
        return json.dumps({'error': errors})
    else: 
        new_coin = Coins(name = data["name"], value = data["value"])
            
        db.session.add(new_coin)
        db.session.commit()

        return new_coin


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req