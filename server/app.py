from flask import jsonify, request
from app import app, db
from models import Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Route to retrieve all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    serialized_heroes = [hero.serialize() for hero in heroes]
    return jsonify(serialized_heroes), 200

# Route to retrieve a specific hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({'error': 'Hero not found'}), 404
    return jsonify(hero.serialize()), 200

# Route to retrieve all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    serialized_powers = [power.serialize() for power in [powers]]
    return jsonify(powers), 200

# Route to retrieve a specific power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({'error': 'Power not found'}), 404
    return jsonify(power.serialize()), 200

# Route to create a hero_power relationship
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')

    if not all([hero_id, power_id, strength]):
        return jsonify({'error': 'Missing data'}), 400

    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({'error': 'Invalid strength'}), 400

    hero = Hero.query.get_or_404(hero_id)
    power = Power.query.get_or_404(power_id)

    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.serialize()), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)