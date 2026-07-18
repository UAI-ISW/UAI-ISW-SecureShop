from flask import Flask
from controllers.tienda_controller import tienda_bp
from controllers.carrito_controller import carrito_bp
from controllers.mascota_controller import mascota_bp
from models.mascota import Mascota

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para session

# Registrar los blueprints
app.register_blueprint(tienda_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(mascota_bp)

# Inicializar la base de datos
Mascota.crear_tabla()

if __name__ == '__main__':
    app.run(debug=True, port=5003) 