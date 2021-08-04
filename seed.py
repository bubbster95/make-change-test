"""Seed database with default coins data"""
from app import db
from models import Coins


db.drop_all()
db.create_all()

Coins.query.delete()

silver = Coins(name = "silver-dollar", value = 1.00)
half = Coins(name = "half-dollar", value = .50)
quarter = Coins(name = "quarter", value = .25)
dime = Coins(name = "dime", value = .10)
nickle = Coins(name = "nickle", value = .05)
penny = Coins(name = "penny", value = .01)


db.session.add_all([
    silver,
    half,
    quarter,
    dime,
    nickle,
    penny
])

db.session.commit()