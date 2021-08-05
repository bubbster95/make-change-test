import json
from models import Coins

def count_coins(amount):
    """Make change by subtracting largest coin possible from amount."""

    coin_count = {}
    amount = float(amount)

    # order_by() accounts for coins added by user.
    coins = Coins.query.order_by(Coins.value.desc()).all()

    for coin in coins:
        coin_value = float(coin.value)
        coin_count[coin.name] = 0

        while coin_value <= amount:
            coin_count[coin.name] += 1
            amount -= coin_value
            amount = round(amount, 2)

    return json.dumps(coin_count)


def validate_form(data):
    errors = {}

    if bool(Coins.query.filter_by(name=data['name']).first()):
        errors["name"] = "This name already exists."
    if len(data["name"]) <= 0:
        errors["name"] = "This field is required."
    if float(data["value"]) <= 0:
        errors["value"] = "This field is required and must be greater then 0."
    return errors

def generate_response(data):
    resp = {
    "name": data["name"],
    "value": data["value"]
    }

    return resp