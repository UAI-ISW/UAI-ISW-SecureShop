# Auditoría OWASP — SecureShop

**Alcance:** código de `SecureShop/` (versión original) y `SecureShopRefactorizadoMVC/`.
**Metodología:** revisión de código (SAST manual) mapeada a **OWASP Top 10:2021**.
**Propósito docente:** demostrar que se parte de un proyecto real e imperfecto y que la
**primera prioridad del Sprint 1 es seguridad** (identidad con QuickLogin/NeuroLedger).

> Estado dinámico (DAST): plan de pruebas definido en
> [`owasp-secureshop-test-plan.md`](owasp-secureshop-test-plan.md) (ambiente, casos TC-01…TC-09,
> OWASP ZAP y enfoque GenAI); pendiente de **ejecutar** con la app levantada. Los hallazgos
> siguientes son por lectura de código y son reproducibles localmente.

## Resumen de hallazgos

| # | Hallazgo | OWASP 2021 | Severidad |
|---|---|---|---|
| H1 | Contraseñas en texto plano (almacenadas y comparadas) | A07 | **Crítica** |
| H2 | Sin control de acceso: endpoints sensibles abiertos | A01 | **Crítica** |
| H3 | "Login" decorativo: no crea sesión, no protege nada | A04 / A07 | **Alta** |
| H4 | Exposición de PII (RUT, chip) sin autenticación | A01 / A02 | **Alta** |
| H5 | `debug=True` en producción (Werkzeug debugger → RCE) | A05 | **Alta** |
| H6 | Secretos hardcodeados (`admin/colocolo`, `secret_key`) | A05 / A07 | **Alta** |
| H7 | CORS abierto a cualquier origen (`CORS(app)`) | A05 | Media |
| H8 | Sin registro/auditoría de acciones | A09 | Media |

## Detalle

### H1 — Contraseñas en texto plano (A07)
`api.py` siembra el usuario con la clave en claro y el "login" la compara directamente:

```python
# api.py
c.execute('INSERT OR IGNORE INTO usuarios (usuario, password) VALUES (?, ?)',
          ('admin', 'colocolo'))
# securesoftware.py
c.execute('SELECT * FROM usuarios WHERE usuario = ? AND password = ?', (usuario, password))
```
- **Impacto:** cualquier acceso a `secure_shop.db` revela todas las credenciales. No hay hash.
- **Remediación:** almacenar solo hash (bcrypt/argon2); comparar por verificación de hash.
  En el curso: **sustituir por QuickLogin/NeuroLedger** (identidad verificable, sin custodiar contraseñas).

### H2 — Broken Access Control (A01)
`/mascotas`, `/estadisticas` y `/registrar_mascota` no exigen autenticación ni autorización.
- **PoC:** `curl http://localhost:5001/mascotas` devuelve toda la tabla; `curl -X POST
  http://localhost:5001/registrar_mascota -H "Content-Type: application/json" -d '{...}'`
  inserta sin credenciales.
- **Remediación:** exigir identidad autenticada + rol; denegar por defecto.

### H3 — Autenticación decorativa (A04 / A07)
El login válido solo hace `redirect(url_for('estadisticas'))`: no crea sesión ni token, y
`/estadisticas` es accesible directo sin pasar por login.
- **Impacto:** el "control" no controla nada; falla de diseño.
- **Remediación:** sesión/token con expiración; proteger rutas; **diseño seguro desde el inicio**.

### H4 — Exposición de PII (A01 / A02)
`GET /mascotas` devuelve `rut` y `chip` (datos personales, Ley 21.719) de todos los registros,
sin autenticación y renderizados en `estadisticas.html`.
- **Remediación:** autenticar el acceso, minimizar campos expuestos, enmascarar RUT.

### H5 — `debug=True` (A05)
Los tres procesos corren con `app.run(debug=True, ...)`. El debugger de Werkzeug permite
ejecución de código si se dispara una excepción.
- **Remediación:** `debug=False` en cualquier despliegue; controlar por variable de entorno.

### H6 — Secretos hardcodeados (A05 / A07)
`admin/colocolo` en `api.py` y `app.secret_key = 'tu_clave_secreta_aqui'` en `app.py` (MVC).
- **Remediación:** secretos por variable de entorno / gestor de secretos; nunca en el repo.

### H7 — CORS abierto (A05)
`CORS(app)` en `api.py` habilita cualquier origen contra una API sin auth.
- **Remediación:** acotar orígenes permitidos.

### H8 — Sin auditoría (A09)
No hay logging de accesos ni de operaciones sensibles (registro/consulta de PII).
- **Remediación:** log estructurado por acción → conecta con **trazabilidad de NeuroLedger**.

## Lo que ya está bien (no regresionar)

- **Consultas parametrizadas** → sin SQL injection (A03) en las rutas revisadas.
- **Autoescape de Jinja2** → sin XSS por defecto en los `templates/`.

## Del hallazgo a la solución del curso

Los hallazgos H1–H4 justifican la **primera historia técnica**: reemplazar el login de
juguete por **QuickLogin (NeuroLedger)** — identidad verificable, autorización como contrato
auditable y trazabilidad (H8). Es el punto donde "seguridad primero" deja de ser eslogan y se
vuelve el primer incremento demostrable.
