from flask import Blueprint, redirect, url_for, render_template, session
from models.producto import Producto
from models.carrito import Carrito

carrito_bp = Blueprint('carrito', __name__)

def get_carrito():
    if 'carrito' not in session:
        session['carrito'] = Carrito().to_dict()
    return Carrito()

@carrito_bp.route('/agregar/<int:producto_id>')
def agregar_producto(producto_id):
    carrito = get_carrito()
    productos = Producto.get_all()
    producto = next((p for p in productos if p.id == producto_id), None)
    if producto:
        carrito.agregar_producto(producto)
        session['carrito'] = carrito.to_dict()
    return redirect(url_for('tienda.tienda'))

@carrito_bp.route('/carrito')
def ver_carrito():
    carrito = get_carrito()
    return render_template('carrito.html', 
                         carrito=carrito.get_items(), 
                         total=carrito.get_total()) 