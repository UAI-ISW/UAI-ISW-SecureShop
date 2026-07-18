from datetime import datetime
import sqlite3

class Mascota:
    def __init__(self, nombre, rut, chip, edad, color, tipo, id=None, fecha_registro=None):
        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.chip = chip
        self.edad = edad
        self.color = color
        self.tipo = tipo
        self.fecha_registro = fecha_registro or datetime.now()

    @staticmethod
    def crear_tabla():
        conn = sqlite3.connect('secure_shop.db')
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
        conn.commit()
        conn.close()

    def guardar(self):
        conn = sqlite3.connect('secure_shop.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO mascotas (nombre, rut, chip, edad, color, tipo, fecha_registro)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.nombre,
            self.rut,
            self.chip,
            self.edad,
            self.color,
            self.tipo,
            self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        self.id = c.lastrowid
        conn.close()

    @staticmethod
    def get_all():
        conn = sqlite3.connect('secure_shop.db')
        c = conn.cursor()
        c.execute('SELECT * FROM mascotas')
        mascotas = []
        for row in c.fetchall():
            mascota = Mascota(
                id=row[0],
                nombre=row[1],
                rut=row[2],
                chip=row[3],
                edad=row[4],
                color=row[5],
                tipo=row[6],
                fecha_registro=datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S')
            )
            mascotas.append(mascota)
        conn.close()
        return mascotas

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rut': self.rut,
            'chip': self.chip,
            'edad': self.edad,
            'color': self.color,
            'tipo': self.tipo,
            'fecha_registro': self.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        } 