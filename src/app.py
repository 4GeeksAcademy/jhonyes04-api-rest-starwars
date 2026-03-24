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
    return jsonify([user.serialize() for user in usuarios]), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    usuario = db.session.get(User, user_id)

    if not usuario:
        return jsonify({"msg": f"Usuario con ID {user_id} no encontrado"}), 404

    return jsonify(usuario.serialize()), 200


@app.route('/api/users', methods=['POST'])
def post_users():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No ha proporcionado un JSON'}), 400

    nuevo_usuario = User(
        email=data['email'],
        password=data['password'],
        firstname=data['firstname'],
        lastname=data['lastname'],
        is_active=data['is_active'],
    )

    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify(nuevo_usuario.serialize()), 201


@app.route('/api/users/favoritos', methods=['GET'])
def get_users_favoritos():
    user_id = 1
    usuario = db.session.get(User, user_id)

    if not usuario:
        return jsonify({'msg': 'Usuario no encontrado'}), 404

    return jsonify(usuario.serialize()), 200


# RECURSOS
MODEL_MAP = {
    'personajes':
    {'model': Personaje, "tipo": TipoRecurso.PERSONAJE},
    'vehiculos':
    {'model': Vehiculo, "tipo": TipoRecurso.VEHICULO},
    'lugares':
    {'model': Lugar, "tipo": TipoRecurso.LUGAR},
    'criaturas':
    {'model': Criatura, "tipo": TipoRecurso.CRIATURA},
    'droides':
    {'model': Droide, "tipo": TipoRecurso.DROIDE},
    'organizaciones':
    {'model': Organizacion,
     "tipo": TipoRecurso.ORGANIZACION},
    'especies':
    {'model': Especie, "tipo": TipoRecurso.ESPECIE},
}


@app.route('/api/<string:tipo_recurso>', methods=['GET'])
def get_recursos(tipo_recurso):
    if tipo_recurso not in MODEL_MAP:
        return jsonify({'msg': f"El recurso '{tipo_recurso}' no es válido"}), 404

    model = MODEL_MAP[tipo_recurso]["model"]
    items = db.session.execute(db.select(model)).scalars().all()

    return jsonify([item.serialize() for item in items]), 200


@app.route('/api/<string:tipo_recurso>/<int:item_id>', methods=['GET'])
def get_recursos_id(tipo_recurso, item_id):
    if tipo_recurso not in MODEL_MAP:
        return jsonify({'msg': "Recurso no válido"}), 404

    model = MODEL_MAP[tipo_recurso]['model']
    item = db.session.get(model, item_id)

    if not item:
        return jsonify({'msg': f"ID {item_id} no encontrado en {tipo_recurso}"}), 404

    return jsonify(item.serialize()), 200


@app.route('/api/<string:tipo_recurso>', methods=['POST'])
def post_recurso(tipo_recurso):
    if tipo_recurso not in MODEL_MAP:
        return jsonify({'msg': 'Recurso no válido'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'msg': 'Todos los campos son obligatorios'}), 400

    model = MODEL_MAP[tipo_recurso]['model']
    nuevo_item = model(
        name=data['name'],
        description=data['description'],
        image=data['image']
    )

    db.session.add(nuevo_item)
    db.session.commit()
    return jsonify(nuevo_item.serialize()), 201


@app.route('/api/<string:tipo_recurso>/<int:item_id>', methods=['PUT'])
def put_recurso(tipo_recurso, item_id):
    if tipo_recurso not in MODEL_MAP:
        return jsonify({'msg': f'El recurso {tipo_recurso} no es válido'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'msg': 'JSON no proporcionado'}), 400

    model = MODEL_MAP[tipo_recurso]['model']

    item = db.session.get(model, item_id)

    if not item:
        return jsonify({'msg': f"No se encontró {tipo_recurso[:-1]} con ID {item_id}"}), 404

    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.image = data.get('image', item.image)

    db.session.commit()
    return jsonify(item.serialize()), 201


@app.route('/api/<string:tipo_recurso>/<int:item_id>', methods=['DELETE'])
def delete_recurso(tipo_recurso, item_id):
    if tipo_recurso not in MODEL_MAP:
        return jsonify({'msg': f'El recurso {tipo_recurso} no es válido'}), 404

    model = MODEL_MAP[tipo_recurso]['model']

    item = db.session.get(model, item_id)

    if not item:
        return jsonify({'msg': f'No se encontró {tipo_recurso[:-1]} con ID {item_id}'}), 404

    db.session.delete(item)
    db.session.commit()

    return jsonify({'msg': f'{tipo_recurso[:-1].capitalize()} eliminado correctamente', "id_eliminado": item_id}), 200

# FAVORITOS


@app.route('/api/favoritos/<string:tipo_recurso>/<int:item_id>', methods=['POST'])
def post_favoritos(tipo_recurso, item_id):
    if tipo_recurso not in MODEL_MAP:
        return jsonify({'msg': 'Recurso no válido'}), 404

    user_id = 1
    model = MODEL_MAP[tipo_recurso]

    if not db.session.get(model['model'], item_id):
        return jsonify({'msg': f'El {tipo_recurso} con ID {item_id} no existe'}), 404

    existe = db.session.execute(db.select(Favorito).filter_by(
        user_id=user_id,
        recurso_id=item_id,
        tipo=model['tipo']
    )).scalar()

    if existe:
        return jsonify({'msg': 'Ya está en favoritos'}), 400

    nuevo_favorito = Favorito(
        user_id=user_id, recurso_id=item_id, tipo=model['tipo'])
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
