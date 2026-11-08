"""Aceptación: el login abre la tienda y /estadisticas sigue exigiendo sesión."""
import secureshop


def test_login_entra_a_la_tienda(client):
    r = client.post('/login', data={'usuario': 'admin', 'password': 'colocolo'})
    assert r.status_code == 302
    assert r.headers['Location'].endswith('/')

    tienda = client.get('/')
    assert tienda.status_code == 200
    assert b'Collar para perro' in tienda.data


def test_login_invalido_no_entra(client):
    r = client.post('/login', data={'usuario': 'admin', 'password': 'incorrecta'})
    assert b'Credenciales incorrectas' in r.data
    assert client.get('/').status_code == 302
    assert '/login' in client.get('/').headers['Location']


def test_rutas_sin_sesion_van_al_login(client):
    for ruta in ('/', '/carrito', '/inscribir', '/estadisticas'):
        r = client.get(ruta)
        assert r.status_code == 302
        assert '/login' in r.headers['Location']


def test_estadisticas_con_sesion(client, monkeypatch):
    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return [{
                'id': 1, 'nombre': 'tiger', 'rut': '12111111-1', 'chip': '1234',
                'edad': '2', 'color': 'gris', 'tipo': 'Gato',
                'fecha_registro': '2025-04-06 18:43:58',
            }]

    monkeypatch.setattr(secureshop.requests, 'get', lambda *a, **k: FakeResp())
    client.post('/login', data={'usuario': 'admin', 'password': 'colocolo'})
    r = client.get('/estadisticas')
    assert r.status_code == 200
    assert b'tiger' in r.data
