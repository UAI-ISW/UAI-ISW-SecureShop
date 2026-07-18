# Comparativa: SecureShop vs. app de referencia (LabCentral)

> **Documento interno (docente).** Objetivo: identificar qué buenas prácticas tiene una app
> más madura del laboratorio (LabCentral, Flask + Docker) que a **SecureShop le faltan**, para
> saber qué vale la pena incorporar como historias del curso. No es una crítica al proyecto:
> SecureShop es un prototipo docente; su valor es justamente mostrar el "antes".

## Resumen en una línea

SecureShop hace lo mínimo para funcionar (mostrar tienda, registrar mascotas, "login" de
juguete). La app de referencia resuelve los mismos problemas pero con **capa de identidad,
autorización, persistencia con ORM, endurecimiento y modularidad**. Ese delta es, casi
literalmente, el temario práctico del curso.

## Tabla de brechas

| Dimensión | SecureShop (nuestra base) | App de referencia (LabCentral) | ¿Lo incorporamos? |
|---|---|---|---|
| **Autenticación** | `SELECT ... WHERE usuario=? AND password=?` con password en **texto plano**; el "login" solo redirige, no crea sesión | Hash de contraseñas (bcrypt) + tokens (JWT) | **Sí** → 1ª historia: QuickLogin/NeuroLedger |
| **Autorización / roles** | No existe. Cualquiera llama `/mascotas`, `/estadisticas`, `/registrar_mascota` | Roles (admin vs usuario), decoradores que protegen rutas | **Sí**, mínimo admin/usuario |
| **Sesión** | Original: sin sesión. MVC: `session` solo para carrito, con `secret_key` hardcodeada | Sesión/token con expiración y secreto por entorno | **Sí** |
| **Persistencia** | `sqlite3` a mano, SQL embebido en cada función | ORM (SQLAlchemy) + modelos | Recomendado (deuda técnica) |
| **Migraciones** | No hay; el esquema se crea con `CREATE TABLE IF NOT EXISTS` | flask-migrate / Alembic | Opcional |
| **Validación de entrada** | Ninguna (`request.form[...]` directo a la BD) | Validación + saneamiento (bleach) | **Sí** |
| **Rate limiting** | No | flask-limiter en endpoints sensibles | Recomendado |
| **Manejo de secretos** | `admin/colocolo` y `secret_key` **en el código** | Config por variables de entorno | **Sí** |
| **CORS** | `CORS(app)` abierto a todo origen | CORS acotado por origen | **Sí** |
| **Modo debug** | `debug=True` en los 3 procesos (Werkzeug debugger = RCE) | Debug apagado en despliegue | **Sí** |
| **Arquitectura** | Original: 3 scripts sueltos. MVC: blueprints + models/controllers (bien) | Blueprints por dominio (auth, exercise, questions, proxy) | Adoptar el patrón MVC ya presente |
| **Contenedores** | No | Docker + orquestación + proxy | No aplica al dominio "tienda" |
| **Trazabilidad / auditoría** | No hay registro de quién hace qué | Logs por acción | **Sí** → encaja con NeuroLedger |

## Lo que SÍ hace bien SecureShop (no romper)

- **Consultas parametrizadas** (`execute(sql, (params,))`): no hay SQL injection en el login
  ni en el registro. Buen punto de partida.
- **Autoescape de Jinja2** activo en los `templates/`: el listado de mascotas no es
  vulnerable a XSS reflejado/almacenado por defecto.
- **La variante MVC** ya separa `models/`, `controllers/` y usa blueprints: es la dirección
  arquitectónica correcta y sirve de referencia para refactorizar la versión original.
- **Separación tienda / API de datos**: aunque simple, ya hay una frontera de servicio
  (`api.py` en `:5001`) que se puede endurecer de forma aislada.

## Traducción a historias del curso (backlog inicial sugerido)

1. **Identidad real (QuickLogin/NeuroLedger)** — reemplazar el login de juguete por
   identidad verificable; eliminar password en texto plano. *(cierra A07)*
2. **Autorización** — proteger `/mascotas`, `/estadisticas` y `/registrar_mascota`; roles
   admin/usuario. *(cierra A01)*
3. **Config segura** — secretos por entorno, `debug=False`, CORS acotado. *(cierra A05)*
4. **Protección de PII** — no exponer RUT/chip sin control; minimizar datos en `/mascotas`.
5. **(Deuda técnica)** — migrar la versión original al patrón MVC ya existente y a ORM.

> Ninguna de estas historias exige "rehacer desde cero": son incrementos sobre una base que
> el equipo ya leyó y entendió. Ese es el hilo del cuaderno hands-on.
