from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    super_name = db.Column(db.String(50))
    powers = db.relationship('HeroPower', backref='hero')

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    heroes = db.relationship('HeroPower', backref='power')

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(10))
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'))

    def validate(self):
        valid_strengths = ['Strong', 'Weak', 'Average']
        return self.strength in valid_strengths

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [
        {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name}
        for hero in heroes
    ]
    return jsonify(hero_list)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    powers = [
        {'id': hero_power.power.id, 'name': hero_power.power.name, 'description': hero_power.power.description}
        for hero_power in hero.powers
    ]
    hero_data = {'id': hero.id, 'name': hero.name, 'super_name': hero.super_name, 'powers': powers}
    return jsonify(hero_data)


if __name__ == '__main__':
    app.run(port=5555)

