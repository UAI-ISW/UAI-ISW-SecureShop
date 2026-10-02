# 05 · Sprint Planning — Sprint 1

- **Iteración / Sprint N.º:** 1 · **Fechas:** 8 sep → 2 oct 2026
- **Capacidad del equipo:** 48 h

## Meta del sprint

> Al terminar este sprint podremos demostrar que el administrador **inicia sesión real**
> (con contraseña **hasheada** y **sesión** con expiración) y que `/estadisticas`
> **exige sesión** (redirige al login si no la hay).

## Sprint backlog

| ID | Historia | Pts | Responsable(s) | DoR? |
|---|---|---|---|---|
| US-01 | Login con identidad verificable (sesión real, contraseña hasheada) | 5 | Matías, Diego | [x] |
| US-02 | `/estadisticas` exige sesión y rol | 3 | Fernanda | [x] |

**Total puntos comprometidos:** 8 (primer sprint, sin velocidad previa).

## Habilitador (chore)

- Sacar `secret_key` y credenciales de admin a **variables de entorno** (`.env`) antes
  de tocar el login — mitiga el hallazgo **H2**.

## Pruebas de aceptación comprometidas

| Test | Criterio |
|---|---|
| AC-LOGIN-OK | `POST /login` con credencial válida → redirige a `/estadisticas` |
| AI-LOGIN-BAD | `POST /login` con password incorrecto → "Credenciales incorrectas", sin sesión |
| AI-EST-DIRECT | `GET /estadisticas` sin sesión → **redirige a `/login`** (hoy: carga sin login, H3) |

## Riesgos / impedimentos

- La base heredada corre con `debug=True` y secretos hardcodeados → plan: sacarlos a
  variables de entorno **antes** de tocar el login (H2).
