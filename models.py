"""SQLAlchemy model for coins and their value."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Coins(db.Model):
    """Information about each coin.
    A bit overkill for this prompt."""

    __tablename__ = 'coins'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    value = db.Column(
        db.Float,
        nullable=False,
    )

    ## If I have time, add a feature to give coins a photo
    # image_url = db.Column(
    #     db.Text,
    #     default="https://images"
    # )


    def __repr__(self):
        return f"<Coin #{self.id}: {self.name}, {self.value}>"

def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)
