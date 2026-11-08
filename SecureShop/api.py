import os

from flask import Flask, jsonify, request
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


def init_db():
    repo.asegurar_esquema(ADMIN_USER, ADMIN_PASSWORD)


@app.route('/registrar_mascota', methods=['POST'])
def registrar_mascota():
    # No pregunta quién llama. Hallazgo A01.
    repo.registrar(request.json)
    return jsonify({'message': 'Mascota registrada'}), 201


@app.route('/mascotas', methods=['GET'])
def get_mascotas():
    # El JSON trae RUT y chip, sin sesión. Hallazgo A01 / CWE-200.
    return jsonify(repo.listar())


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
