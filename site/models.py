from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Countries(db.Model):
    """Model for the countries table"""
    __tablename__ = 'countries3'

    id = db.Column(db.Integer, primary_key = True)
    iso_a3 = db.Column(db.String())
    country_name = db.Column(db.String())
    indicator_code = db.Column(db.String())
    year = db.Column(db.Integer)
    value = db.Column(db.String())
