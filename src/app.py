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
from models import db, User, Personaje, Vehiculo, Lugar, Criatura, Droide, Organizacion, Especie, Favorito, TipoRecurso
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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

# USUARIOS


@app.route('/api/users', methods=['GET'])
def get_users():

    usuarios = db.session.execute(db.select(User)).scalars().all()

    if not usuarios:
        return jsonify([]), 200

    return jsonify([user.serialize() for user in usuarios]), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    usuario = db.session.get(User, user_id)

    if usuario is None:
        return jsonify({"msg": f"Usuario con ID {user_id} no encontrado"}), 404

    return jsonify(usuario.serialize()), 200


@app.route('/api/users', methods=['POST'])
def post_users():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nuevo_vehiculo = Vehiculo(
        email=data['email'],
        password=data['password'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        is_active=data['is_active'],
    )

    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return jsonify(nuevo_vehiculo.serialize()), 201

# PERSONAJES


@app.route('/api/personajes', methods=['GET'])
def get_personajes():

    personajes = db.session.execute(db.select(Personaje)).scalars().all()

    if not personajes:
        return jsonify([]), 200

    return jsonify([personaje.serialize() for personaje in personajes]), 200


@app.route('/api/personajes/<int:personaje_id>', methods=['GET'])
def get_personaje(personaje_id):
    personaje = db.session.get(Personaje, personaje_id)

    if personaje is None:
        return jsonify({"msg": f"Personaje con ID {personaje_id} no encontrado"}), 404

    return jsonify(personaje.serialize()), 200


@app.route('/api/personajes', methods=['POST'])
def post_personajes():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nuevo_personaje = Personaje(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nuevo_personaje)
    db.session.commit()
    return jsonify(nuevo_personaje.serialize()), 201

# VEHÍCULOS


@app.route('/api/vehiculos', methods=['GET'])
def get_vehiculos():

    vehiculos = db.session.execute(db.select(Vehiculo)).scalars().all()

    if not vehiculos:
        return jsonify([]), 200

    return jsonify([vehiculo.serialize() for vehiculo in vehiculos]), 200


@app.route('/api/vehiculos/<int:vehiculo_id>', methods=['GET'])
def get_vehiculo(vehiculo_id):
    vehiculo = db.session.get(Vehiculo, vehiculo_id)

    if vehiculo is None:
        return jsonify({"msg": f"Vehículo con ID {vehiculo_id} no encontrado"}), 404

    return jsonify(vehiculo.serialize()), 200


@app.route('/api/vehiculos', methods=['POST'])
def post_vehiculos():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nuevo_vehiculo = Vehiculo(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nuevo_vehiculo)
    db.session.commit()
    return jsonify(nuevo_vehiculo.serialize()), 201

# LUGARES


@app.route('/api/lugares', methods=['GET'])
def get_lugares():

    lugares = db.session.execute(db.select(Lugar)).scalars().all()

    if not lugares:
        return jsonify([]), 200

    return jsonify([lugar.serialize() for lugar in lugares]), 200


@app.route('/api/lugares/<int:lugar_id>', methods=['GET'])
def get_lugar(lugar_id):
    lugar = db.session.get(Lugar, lugar_id)

    if lugar is None:
        return jsonify({"msg": f"Lugar con ID {lugar_id} no encontrado"}), 404

    return jsonify(lugar.serialize()), 200


@app.route('/api/lugares', methods=['POST'])
def post_lugares():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nuevo_lugar = Lugar(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nuevo_lugar)
    db.session.commit()
    return jsonify(nuevo_lugar.serialize()), 201

# CRIATURAS


@app.route('/api/criaturas', methods=['GET'])
def get_criaturas():

    criaturas = db.session.execute(db.select(Criatura)).scalars().all()

    if not criaturas:
        return jsonify([]), 200

    return jsonify([criatura.serialize() for criatura in criaturas]), 200


@app.route('/api/criaturas/<int:criatura_id>', methods=['GET'])
def get_criatura(criatura_id):
    criatura = db.session.get(Criatura, criatura_id)

    if criatura is None:
        return jsonify({"msg": f"Criatura con ID {criatura_id} no encontrado"}), 404

    return jsonify(criatura.serialize()), 200


@app.route('/api/criaturas', methods=['POST'])
def post_criaturas():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nueva_criatura = Criatura(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nueva_criatura)
    db.session.commit()
    return jsonify(nueva_criatura.serialize()), 201

# DROIDES


@app.route('/api/droides', methods=['GET'])
def get_droides():

    droides = db.session.execute(db.select(Droide)).scalars().all()

    if not droides:
        return jsonify([]), 200

    return jsonify([droide.serialize() for droide in droides]), 200


@app.route('/api/droides/<int:droide_id>', methods=['GET'])
def get_droide(droide_id):
    droide = db.session.get(Droide, droide_id)

    if droide is None:
        return jsonify({"msg": f"Droide con ID {droide_id} no encontrado"}), 404

    return jsonify(droide.serialize()), 200


@app.route('/api/droides', methods=['POST'])
def post_droides():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nuevo_droide = Droide(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nuevo_droide)
    db.session.commit()
    return jsonify(nuevo_droide.serialize()), 201

# ORGANIZACIONES


@app.route('/api/organizaciones', methods=['GET'])
def get_organizaciones():

    organizaciones = db.session.execute(
        db.select(Organizacion)).scalars().all()

    if not organizaciones:
        return jsonify([]), 200

    return jsonify([organizacion.serialize() for organizacion in organizaciones]), 200


@app.route('/api/organizaciones/<int:organizacion_id>', methods=['GET'])
def get_organizacion(organizacion_id):
    organizacion = db.session.get(Organizacion, organizacion_id)

    if organizacion is None:
        return jsonify({"msg": f"Organización con ID {organizacion_id} no encontrada"}), 404

    return jsonify(organizacion.serialize()), 200


@app.route('/api/organizaciones', methods=['POST'])
def post_organizaciones():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nueva_organizacion = Organizacion(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nueva_organizacion)
    db.session.commit()
    return jsonify(nueva_organizacion.serialize()), 201

# ESPECIES


@app.route('/api/especies', methods=['GET'])
def get_especies():

    especies = db.session.execute(
        db.select(Especie)).scalars().all()

    if not especies:
        return jsonify([]), 200

    return jsonify([especie.serialize() for especie in especies]), 200


@app.route('/api/especies/<int:especie_id>', methods=['GET'])
def get_especie(especie_id):
    especie = db.session.get(Especie, especie_id)

    if especie is None:
        return jsonify({"msg": f"Especie con ID {especie_id} no encontrada"}), 404

    return jsonify(especie.serialize()), 200


@app.route('/api/especies', methods=['POST'])
def post_especies():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON data'}), 400

    nueva_especie = Especie(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nueva_especie)
    db.session.commit()
    return jsonify(nueva_especie.serialize()), 201

# FAVORITOS


@app.route('/api/favoritos/personajes/<int:personaje_id>', methods=['POST'])
def post_personaje_favorito(personaje_id):
    user_id = 1

    personaje = db.session.get(Personaje, personaje_id)
    if not personaje:
        return jsonify({'msg': f'El personaje con ID {personaje_id} no existe'}), 404

    existe = db.session.execute(db.select(Favorito).filter_by(
        user_id=user_id,
        recurso_id=personaje_id,
        tipo=TipoRecurso.PERSONAJE
    )).scalar()

    if existe:
        return jsonify({'msg': "Este personaje ya están en favoritos para este usuario"}), 400

    nuevo_favorito = Favorito(
        user_id=user_id,
        recurso_id=personaje_id,
        tipo=TipoRecurso.PERSONAJE
    )

    db.session.add(nuevo_favorito)
    db.session.commit()
    return jsonify(nuevo_favorito.serialize()), 201


@app.route('/api/favoritos/<int:favorito_id>', methods=['DELETE'])
def delete_favorito(favorito_id):
    favorito = db.session.get(Favorito, favorito_id)

    if not favorito:
        return jsonify({'msg': f"El favorito con ID {favorito_id} no existe"}), 404

    db.session.delete(favorito)
    db.session.commit()

    return jsonify({
        "msg": 'Favorito eliminado con éxito',
        "id_favorito_eliminado": favorito_id
    }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
