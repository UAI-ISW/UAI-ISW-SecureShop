from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests

app = Flask(__name__)

# Lista de productos de ejemplo
productos = [
    {'id': 1, 'nombre': 'Collar para perro', 'precio': 5000},
    {'id': 2, 'nombre': 'Correa retráctil', 'precio': 8000},
    {'id': 3, 'nombre': 'Plato de comida', 'precio': 3000},
    {'id': 4, 'nombre': 'Juguete para gato', 'precio': 4000},
]

# Carrito de compras
carrito = []

@app.route('/')
def tienda():
    return render_template('tienda.html', productos=productos)

@app.route('/agregar/<int:producto_id>')
def agregar_producto(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        carrito.append(producto)
    return redirect(url_for('tienda'))

@app.route('/carrito')
def ver_carrito():
    total = sum(producto['precio'] for producto in carrito)
    return render_template('carrito.html', carrito=carrito, total=total)

@app.route('/inscribir', methods=['GET', 'POST'])
def inscribir_mascota():
    if request.method == 'POST':
        datos_mascota = {
            'nombre': request.form['nombre'],
            'rut': request.form['rut'],
            'chip': request.form['chip'],
            'edad': request.form['edad'],
            'color': request.form['color'],
            'tipo': request.form['tipo']
        }
        
        # Enviar datos a la API
        response = requests.post('http://localhost:5001/registrar_mascota', 
                               json=datos_mascota)
        
        if response.status_code == 201:
            return 'Mascota registrada exitosamente'
        else:
            return 'Error al registrar la mascota'
            
    return render_template('inscribir.html')

if __name__ == '__main__':
    app.run(debug=True, port=5003) 