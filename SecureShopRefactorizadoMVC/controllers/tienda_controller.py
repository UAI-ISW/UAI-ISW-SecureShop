from flask import Blueprint, render_template
from models.producto import Producto

tienda_bp = Blueprint('tienda', __name__)

@tienda_bp.route('/')
def tienda():
    productos = Producto.get_all()
    return render_template('tienda.html', productos=productos) 