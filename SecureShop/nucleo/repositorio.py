"""Tablas de usuarios y mascotas.

Las consultas usan `?`. Eso se miró y no es inyección.
La API que llama a este repositorio no pide sesión: eso sí se conserva.
"""
import sqlite3
from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash


class Repositorio:
    def __init__(self, db_path):
        self.db_path = db_path

    def _conexion(self):
        return sqlite3.connect(self.db_path)

    def asegurar_esquema(self, admin_user, admin_password):
        conn = self._conexion()
        c = conn.cursor()
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
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # La tabla no tiene columna de rol. Quien pasa el login queda admin en la sesión.
        c.execute(
            '''INSERT INTO usuarios (usuario, password) VALUES (?, ?)
               ON CONFLICT(usuario) DO UPDATE SET password = excluded.password''',
            (admin_user, generate_password_hash(admin_password)))
        conn.commit()
        conn.close()

    def clave_correcta(self, usuario, password):
        conn = self._conexion()
        c = conn.cursor()
        c.execute('SELECT password FROM usuarios WHERE usuario = ?', (usuario,))
        row = c.fetchone()
        conn.close()
        return bool(row and check_password_hash(row[0], password))

    def registrar(self, data):
        # Sin validar RUT, edad ni chip. Si falta un campo, revienta (sigue así).
        conn = self._conexion()
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
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        ))
        conn.commit()
        conn.close()

    def listar(self):
        conn = self._conexion()
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
                'fecha_registro': row[7],
            }
            for row in c.fetchall()
        ]
        conn.close()
        return mascotas
