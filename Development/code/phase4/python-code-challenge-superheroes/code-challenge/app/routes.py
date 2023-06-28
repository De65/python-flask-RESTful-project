from flask import jsonify, request
from app import app, db
from models import Hero, Power, HeroPower

# Route handler for '/heroes' endpoint
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = []
    for hero in heroes:
        hero_list.append({
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        })
    return jsonify(hero_list)

# Route handler for '/heroes/<id>' endpoint
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
    powers = []
    for hero_power in hero.powers:
        powers.append({
            'id': hero_power.power.id,
            'name': hero_power.power.name,
            'description': hero_power.power.description
        })
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }
    return jsonify(hero_data)

# Route handler for '/powers' endpoint
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = []
    for power in powers:
        power_list.append({
            'id': power.id,
            'name': power.name,
            'description': power.description
        })
    return jsonify(power_list)

# Route handler for '/powers/<id>' endpoint
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404
    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(power_data)

# Route handler for '/powers/<id>' endpoint (PATCH request)
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    new_description = request.json.get('description')
    if not new_description or len(new_description) < 20:
        return jsonify({'errors': ['Invalid description']}), 400

    power.description = new_description
    db.session.commit()

    updated_power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(updated_power_data)

# Route handler for '/hero_powers' endpoint (POST request)
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    strength = request.json.get('strength')
    power_id = request.json.get('power_id')
    hero_id = request.json.get('hero_id')

    if not strength or not power_id or not hero_id:
        return jsonify({'errors': ['Missing data']}), 400

    power = Power.query.get(power_id)
    hero = Hero.query.get(hero_id)

    if power is None or hero is None:
        return jsonify({'errors': ['Invalid power or hero']}), 400

    hero_power = HeroPower(strength=strength, hero=hero, power=power)
    if not hero_power.validate():
        return jsonify({'errors': ['Invalid strength']}), 400

    db.session.add(hero_power)
    db.session.commit()

    return get_hero(hero_id)  # Assuming this is a helper function to retrieve the hero's data

# Additional route handlers can be defined here

