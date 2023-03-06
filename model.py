# pylint: disable=no-member

"""Module's docstring"""


from datetime import date as dt

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()


class Account(db.Model):  # pylint: disable=too-few-public-methods

    """Class Account docstring

    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    #address = db.Column(db.String(200))
    #phone_number = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        """function's docstring"""
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """function's docstring"""
        self.password_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        """function's docstring"""
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_authenticated(self):
        """function's docstring"""
        return "" != self.email and self.email is not None

    def is_anonymous(self):
        """function's docstring"""
        return not self.is_authenticated()


class Delivery(db.Model):  # pylint: disable=too-few-public-methods
    """Class Delivery docstring

    """
    __tablename__ = "delivery"

    order_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), nullable=False, unique=True)
    product = db.Column(db.String(60), nullable=False)
    date = db.Column(db.Date, nullable=False, default=dt.today())
    special_instructions = db.Column(db.String(1000))
