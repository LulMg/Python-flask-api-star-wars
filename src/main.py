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
from models import db, User, People, Planets, Fav_people, Fav_planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

#AQUI VAMOS A CREAR NUESTRAS RUTAS
@app.route('/people', methods=['GET'])
def get_people():
    all_people = People.query.all() #se retorna un arreglo de clases
    all_people = list(map(lambda elem: elem.serialize(), all_people)) #itero c/u de las clases y almaceno el resultado en all_people
    print(all_people)
    return jsonify({'resultado': all_people})

@app.route('/planets', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all() #se retorna un arreglo de clases
    all_planets = list(map(lambda elem: elem.serialize(), all_planets)) #itero c/u de las clases y almaceno el resultado en all_people
    print(all_planets)
    return jsonify({'resultado': all_planets})

@app.route('/user', methods=['GET'])
def get_user():
    all_users = User.query.all() #se retorna un arreglo de clases
    all_users = list(map(lambda elem: elem.serialize(), all_users)) #itero c/u de las clases y almaceno el resultado en all_people
    print(all_users)
    return jsonify({'resultado': all_users})

@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    #bajo un parametro especifico
    #get_one_people = People.query.filter_by(id=id).first() #se retorna un arreglo de clases.. con first te devuelve el primer valor, si los queremos todos ponemos el .all
    #buscar solo por el id
    get_one_people = People.query.get(id).serialize()
    return jsonify({'resultado': get_one_people})

@app.route('/planets/<int:id>', methods=['GET'])
def get_one_planet(id):
    #bajo un parametro especifico
    #get_one_people = People.query.filter_by(id=id).first() #se retorna un arreglo de clases.. con first te devuelve el primer valor, si los queremos todos ponemos el .all
    #buscar solo por el id
    get_one_planet = Planets.query.get(id)
    if get_one_planet:
        return jsonify({'resultado': get_one_planet.serialize()})
    else:
        return jsonify({'resultado': 'resultado no existe'})

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_fav_people(people_id):
    onepeople = People.query.get(people_id)
    if onepeople:
        new = Fav_people()
        new.user_id = 1
        new.people_id = people_id
        db.session.add(new) #agrego el registro a la base de datos
        db.session.commit() #voy a guardar los cambios realixados

        return jsonify({'resultado': 'todo salio bien'})
    else:
        return jsonify({'resultado': 'personaje no existe'})

@app.route('/favorite/planets/<int:planet_id>', methods=['POST'])
def add_fav_planet(planet_id):
    oneplanet = Planets.query.get(planet_id)
    if oneplanet:
        new = Fav_planets()
        new.user_id = 1
        new.planet_id = planet_id
        db.session.add(new) #agrego el registro a la base de datos
        db.session.commit() #voy a guardar los cambios realixados

        return jsonify({'resultado': 'todo salio bien'})
    else:
        return jsonify({'resultado': 'personaje no existe'})

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def del_fav_planet(planet_id):
    all_planets = Planets.query.all()
    del_oneplanet = Fav_planets.query.get(planet_id)
    if del_oneplanet:

        db.session.delete(del_oneplanet)
        db.session.commit()
        return jsonify({'resultado': 'todo salio bien'})
    else:
        return jsonify({'resultado': 'planeta no existe'})

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def del_fav_people(people_id):
    del_onepeople = Fav_people.query.filter_by(id = people_id).first()
    print(del_onepeople)
    if del_onepeople:

        db.session.delete(del_onepeople)
        db.session.commit()
        return jsonify({'resultado': 'todo salio bien'})
    else:
        return jsonify({'resultado': 'personaje no existe'})

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
