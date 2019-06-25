from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from app import db

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })


class Countries(BaseModel, db.Model):
    """Model for the countries table"""
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key = True)
    iso_a3 = db.Column(db.String())
    names = db.Column(JSON)
    data = db.Column(JSON)