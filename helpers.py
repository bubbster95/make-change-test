import json
from models import Coins
from sqlalchemy.sql import exists

def count_coins(amount):
    """If coin <= amount is true:
    Subtract the coins value from amount.
    Increment that coins count, rinse and repeat.
    If false: move to the next lowest coin in line"""

    coin_count = {}
    amount = float(amount)

    # order_by is to account for coins made by user.
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
    if int(data["value"]) <= 0 :
        errors["value"] = "This field is required and must be greater then 0."
    return errors