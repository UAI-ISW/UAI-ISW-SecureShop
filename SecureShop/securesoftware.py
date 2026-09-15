import os
import sqlite3
from datetime import timedelta

import requests
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash

# Sprint 1 · chore (H2): configuración desde variables de entorno.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_PATH = os.environ.get('SECURE_SHOP_DB', 'secure_shop.db')
API_URL = os.environ.get('API_URL', 'http://localhost:5001')

app = Flask(__name__)
# La clave de sesión ya no vive en el código (H2).
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')
# La sesión expira (US-01): no queda abierta para siempre.
app.permanent_session_lifetime = timedelta(hours=1)


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT password FROM usuarios WHERE usuario = ?', (usuario,))
        row = c.fetchone()
        conn.close()

        # US-01: verificación contra el hash + creación de sesión real.
        if row and check_password_hash(row[0], password):
            session.permanent = True
            session['usuario'] = usuario
            session['rol'] = 'admin'
            return redirect(url_for('estadisticas'))
        else:
            return 'Credenciales incorrectas'
    return render_template('login.html')


@app.route('/estadisticas')
def estadisticas():
    response = requests.get(f'{API_URL}/mascotas')
    mascotas = response.json()
    return render_template('estadisticas.html', mascotas=mascotas)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
