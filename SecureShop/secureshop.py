import os
from datetime import timedelta
from functools import wraps

import requests
from flask import Flask, Response, flash, redirect, render_template, request, session, url_for

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from nucleo.carrito import carrito_del_proceso
from nucleo.catalogo import CATALOGO, buscar
from nucleo.pago import StubWebpay, pagar_carrito
from nucleo.repositorio import Repositorio

DB_PATH = os.environ.get('SECURE_SHOP_DB', 'secure_shop.db')
API_URL = os.environ.get('API_URL', 'http://localhost:5001')

app = Flask(__name__)
# Valor de relleno en el fuente. Hallazgo A04 / CWE-798.
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-change-me')
app.permanent_session_lifetime = timedelta(hours=1)

carrito = carrito_del_proceso
repo = Repositorio(DB_PATH)
# La presentación depende de la interfaz. Hoy la implementación conectada es el stub.
pasarela = StubWebpay()


def login_required(rol=None):
    def decorador(vista):
        @wraps(vista)
        def envoltura(*args, **kwargs):
            if 'usuario' not in session:
                return redirect(url_for('login'))
            if rol is not None and session.get('rol') != rol:
                return redirect(url_for('login'))
            return vista(*args, **kwargs)
        return envoltura
    return decorador


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('usuario'):
        return redirect(url_for('tienda'))

    error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        if repo.clave_correcta(usuario, password):
            session.permanent = True
            session['usuario'] = usuario
            # No hay columna de rol. Quien entra queda admin. Hallazgo A07.
            session['rol'] = 'admin'
            return redirect(url_for('tienda'))
        error = 'Credenciales incorrectas'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_required()
def tienda():
    return render_template('tienda.html', productos=CATALOGO)


@app.route('/agregar/<int:producto_id>')
@login_required()
def agregar_producto(producto_id):
    producto = buscar(producto_id)
    if producto:
        carrito.agregar(producto)
    return redirect(url_for('ver_carrito'))


@app.route('/carrito')
@login_required()
def ver_carrito():
    return render_template('carrito.html', carrito=carrito, total=carrito.total())


@app.route('/comprar', methods=['POST'])
@login_required()
def comprar():
    if not carrito:
        flash('El carrito está vacío.')
        return redirect(url_for('ver_carrito'))
    resultado = pagar_carrito(carrito, pasarela)
    if not resultado.aprobado:
        flash(resultado.mensaje)
        return redirect(url_for('ver_carrito'))
    flash('Compra registrada. ' + resultado.mensaje)
    return redirect(url_for('tienda'))


@app.route('/inscribir', methods=['GET', 'POST'])
@login_required()
def inscribir_mascota():
    if request.method == 'POST':
        datos = {
            'nombre': request.form['nombre'],
            'rut': request.form['rut'],
            'chip': request.form['chip'],
            'edad': request.form['edad'],
            'color': request.form['color'],
            'tipo': request.form['tipo'],
        }
        archivo = request.files.get('imagen')
        files = None
        if archivo and archivo.filename:
            files = {
                'imagen': (
                    archivo.filename,
                    archivo.read(),
                    archivo.mimetype or 'application/octet-stream',
                ),
            }
        try:
            response = requests.post(
                f'{API_URL}/registrar_mascota', data=datos, files=files, timeout=10,
            )
        except requests.RequestException:
            flash('No pude hablar con la API (puerto 5001).')
            return render_template('inscribir.html')

        if response.status_code == 201:
            # No queda un log de quién inscribió. Hallazgo A09.
            flash('Mascota registrada.')
            cuerpo = response.json() if response.content else {}
            if files and not cuerpo.get('imagen_guardada'):
                flash('La foto no se guardó. Sirve jpg, png, gif o webp, hasta 2 MB.')
            return redirect(url_for('estadisticas'))
        flash('No se pudo registrar la mascota.')

    return render_template('inscribir.html')


@app.route('/estadisticas')
@login_required(rol='admin')
def estadisticas():
    mascotas = []
    try:
        response = requests.get(f'{API_URL}/mascotas', timeout=3)
        response.raise_for_status()
        mascotas = response.json()
    except requests.RequestException:
        flash('No pude leer las mascotas. ¿Está la API en el puerto 5001?')
    return render_template('estadisticas.html', mascotas=mascotas)


@app.route('/mascota/<int:mascota_id>/imagen')
@login_required()
def imagen_mascota(mascota_id):
    try:
        response = requests.get(f'{API_URL}/mascotas/{mascota_id}/imagen', timeout=5)
    except requests.RequestException:
        return '', 404
    if response.status_code != 200:
        return '', 404
    tipo = response.headers.get('Content-Type', 'application/octet-stream')
    return Response(response.content, mimetype=tipo)


if __name__ == '__main__':
    app.run(debug=True, port=5002)
