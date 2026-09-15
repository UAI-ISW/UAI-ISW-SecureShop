import os
import sqlite3
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash

# Sprint 1 · chore (H2): configuración desde variables de entorno.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:  # dotenv es opcional; en CI/env las vars ya vienen del entorno
    pass

DB_PATH = os.environ.get('SECURE_SHOP_DB', 'secure_shop.db')
ADMIN_USER = os.environ.get('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'colocolo')

app = Flask(__name__)
CORS(app)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Crear tabla de mascotas
    c.execute('''
        CREATE TABLE IF NOT EXISTS mascotas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            rut TEXT NOT NULL,
            chip TEXT,
            edad TEXT,
            color TEXT,
            tipo TEXT,
            fecha_registro TIMESTAMP
        )
    ''')
    # Crear tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Insertar/actualizar admin con contraseña HASHEADA (US-01, corrige H1).
    # El upsert re-hashea también bases heredadas que traían texto plano.
    c.execute(
        '''INSERT INTO usuarios (usuario, password) VALUES (?, ?)
           ON CONFLICT(usuario) DO UPDATE SET password = excluded.password''',
        (ADMIN_USER, generate_password_hash(ADMIN_PASSWORD)))
    conn.commit()
    conn.close()


@app.route('/registrar_mascota', methods=['POST'])
def registrar_mascota():
    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO mascotas (nombre, rut, chip, edad, color, tipo, fecha_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['nombre'],
        data['rut'],
        data['chip'],
        data['edad'],
        data['color'],
        data['tipo'],
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Mascota registrada'}), 201


@app.route('/mascotas', methods=['GET'])
def get_mascotas():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM mascotas')
    mascotas = [
        {
            'id': row[0],
            'nombre': row[1],
            'rut': row[2],
            'chip': row[3],
            'edad': row[4],
            'color': row[5],
            'tipo': row[6],
            'fecha_registro': row[7]
        }
        for row in c.fetchall()
    ]
    conn.close()
    return jsonify(mascotas)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)
