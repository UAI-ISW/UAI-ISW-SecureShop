# 03 · Hallazgos del legado

El sistema **funciona pero arrastra malas prácticas** típicas de un primer prototipo.
Estos hallazgos alimentan el backlog. (El análisis OWASP formal es materia del curso
de Seguridad TI; aquí registramos lo que impacta la ingeniería del producto.)

| ID | Hallazgo | Dónde | Severidad | Historia asociada |
|---|---|---|---|---|
| **H1** | Contraseñas en **texto plano** en la tabla `usuarios` | `api.py` `init_db` | Alta | US-01 |
| **H2** | `secret_key` / credenciales **hardcodeadas**; sin variables de entorno | `api.py`, `securesoftware.py` | Alta | chore S1 |
| **H3** | `/estadisticas` **carga sin sesión** (no exige login ni rol) → expone PII | `securesoftware.py` | Alta | US-02 |
| **H4** | `debug=True` en producción; `CORS` totalmente abierto | `api.py`, `securesoftware.py` | Media | chore / S2 |
| **H5** | `POST /registrar_mascota` sin campo obligatorio → **500** (debería 400) | `api.py` | Media | US-03 (S2) |

## Prioridad para Sprint 1

Los **Must** que atacamos primero son **H1/H3** (identidad y autorización), con el
**chore H2** como habilitador (sacar secretos a variables de entorno antes de tocar
el login). H4 y H5 se secuencian en Sprint 2.
