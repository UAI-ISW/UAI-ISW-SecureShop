import os
import tempfile

import pytest

_TMPDIR = tempfile.mkdtemp()
os.environ.setdefault('SECURE_SHOP_DB', os.path.join(_TMPDIR, 'test_secure_shop.db'))
os.environ.setdefault('SECRET_KEY', 'test-secret-key')
os.environ.setdefault('ADMIN_USER', 'admin')
os.environ.setdefault('ADMIN_PASSWORD', 'colocolo')

import api  # noqa: E402
import secureshop  # noqa: E402


@pytest.fixture()
def client():
    api.init_db()
    secureshop.carrito.clear()
    secureshop.app.config['TESTING'] = True
    with secureshop.app.test_client() as c:
        yield c


@pytest.fixture()
def api_client():
    api.init_db()
    api.app.config['TESTING'] = True
    with api.app.test_client() as c:
        yield c
