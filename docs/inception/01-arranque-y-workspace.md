# 01 · Arranque y espacio de trabajo

## Levantar en localhost

Opción rápida (script):

```bash
./run-local.sh
```

Opción manual (tres terminales), tal como está documentado en el `README.md` raíz:

```bash
cd SecureShop
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python api.py            # http://localhost:5001  (crea secure_shop.db + admin)
python secureshop.py     # http://localhost:5003  (tienda + inscripción)
python securesoftware.py # http://localhost:5002  (login + estadísticas)
```

## Verificación de humo (smoke test)

```bash
# La API responde y siembra la BD
curl -s http://localhost:5001/mascotas          # -> [] (lista vacía al inicio)

# El panel redirige a login
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5002/   # -> 302
```

## Espacio de trabajo del equipo

- Tablero (GitHub Projects) con las columnas Backlog → Ready → In progress → Review → Done.
- Ramas por **fase**: `inception`, `sprint-1`, `sprint-2`, `sprint-3` (se integran a `main` por PR).
- `main` siempre desplegable.
