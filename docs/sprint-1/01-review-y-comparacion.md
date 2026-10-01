# Sprint 1 — Review y comparación (base vs. avanzada)

- **Fechas:** 8 sep → 2 oct 2026 · **Meta:** login real + `/estadisticas` protegida.
- **Resultado:** meta cumplida. Pruebas de aceptación **4/4 verdes**; CI configurado.

## Antes / después

| Hallazgo | Base (inception) | Sprint 1 |
|---|---|---|
| **H1** contraseñas en texto plano | `admin/colocolo` en claro | admin **hasheado** (`generate_password_hash`) |
| **H2** secretos en el código | `secret_key`/creds hardcodeados | en **variables de entorno** (`.env`) |
| **H3** `/estadisticas` sin sesión | responde **200** sin login | **302 → /login** (exige sesión y rol) |

## Cómo comparar en localhost

Ambas versiones se levantan igual (`./run-local.sh`), en los mismos puertos.

**Versión base (con el bug):**

```bash
git switch inception
./run-local.sh
# GET http://localhost:5002/estadisticas  -> 200 (expone PII sin login)  [H3]
```

**Versión avanzada (Sprint 1):**

```bash
git switch sprint-1
cp SecureShop/.env.example SecureShop/.env   # ajusta SECRET_KEY
./run-local.sh
# GET http://localhost:5002/estadisticas  -> 302 -> /login             [H3 corregido]
# Login en :5002 con admin / colocolo  -> sesión real -> /estadisticas
```

> Al iniciar `api.py`, la siembra re-hashea al admin (upsert), por lo que el login
> funciona también sobre la BD heredada. Correr la app modifica `secure_shop.db` local.

## Pruebas de aceptación

```bash
cd SecureShop
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q          # 4 passed
```

## Definition of Done (Sprint 1)

- [x] US-01 y US-02 implementadas y demostrables en localhost.
- [x] Pruebas de aceptación verdes (AC-LOGIN-OK, AI-LOGIN-BAD, AI-EST-DIRECT, AC-EST-SESION).
- [x] CI en verde en cada push/PR.
- [x] Secretos fuera del código (H2); sin regresiones en tienda/inscripción.

## Próximo (Sprint 2, desde `main`)

US-03 (validación RUT/edad/chip, H5) · endurecer `debug`/CORS (H4).
