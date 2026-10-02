import os
import tempfile

import pytest

# Los módulos leen su configuración del entorno al importarse, así que hay que
# fijar las variables ANTES de importarlos. Usamos una BD SQLite temporal.
_TMPDIR = tempfile.mkdtemp()
os.environ.setdefault('SECURE_SHOP_DB', os.path.join(_TMPDIR, 'test_secure_shop.db'))
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('ADMIN_USER', 'admin')
os.environ.setdefault('ADMIN_PASSWORD', 'colocolo')

import api            # noqa: E402
import securesoftware  # noqa: E402


@pytest.fixture()
def client():
    # Crea el esquema y siembra al admin con contraseña hasheada en la BD temporal.
    api.init_db()
    securesoftware.app.config['TESTING'] = True
    with securesoftware.app.test_client() as c:
        yield c
