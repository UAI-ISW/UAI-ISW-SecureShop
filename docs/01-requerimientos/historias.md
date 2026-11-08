# Requerimientos · historias de usuario

Esta es la evidencia de requerimientos. Cada fila US es la historia. Las filas CA de debajo son sus criterios de aceptación. Pedir sesión en `/estadisticas` es CA-02.2 de ver las estadísticas, no una historia aparte.

El plan para correr esos criterios con el mandante, con el resultado todavía vacío, es [`plan-de-aceptacion.md`](plan-de-aceptacion.md).

Salen del backlog del commit `1cc15f0`. No hay un tablero de GitHub verificado: `gh` no autentica, y el clone de TICS413 no confirma un project board.

| ID | Historia y criterios | MoSCoW | En el código de hoy |
|---|---|---|---|
| US-01 | Como administrador, quiero iniciar sesión, para entrar a la tienda | Must | Sí |
| CA-01.1 | Con `admin` / `colocolo` entra a `/` y ve la barra | Must | Sí. `tests/test_acceptance.py` |
| CA-01.2 | Con una clave incorrecta ve «Credenciales incorrectas» y `/` vuelve a `/login` | Must | Sí. `tests/test_acceptance.py` |
| US-02 | Como administrador, quiero ver las estadísticas de las mascotas inscritas, para saber qué quedó registrado | Must | Sí |
| CA-02.1 | Con sesión, `/estadisticas` muestra el listado | Must | Sí. `tests/test_acceptance.py` |
| CA-02.2 | Sin sesión, `/estadisticas` vuelve a `/login` y no muestra los datos | Must | Sí. `tests/test_acceptance.py` |
| US-03 | Como encargada de datos, quiero registrar una mascota con RUT, edad y chip válidos, para guardar datos confiables | Should | No |
| CA-03.1 | Un RUT con formato inválido no se guarda | Should | No |
| CA-03.2 | Una edad que no es un número no se guarda | Should | No |
| CA-03.3 | Un chip vacío no se guarda | Should | No |
| US-04 | Como dueña, quiero un carrito por sesión, para comprar accesorios sin mezclarlos con otra persona | Could | No. El carrito es una lista del proceso |
| CA-04.1 | Dos sesiones no ven los mismos productos | Could | No |
| CA-04.2 | Al salir, quien entra después no hereda ese carrito | Could | No |
| US-05 | Como administrador, quiero identificarme sin que esta aplicación guarde otra clave, para no custodiar contraseñas | Won't por ahora | No. No está en esta entrega |
| CA-05.1 | Si la identidad la diera un proveedor externo, la tabla no guardaría esa clave | Won't por ahora | No |

## Tickets de seguridad

No son historias de usuario. Siguen abiertos. No se cierran en este corte. El proceso para mirarlos con Antares y con ZAP está en [`../operacion.md`](../operacion.md).

| Ticket | Qué pide | Sigue abierto en |
|---|---|---|
| T01 · A01 | `/mascotas` y `/registrar_mascota` exigen sesión. RUT y chip no salen a cualquiera | `api.py`. La foto `GET /mascotas/<id>/imagen` está igual |
| T02 · A05 | `debug=True` solo si una variable de entorno lo pide | `api.py`, `secureshop.py` |
| T03 · A07 | Si faltan `SECRET_KEY` o `ADMIN_PASSWORD`, el proceso no arranca | Hoy arranca con valores de relleno |
| T04 · A04 | El carrito es el de quien compra, no una lista del proceso | `nucleo/carrito.py` |
| T05 · A07 | El rol sale de la tabla, no de una cadena fija en el login | `secureshop.py` |
| T06 · A09 | Inscribir deja registro de que ocurrió, sin volcar el RUT al log | `secureshop.py` |

También siguen a propósito, y una revisión no los “limpia” salvo que el ticket lo pida: CORS abierto, el POST de login e inscribir sin token, `requirements.txt` sin versión fija. El `INSERT` y el login usan `?`: eso se miró y no se concatena.
