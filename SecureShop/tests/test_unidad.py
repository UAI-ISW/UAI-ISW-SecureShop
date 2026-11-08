"""Casos de unidad del backend. Un componente a la vez. No levantan Flask.

Válidos e inválidos de Repositorio, Carrito, Catálogo y StubWebpay.
La integración de esos componentes está en test_integracion.py.
"""
import sqlite3

import pytest

from nucleo.carrito import Carrito, carrito_del_proceso
from nucleo.catalogo import buscar
from nucleo.pago import StubWebpay
from nucleo.repositorio import Repositorio

MASCOTA = {
    'nombre': 'Luna', 'rut': '11.111.111-1', 'chip': 'CHIP-TEST',
    'edad': '2', 'color': 'blanco', 'tipo': 'Gato',
}


def _repo(tmp_path):
    repo = Repositorio(str(tmp_path / 'shop.db'))
    repo.asegurar_esquema('admin', 'colocolo')
    return repo


def test_valido_clave_correcta(tmp_path):
    assert _repo(tmp_path).clave_correcta('admin', 'colocolo')


def test_invalido_clave_incorrecta(tmp_path):
    assert not _repo(tmp_path).clave_correcta('admin', 'otra')


def test_invalido_usuario_que_no_existe(tmp_path):
    assert not _repo(tmp_path).clave_correcta('nadie', 'colocolo')


def test_valido_la_clave_queda_como_hash_con_salt(tmp_path):
    db = tmp_path / 'shop.db'
    repo = Repositorio(str(db))
    repo.asegurar_esquema('admin', 'colocolo')
    conn = sqlite3.connect(db)
    guardada = conn.execute('SELECT password FROM usuarios').fetchone()[0]
    conn.close()
    assert guardada != 'colocolo'
    metodo, salt, digest = guardada.split('$')
    assert metodo.startswith('pbkdf2:sha256')
    assert salt
    assert digest
    assert repo.clave_correcta('admin', 'colocolo')


def test_valido_registrar_y_listar_conserva_rut_y_chip(tmp_path):
    repo = _repo(tmp_path)
    repo.registrar(MASCOTA)
    fila = repo.listar()[0]
    assert fila['rut'] == '11.111.111-1'
    assert fila['chip'] == 'CHIP-TEST'
    assert fila['tiene_imagen'] is False


def test_invalido_registrar_sin_nombre(tmp_path):
    datos = dict(MASCOTA)
    del datos['nombre']
    with pytest.raises(KeyError):
        _repo(tmp_path).registrar(datos)


def test_valido_leer_imagen(tmp_path):
    repo = _repo(tmp_path)
    png = b'\x89PNG\r\n\x1a\n' + b'foto'
    repo.registrar(MASCOTA, png, 'image/png')
    fila = repo.listar()[0]
    datos, tipo = repo.leer_imagen(fila['id'])
    assert datos == png
    assert tipo == 'image/png'


def test_invalido_leer_imagen_de_un_id_que_no_existe(tmp_path):
    assert _repo(tmp_path).leer_imagen(999) is None


def test_valido_agregar_suma_el_precio():
    carrito = Carrito()
    carrito.agregar(buscar(1))
    assert len(carrito) == 1
    assert carrito.total() == 5000


def test_invalido_carrito_vacio_total_cero():
    carrito = Carrito()
    assert carrito.total() == 0
    carrito.vaciar()
    assert not carrito


def test_valido_el_carrito_del_proceso_es_uno_solo():
    carrito_del_proceso.clear()
    carrito_del_proceso.agregar(buscar(2))
    assert any(p.nombre == 'Correa retráctil' for p in carrito_del_proceso)
    carrito_del_proceso.clear()


def test_valido_buscar_producto():
    assert buscar(4).nombre == 'Juguete para gato'


def test_invalido_buscar_producto_que_no_existe():
    assert buscar(99) is None


def test_valido_stub_webpay_autoriza():
    resultado = StubWebpay().cobrar(5000, 'webpay')
    assert resultado.aprobado
    assert resultado.codigo == 'autorizado'


def test_invalido_stub_webpay_monto_cero():
    resultado = StubWebpay().cobrar(0, 'webpay')
    assert not resultado.aprobado
    assert resultado.codigo == 'monto-invalido'


def test_invalido_stub_webpay_monto_negativo():
    resultado = StubWebpay().cobrar(-1, 'webpay')
    assert not resultado.aprobado
    assert resultado.codigo == 'monto-invalido'


def test_invalido_stub_webpay_rechazo():
    resultado = StubWebpay().cobrar(5000, 'rechazo')
    assert not resultado.aprobado
    assert resultado.codigo == 'rechazado'
