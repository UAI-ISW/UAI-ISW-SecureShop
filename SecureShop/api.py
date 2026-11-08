import os

from flask import Flask, Response, jsonify, request
from flask_cors import CORS

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from nucleo.repositorio import Repositorio

DB_PATH = os.environ.get('SECURE_SHOP_DB', 'secure_shop.db')
# Valor de relleno en el fuente. Hallazgo A04 / CWE-798. No se saca en este corte.
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'colocolo')

app = Flask(__name__)
# Cualquier origen puede llamar. Se conserva.
CORS(app)

repo = Repositorio(DB_PATH)

MAX_IMAGEN = 2 * 1024 * 1024
TIPOS_IMAGEN = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}


def init_db():
    repo.asegurar_esquema(ADMIN_USER, ADMIN_PASSWORD)


def _imagen_del_pedido():
    archivo = request.files.get('imagen')
    if not archivo or not archivo.filename:
        return None, None, False
    blob = archivo.read(MAX_IMAGEN + 1)
    tipo = (archivo.mimetype or '').split(';')[0].strip().lower()
    if not blob or len(blob) > MAX_IMAGEN or tipo not in TIPOS_IMAGEN:
        return None, None, True
    return blob, tipo, False


@app.route('/registrar_mascota', methods=['POST'])
def registrar_mascota():
    # No pregunta quién llama. Hallazgo A01.
    if request.is_json:
        datos = request.json
        imagen, imagen_tipo, rechazada = None, None, False
    else:
        datos = request.form.to_dict()
        imagen, imagen_tipo, rechazada = _imagen_del_pedido()
    repo.registrar(datos, imagen, imagen_tipo)
    return jsonify({
        'message': 'Mascota registrada',
        'imagen_guardada': imagen is not None,
        'imagen_rechazada': rechazada,
    }), 201


@app.route('/mascotas', methods=['GET'])
def get_mascotas():
    # El JSON trae RUT y chip, sin sesión. Hallazgo A01 / CWE-200.
    # La foto no viaja en este JSON: se pide por id.
    return jsonify(repo.listar())


@app.route('/mascotas/<int:mascota_id>/imagen', methods=['GET'])
def get_imagen(mascota_id):
    # Sin sesión, igual que el listado. Hallazgo A01.
    encontrada = repo.leer_imagen(mascota_id)
    if not encontrada:
        return '', 404
    datos, tipo = encontrada
    return Response(datos, mimetype=tipo)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
