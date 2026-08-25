# 02 · Arquitectura reconstruida (ingeniería reversa)

Leyendo el código heredado, SecureShop son **tres procesos Flask** que se comunican
por HTTP y comparten una **base SQLite** (`secure_shop.db`).

```
[navegador] → tienda (:5003)   ─┐
[navegador] → panel  (:5002)   ─┼─ HTTP ─→ api.py (:5001, Flask+CORS) ─→ SQLite (secure_shop.db)
                                │
                     (panel consume GET /mascotas)
```

## Componentes

| Proceso | Puerto | Responsabilidad | Rutas clave |
|---|---|---|---|
| `api.py` | 5001 | API de datos; crea la BD, tablas `mascotas` y `usuarios`, siembra `admin` | `POST /registrar_mascota`, `GET /mascotas` |
| `securesoftware.py` | 5002 | Panel: login y estadísticas | `/login`, `/estadisticas` |
| `secureshop.py` | 5003 | Tienda: catálogo, carrito, inscripción de mascotas | `/`, `/carrito`, `/inscribir` |

## Modelo de datos

- `usuarios(id, usuario UNIQUE, password)` — hoy la contraseña se guarda **en texto plano**.
- `mascotas(id, nombre, rut, chip, edad, color, tipo, fecha_registro)` — contiene **PII** (RUT, chip).

## Casos de uso (observados)

- **CU01** Comprar productos (tienda → carrito).
- **CU02** Inscribir una mascota (tienda → API).
- **CU03** Login del administrador (panel).
- **CU04** Ver estadísticas / lista de mascotas (panel → API).
