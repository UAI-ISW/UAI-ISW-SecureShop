# SecureShop — proyecto base ISW (UAI)

Aplicación de ejemplo para el curso de **Ingeniería de Software (ISW)**. SecureShop es
una pequeña **tienda + registro de mascotas** escrita en Flask. Es un proyecto **real e
imperfecto**: funciona, pero arrastra malas prácticas de seguridad típicas de un primer
prototipo. Por eso es el punto de partida ideal del curso: **no partimos de un proyecto
limpio, partimos de la realidad**. La primera misión del equipo es *hacerse cargo* del
sistema —levantarlo, montar el espacio de trabajo y entenderlo (mentalidad de
**mantención**)— y desde ahí **construir el backlog desde cero**.

> Autoría y titularidad: material docente de la **UAI** (Prof. Romina Torres). Uso
> educativo. Licencia **CC BY-NC-SA 4.0** — ver `LICENSE` y `NOTICE.md`.

## Qué hay aquí

| Carpeta | Qué es | Uso en el curso |
|---|---|---|
| `SecureShop/` | Versión original (Flask plano: `api.py`, `secureshop.py`, `securesoftware.py` + `templates/` + `secure_shop.db`) | **Base oficial** que los equipos forkean y aseguran |
| `SecureShopRefactorizadoMVC/` | Refactor a MVC (blueprints + `models/` + `controllers/`) | Referencia de cómo separar responsabilidades |
| `security/` | Auditoría OWASP y hallazgos | Insumo del hito de seguridad (Sprint 1) |

## Arquitectura (versión original)

Tres procesos Flask que se hablan por HTTP + una base SQLite compartida:

- **`api.py`** (`:5001`) — API de datos. Crea `secure_shop.db`, tablas `mascotas` y
  `usuarios`, siembra `admin`. Endpoints: `POST /registrar_mascota`, `GET /mascotas`.
- **`securesoftware.py`** (`:5002`) — "panel": `login` + `estadisticas` (consume `/mascotas`).
- **`secureshop.py`** (`:5003`) — tienda: catálogo, carrito y formulario `inscribir`.

```
[navegador] → tienda/panel (Flask) → HTTP → api.py (Flask+CORS) → SQLite (secure_shop.db)
```

## Cómo levantarlo (local)

```bash
cd SecureShop
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Terminal 1 — API de datos (crea la BD e inserta admin)
python api.py            # http://localhost:5001

# Terminal 2 — Tienda + inscripción de mascotas
python secureshop.py     # http://localhost:5003

# Terminal 3 — Panel / login / estadísticas
python securesoftware.py # http://localhost:5002
```

Variante MVC:

```bash
cd SecureShopRefactorizadoMVC
pip install -r requirements.txt
python app.py            # http://localhost:5003
```
> La variante MVC referencia `templates/` (reutiliza los de `SecureShop/templates`); si
> la ejecutas aislada, copia esa carpeta.

## El recorrido del curso (ISW)

1. **Levantar y hacerse cargo** — poner el sistema heredado a correr y montar el espacio de
   trabajo del equipo (mantención primero).
2. **Ingeniería reversa** — leer el código y reconstruir la arquitectura (ver sección
   "Arquitectura" arriba).
3. **Backlog desde cero** — con el sistema entendido, construir el product backlog con lo que
   necesita.
4. **Iterar** — tres sprints (Scrum + XP), diseñando con **seguridad como atributo de
   calidad** (identidad, autorización, registro auditable; aspiración: QuickLogin/NeuroLedger).

> **Nota sobre seguridad.** SecureShop tiene fallas reales (contraseñas en texto plano, sin
> sesión/autorización, `debug=True`, PII de mascotas expuesta, CORS abierto). El **análisis
> OWASP formal** y su informe de pruebas se trabajan en el curso de **Seguridad TI**; el
> curso de ISW **no depende** de ese informe. La carpeta `security/` es insumo de ese otro
> curso.
