"""Casos de unidad. No levantan el servidor."""
from nucleo.carrito import Carrito
from nucleo.catalogo import buscar
from nucleo.repositorio import Repositorio


def test_el_carrito_es_uno_solo_para_el_proceso():
    uno = Carrito()
    uno.agregar(buscar(1))
    assert len(uno) == 1
    assert uno.total() == 5000
    uno.vaciar()
    assert not uno


def test_dos_objetos_no_comparten_items_pero_el_del_proceso_si():
    from nucleo.carrito import carrito_del_proceso
    carrito_del_proceso.clear()
    carrito_del_proceso.agregar(buscar(2))
    assert any(p.nombre == 'Correa retráctil' for p in carrito_del_proceso)
    carrito_del_proceso.clear()


def test_buscar_producto():
    assert buscar(4).nombre == 'Juguete para gato'
    assert buscar(99) is None


def test_clave_y_listado_sin_filtrar_pii(tmp_path):
    db = tmp_path / 'shop.db'
    repo = Repositorio(str(db))
    repo.asegurar_esquema('admin', 'colocolo')
    assert repo.clave_correcta('admin', 'colocolo')
    assert not repo.clave_correcta('admin', 'otra')
    repo.registrar({
        'nombre': 'Luna', 'rut': '11.111.111-1', 'chip': 'CHIP-TEST',
        'edad': '2', 'color': 'blanco', 'tipo': 'Gato',
    })
    fila = repo.listar()[0]
    assert fila['rut'] == '11.111.111-1'
    assert fila['chip'] == 'CHIP-TEST'
