# Tickets que ya trae el repo

Salen del backlog que venía en el código (`docs/inception/04-product-backlog.md` del commit `1cc15f0`). No es un tablero de GitHub.

**No está verificado.** No se abrió un proyecto (canvas) en GitHub: `gh` no autentica contra `github.com/UAI-ISW/UAI-ISW-SecureShop`. La otra copia que miramos es solo el clone local de Seguridad TI, `TICS413/2026-2/SEMANA2SEMANA/11-04`. Esa carpeta cruza con la clase de SAST (Antares / OWASP); no confirma issues ni un project board.

| ID | Historia | MoSCoW | En el código de hoy |
|---|---|---|---|
| US-01 | Como administrador, quiero iniciar sesión, para entrar a la aplicación | Must | Sí. Hash, sesión, y el login abre la tienda |
| US-02 | Como administrador, quiero que `/estadisticas` exija sesión y rol, para no exponer datos personales | Must | Sí. Sin cookie vuelve a `/login` |
| US-03 | Como encargada de datos, quiero validar RUT, edad y chip al registrar | Should | No |
| US-04 | Como dueña, quiero un carrito por sesión | Could | No. Hay carrito, pero es una lista compartida del proceso |
| US-05 | Como equipo, queremos SSO con un proveedor externo | Won't por ahora | No. QuickLogin queda anotado en `docs/quicklogin.md` |

Tickets de seguridad (clase TICS413, plantilla SAST). Son mejoras, no historias ya hechas:

| Ticket | Qué pide |
|---|---|
| T01 · A01 | `/mascotas` y `/registrar_mascota` exigen sesión. RUT y chip no salen a cualquiera |
| T02 · A05 | `debug=True` solo si una variable de entorno lo pide |
| T03 · A07 | Si faltan `SECRET_KEY` o `ADMIN_PASSWORD`, el proceso no arranca |
| T04 · A04 | El carrito es el de quien compra, no una lista del proceso |
| T05 · A07 | El rol sale de la tabla, no de una cadena fija en el login |
| T06 · A09 | Inscribir deja registro de que ocurrió, sin volcar el RUT al log |
