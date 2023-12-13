"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, People, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = map(lambda user: user.serialize(), all_users)
    user_list = list(results)
    return jsonify(user_list), 200

#get list of planets 

@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planet.query.all()
    results = map(lambda planet: planet.serialize(), all_planets)
    planet_list = list(results)
    return jsonify(planet_list), 200

# get single planet 

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)

    if not planet:
        return jsonify({"error": "Planet not found"}), 404

    return jsonify(planet.serialize()), 200

#get list of people

@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all()
    results = map(lambda people: people.serialize(), all_people)
    people_list = list(results)
    return jsonify(people_list), 200

# get single people

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)

    if not person:
        return jsonify({"error": "Person not found"}), 404

    return jsonify(person.serialize()), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
