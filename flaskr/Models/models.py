from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
from random import choices
import os

db = SQLAlchemy()


def app_config(app):
    # Setting up Database & app config
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('PROJECT_SECRET')
    db.app = app
    db.init_app(app)

    db.create_all()


# MODELS: TABLES

class ShortURL(db.Model):

    __tablename__ = 'ShortURL'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String)
    short_url = db.Column(db.String(5))
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, original_url, short_url=None):
        self.original_url = original_url
        if short_url:
            self.short_url = short_url
        else:
            self.short_url = self.generate_short_url()

    def generate_short_url(self):
        char = string.digits + string.ascii_letters
        short_link = ''.join(choices(char, k=5))

        url = self.query.filter_by(short_url=short_link).first()

        if url:
            return self.generate_short_url()

        return short_link

    def display(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'short_url': self.short_url,
            'date_created': self.date_created
        }

    def shortDisplay(self):
        return {
            'short_url': self.short_url
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()


