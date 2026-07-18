from flask import Blueprint, request, render_template, jsonify
from models.mascota import Mascota

mascota_bp = Blueprint('mascota', __name__)

@mascota_bp.route('/inscribir', methods=['GET', 'POST'])
def inscribir_mascota():
    if request.method == 'POST':
        mascota = Mascota(
            nombre=request.form['nombre'],
            rut=request.form['rut'],
            chip=request.form['chip'],
            edad=request.form['edad'],
            color=request.form['color'],
            tipo=request.form['tipo']
        )
        mascota.guardar()
        return 'Mascota registrada exitosamente'
    return render_template('inscribir.html')

@mascota_bp.route('/mascotas', methods=['GET'])
def get_mascotas():
    mascotas = Mascota.get_all()
    return jsonify([mascota.to_dict() for mascota in mascotas]) 