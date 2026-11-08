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
                fecha_registro TIMESTAMP,
                imagen BLOB,
                imagen_tipo TEXT
            )
        ''')
        columnas = {fila[1] for fila in c.execute('PRAGMA table_info(mascotas)')}
        if 'imagen' not in columnas:
            c.execute('ALTER TABLE mascotas ADD COLUMN imagen BLOB')
        if 'imagen_tipo' not in columnas:
            c.execute('ALTER TABLE mascotas ADD COLUMN imagen_tipo TEXT')
        c.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        # La tabla no tiene columna de rol. Quien pasa el login queda admin en la sesión.
        # pbkdf2 con salt aleatorio. En la fila queda method$salt$hash, nunca la clave.
        clave = generate_password_hash(admin_password, method='pbkdf2:sha256')
        c.execute(
            '''INSERT INTO usuarios (usuario, password) VALUES (?, ?)
               ON CONFLICT(usuario) DO UPDATE SET password = excluded.password''',
            (admin_user, clave))
        conn.commit()
        conn.close()

    def clave_correcta(self, usuario, password):
        conn = self._conexion()
        c = conn.cursor()
        c.execute('SELECT password FROM usuarios WHERE usuario = ?', (usuario,))
        row = c.fetchone()
        conn.close()
        return bool(row and check_password_hash(row[0], password))

    def registrar(self, data, imagen=None, imagen_tipo=None):
        # Sin validar RUT, edad ni chip. Si falta un campo, revienta (sigue así).
        # La foto es opcional. Si viene, queda en esta misma base.
        conn = self._conexion()
        c = conn.cursor()
        c.execute('''
            INSERT INTO mascotas (
                nombre, rut, chip, edad, color, tipo, fecha_registro, imagen, imagen_tipo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['nombre'],
            data['rut'],
            data['chip'],
            data['edad'],
            data['color'],
            data['tipo'],
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            imagen,
            imagen_tipo if imagen else None,
        ))
        conn.commit()
        conn.close()

    def listar(self):
        conn = self._conexion()
        c = conn.cursor()
        c.execute('''
            SELECT id, nombre, rut, chip, edad, color, tipo, fecha_registro,
                   CASE WHEN imagen IS NOT NULL THEN 1 ELSE 0 END
            FROM mascotas
        ''')
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
                'tiene_imagen': bool(row[8]),
            }
            for row in c.fetchall()
        ]
        conn.close()
        return mascotas

    def leer_imagen(self, mascota_id):
        conn = self._conexion()
        c = conn.cursor()
        c.execute(
            'SELECT imagen, imagen_tipo FROM mascotas WHERE id = ?',
            (mascota_id,),
        )
        row = c.fetchone()
        conn.close()
        if not row or row[0] is None:
            return None
        return row[0], row[1] or 'application/octet-stream'
