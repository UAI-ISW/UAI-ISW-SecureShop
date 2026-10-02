"""Pruebas de aceptación del Sprint 1 (US-01 y US-02).

Mapean 1:1 con el plan de aceptación del kit:
- AC-LOGIN-OK    : login válido redirige a /estadisticas
- AI-LOGIN-BAD   : login inválido no autentica
- AI-EST-DIRECT  : /estadisticas sin sesión redirige a /login (corrige H3)
- AC-EST-SESION  : /estadisticas con sesión lista las mascotas
"""
import securesoftware


def test_ac_login_ok(client):
    r = client.post('/login', data={'usuario': 'admin', 'password': 'colocolo'})
    assert r.status_code == 302
    assert '/estadisticas' in r.headers['Location']


def test_ai_login_bad(client):
    r = client.post('/login', data={'usuario': 'admin', 'password': 'incorrecta'})
    assert b'Credenciales incorrectas' in r.data
    # y sigue sin poder entrar al panel
    r2 = client.get('/estadisticas')
    assert r2.status_code == 302
    assert '/login' in r2.headers['Location']


def test_ai_est_direct_sin_sesion(client):
    r = client.get('/estadisticas')
    assert r.status_code == 302
    assert '/login' in r.headers['Location']


def test_ac_est_con_sesion(client, monkeypatch):
    class FakeResp:
        def json(self):
            return [{
                'id': 1, 'nombre': 'tiger', 'rut': '12111111-1', 'chip': '1234',
                'edad': '2', 'color': 'gris', 'tipo': 'Gato',
                'fecha_registro': '2025-04-06 18:43:58',
            }]

    monkeypatch.setattr(securesoftware.requests, 'get', lambda *a, **k: FakeResp())
    client.post('/login', data={'usuario': 'admin', 'password': 'colocolo'})
    r = client.get('/estadisticas')
    assert r.status_code == 200
    assert b'tiger' in r.data
