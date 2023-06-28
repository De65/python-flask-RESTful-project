from app import db
from flask_sqlalchemy import Model
from app.models import HeroPower

class Hero(db.Model):
    __tablename__ = 'hero'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    power = db.relationship('app.models.HeroPower', backref='hero', uselist=False)
    
    __table_args__ = {'extend_existing': True}

    def __repr__(self):
        return f"<Hero id={self.id} name='{self.name}'>"


class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    heroes = db.relationship('HeroPower', backref='power')
    
    __table_args__ = {'extend_existing': True}
    
    def __repr__(self):
        return f"<Power id={self.id} name='{self.name}' description='{self.description}'>"


class HeroPower(db.Model):
    __tablename__ = 'heropower'
    id = db.Column(db.Integer, primary_key=True)
    power = db.Column(db.String(50))
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    
    __table_args__ = {'extend_existing': True}
    
    def __repr__(self):
        return f"<HeroPower id={self.id} strength='{self.strength}'>"

