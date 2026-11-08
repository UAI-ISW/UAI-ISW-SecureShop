"""Estos casos documentan debilidades que se dejan a propósito.

Si alguien cierra la API con sesión, estos tests tienen que fallar
y el cambio se discute: no se 'arregla' el test en silencio.
"""
import api


def test_mascotas_responde_sin_sesion(api_client):
    r = api_client.get('/mascotas')
    assert r.status_code == 200
    assert r.get_json() == []


def test_registrar_no_pide_sesion(api_client):
    r = api_client.post('/registrar_mascota', json={
        'nombre': 'Luna', 'rut': '11.111.111-1', 'chip': 'CHIP-TEST',
        'edad': '2', 'color': 'blanco', 'tipo': 'Gato',
    })
    assert r.status_code == 201
    lista = api_client.get('/mascotas').get_json()
    assert lista[0]['rut'] == '11.111.111-1'


def test_el_arranque_sigue_con_depurador():
    assert 'debug=True' in open(api.__file__, encoding='utf-8').read()
    assert 'debug=True' in open('secureshop.py', encoding='utf-8').read()
