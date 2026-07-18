from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('secure_shop.db')
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
    # Insertar usuario admin
    c.execute('INSERT OR IGNORE INTO usuarios (usuario, password) VALUES (?, ?)', 
             ('admin', 'colocolo'))
    conn.commit()
    conn.close()

@app.route('/registrar_mascota', methods=['POST'])
def registrar_mascota():
    data = request.json
    conn = sqlite3.connect('secure_shop.db')
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
    conn = sqlite3.connect('secure_shop.db')
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