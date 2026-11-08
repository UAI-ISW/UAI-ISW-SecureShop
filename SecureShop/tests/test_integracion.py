"""Integración bottom-up. Cada nivel junta lo que el nivel de abajo ya probó.

1. Carrito con un Producto del catálogo. Repositorio con el archivo sqlite.
2. Carrito con StubWebpay, por la interfaz PasarelaPago.
3. La API HTTP con el Repositorio.
La presentación (secureshop.py) se prueba encima, en test_acceptance.py.
"""
from io import BytesIO

from nucleo.carrito import Carrito
from nucleo.catalogo import buscar
from nucleo.pago import StubWebpay, pagar_carrito
from nucleo.repositorio import Repositorio

MASCOTA = {
    'nombre': 'Luna', 'rut': '11.111.111-1', 'chip': 'CHIP-TEST',
    'edad': '2', 'color': 'blanco', 'tipo': 'Gato',
}


def test_nivel1_carrito_suma_productos_del_catalogo():
    carrito = Carrito()
    carrito.agregar(buscar(1))
    carrito.agregar(buscar(3))
    assert carrito.total() == 8000


def test_nivel1_la_foto_sigue_al_abrir_el_mismo_archivo(tmp_path):
    db = tmp_path / 'shop.db'
    png = b'\x89PNG\r\n\x1a\n' + b'foto'
    repo = Repositorio(str(db))
    repo.asegurar_esquema('admin', 'colocolo')
    repo.registrar(MASCOTA, png, 'image/png')
    otro = Repositorio(str(db))
    fila = otro.listar()[0]
    datos, tipo = otro.leer_imagen(fila['id'])
    assert fila['tiene_imagen'] is True
    assert datos == png
    assert tipo == 'image/png'


def test_nivel2_pago_autorizado_vacia_el_carrito():
    carrito = Carrito()
    carrito.agregar(buscar(1))
    resultado = pagar_carrito(carrito, StubWebpay())
    assert resultado.aprobado
    assert resultado.codigo == 'autorizado'
    assert not carrito


def test_nivel2_pago_rechazado_deja_el_carrito():
    carrito = Carrito()
    carrito.agregar(buscar(1))
    resultado = pagar_carrito(carrito, StubWebpay(), medio='rechazo')
    assert not resultado.aprobado
    assert len(carrito) == 1


def test_nivel2_carrito_vacio_no_autoriza():
    resultado = pagar_carrito(Carrito(), StubWebpay())
    assert not resultado.aprobado
    assert resultado.codigo == 'monto-invalido'


def test_nivel3_la_api_guarda_y_devuelve_la_imagen(api_client):
    png = b'\x89PNG\r\n\x1a\n' + b'foto-api'
    alta = api_client.post('/registrar_mascota', data={
        'nombre': 'Foto', 'rut': '22.222.222-2', 'chip': 'CHIP-FOTO',
        'edad': '1', 'color': 'negro', 'tipo': 'Perro',
        'imagen': (BytesIO(png), 'luna.png', 'image/png'),
    })
    assert alta.status_code == 201
    assert alta.get_json()['imagen_guardada'] is True
    lista = api_client.get('/mascotas').get_json()
    mia = next(m for m in lista if m['chip'] == 'CHIP-FOTO')
    assert mia['tiene_imagen'] is True
    assert mia['rut'] == '22.222.222-2'
    img = api_client.get(f"/mascotas/{mia['id']}/imagen")
    assert img.status_code == 200
    assert img.data == png
