# Casos · OWASP Top 10:2021

Cada caso tiene id, objetivo, entrada, procedimiento y salida esperada. El resultado lo anota quien lo corre.

Precondiciones de todos: `./run-local.sh` abierto, solo `127.0.0.1`, puertos 5001 y 5002. ZAP en modo Protected, con los dos puertos en el contexto: [`zap.md`](zap.md). El mismo caso por terminal es `./seguridad-ti/casos.sh a01` … `a10`.

Un «no» también se anota. En este MVP hay ítems que se ven y otros que aguantan. No se cierra el código: T01–T06 siguen abiertos. El resultado va a `~/pentesting/DAST/`, no al repo.

---

# A01 · Control de acceso roto

| Campo | Contenido |
|---|---|
| ID | A01 |
| Objetivo | Mostrar que la API entrega RUT y chip sin sesión |
| Ticket | T01, sigue abierto |
| Entrada | `GET http://127.0.0.1:5001/mascotas` sin cookie. POST JSON a `/registrar_mascota`: nombre `CasoA01`, rut `1-9`, chip `CASO-A01`, edad `1`, color `gris`, tipo `Gato` |
| Salida esperada | El GET responde 200 y el JSON trae `rut` y `chip`. El POST responde 201. `http://127.0.0.1:5002/estadisticas` sin sesión vuelve a `/login` |

## Procedimiento

1. En el navegador de ZAP, Salir.
2. Abrir `http://127.0.0.1:5001/mascotas`.
3. En History, confirmar que el GET no lleva cookie y que el cuerpo trae `rut`.
4. En Manual Request Editor, el POST de la entrada, sin cookie.
5. Abrir `http://127.0.0.1:5002/estadisticas` sin haber entrado de nuevo.

Por terminal: `./seguridad-ti/casos.sh a01`.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| La API entregó RUT y chip sin sesión | | |
| La web de estadísticas volvió al login | | |

---

# A02 · Fallas criptográficas

| Campo | Contenido |
|---|---|
| ID | A02 |
| Objetivo | Mostrar que la sesión viaja sin la marca `Secure`, y que la clave en la tabla no está en claro |
| Entrada | POST `/login` con usuario `admin` y clave `colocolo` |
| Salida esperada | `Set-Cookie` trae `HttpOnly` y no trae `Secure`. En la tabla, la celda empieza por `pbkdf2:sha256` y no es la palabra `colocolo` |

## Procedimiento

1. En el navegador de ZAP, entrar con `admin` / `colocolo`.
2. En History, abrir la respuesta del POST `/login` y leer `Set-Cookie`.
3. En la terminal, desde la raíz: `./seguridad-ti/casos.sh a02`. Anotar la línea de la tabla.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| La cookie no trae `Secure` | | |
| La celda no es la palabra `colocolo` | | |

---

# A03 · Inyección

| Campo | Contenido |
|---|---|
| ID | A03 |
| Objetivo | Comprobar si una comilla inyecta el login o el alta |
| Entrada | Usuario `admin' OR '1'='1` y clave `x` en `/login`. POST JSON a `/registrar_mascota` con nombre `Bobby' OR '1'='1`, rut `1-9`, chip `CASO-A03`, edad `1`, color `negro`, tipo `Perro` |
| Salida esperada | El login muestra «Credenciales incorrectas». El nombre queda guardado como texto y `GET /mascotas` sigue siendo una lista. En este MVP la inyección no se concreta |

## Procedimiento

1. En el formulario de login, enviar la entrada del usuario con comilla.
2. En History, leer el HTML de la respuesta.
3. En Manual Request Editor, el POST del alta. Después, `GET /mascotas` y buscar el chip `CASO-A03`.

Por terminal: `./seguridad-ti/casos.sh a03`.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| El login rechazó la comilla | | |
| El nombre quedó como texto y la lista sigue | | |

---

# A04 · Diseño inseguro

| Campo | Contenido |
|---|---|
| ID | A04 |
| Objetivo | Mostrar que el carrito es del proceso, no de la sesión |
| Ticket | T04, sigue abierto |
| Entrada | Sesión A: login `admin` / `colocolo` y `GET /agregar/1` (Collar para perro). Sesión B: otro login, sin pasar por `/agregar` |
| Salida esperada | El carrito de B muestra «Collar para perro» |

## Procedimiento

1. En el navegador de ZAP, entrar y agregar el collar. History queda con `GET /agregar/1`.
2. En una ventana privada, entrar con `admin` / `colocolo` y abrir el carrito.
3. Comparar las dos cookies. El collar está en las dos pantallas.

Por terminal: `./seguridad-ti/casos.sh a04`.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| B vio el collar sin agregarlo | | |

---

# A05 · Configuración insegura

| Campo | Contenido |
|---|---|
| ID | A05 |
| Objetivo | Mostrar el depurador en un error, y el CORS abierto |
| Ticket | T02, sigue abierto |
| Entrada | POST `http://127.0.0.1:5001/registrar_mascota` con `Content-Type: application/json` y cuerpo `{}`. Después, `GET /mascotas` |
| Salida esperada | El POST responde 500 y el HTML nombra al depurador. El GET trae `Access-Control-Allow-Origin: *` |

## Procedimiento

1. En Manual Request Editor, enviar el POST vacío.
2. En la respuesta, mirar la palabra «depurador» y cortar. No se abre la consola y no se copia el PIN que imprime la terminal de `./run-local.sh`.
3. En History, el GET `/mascotas`, leer la cabecera CORS.

Por terminal: `./seguridad-ti/casos.sh a05`.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| El 500 nombra al depurador | | |
| El listado manda `Access-Control-Allow-Origin: *` | | |

---

# A06 · Componentes vulnerables o viejos

| Campo | Contenido |
|---|---|
| ID | A06 |
| Objetivo | Mostrar que la dependencia que corre no está fijada en el archivo que la instala |
| Entrada | `SecureShop/requirements.txt` y el Flask del `.venv` que levantó `./run-local.sh` |
| Salida esperada | El archivo lista `Flask` sin versión. `pip` imprime un número de versión distinto de «sin fijar» |

## Procedimiento

1. En History, un GET a `http://127.0.0.1:5002/login`. Anotar la cabecera `Server` si viene.
2. Desde la raíz: `./seguridad-ti/casos.sh a06`.
3. Comparar el número de Flask con la línea de `requirements.txt`.

No hace falta explotar un CVE.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| `requirements.txt` no fija la versión | | |
| El Flask instalado tiene un número | | |

---

# A07 · Fallas de identificación

| Campo | Contenido |
|---|---|
| ID | A07 |
| Objetivo | Mostrar la clave de demo en la página, y que tres fallos no bloquean |
| Ticket | T03, sigue abierto |
| Entrada | GET `/login`. Tres POST con clave `mala`. Un POST con `admin` / `colocolo` |
| Salida esperada | El HTML del GET muestra `admin / colocolo`. Los tres fallos se quedan en el login. El cuarto responde 302 hacia la tienda |

## Procedimiento

1. Abrir `http://127.0.0.1:5002/login` en el navegador de ZAP.
2. En History, leer el HTML del GET.
3. Enviar tres claves malas y después `colocolo`. Anotar el código de la última respuesta.

Por terminal: `./seguridad-ti/casos.sh a07`.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| La página muestra `admin / colocolo` | | |
| Después de tres fallos, la demo sigue entrando | | |

---

# A08 · Fallas de integridad

| Campo | Contenido |
|---|---|
| ID | A08 |
| Objetivo | Mostrar que la API guarda bytes que no son una imagen si el cliente dice `image/png` |
| Entrada | POST multipart a `/registrar_mascota`: nombre `CasoA08`, rut `1-9`, chip `CASO-A08`, edad `1`, color `gris`, tipo `Perro`, archivo cuyo contenido es `no-es-una-imagen` y tipo `image/png` |
| Salida esperada | La respuesta dice `imagen_guardada` verdadero. `GET /mascotas/<id>/imagen` devuelve esos bytes |

## Procedimiento

1. Desde la raíz, con la app arriba: `./seguridad-ti/casos.sh a08`.
2. Anotar el id y los bytes que imprime.
3. ZAP no ve ese pedido si no pasó por el proxy. La evidencia de la ficha es la salida del comando.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| Guardó bytes que no son PNG | | |

---

# A09 · Fallas de registro y monitoreo

| Campo | Contenido |
|---|---|
| ID | A09 |
| Objetivo | Mostrar que inscribir deja la línea de acceso y no una línea de auditoría de quién lo hizo |
| Ticket | T06, sigue abierto |
| Entrada | POST JSON a `/registrar_mascota`: nombre `CasoA09`, rut `1-9`, chip `CASO-A09`, edad `1`, color `gris`, tipo `Gato` |
| Salida esperada | La terminal de `./run-local.sh` muestra `POST /registrar_mascota`. No muestra una línea de auditoría de quién inscribió |

## Procedimiento

1. Inscribir por el formulario del navegador de ZAP, o correr `./seguridad-ti/casos.sh a09`.
2. En History, confirmar que el POST salió.
3. Mirar la terminal del script. Anotar la línea de acceso y la ausencia de auditoría.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| Hubo línea de acceso | | |
| No hubo línea de auditoría | | |

---

# A10 · SSRF

| Campo | Contenido |
|---|---|
| ID | A10 |
| Objetivo | Comprobar si la API abre una URL que viene en el pedido |
| Entrada | `GET http://127.0.0.1:5001/mascotas?url=http://127.0.0.1:9/no-existe` |
| Salida esperada | Código 200 y el cuerpo sigue siendo el listado. En este MVP la app no abre esa URL |

## Procedimiento

1. En la barra del navegador de ZAP, abrir la entrada.
2. En History, leer el código y el cuerpo.
3. No se apunta el pedido a otro host.

Por terminal: `./seguridad-ti/casos.sh a10`.

## Resultado

| Verificación | Resultado (sí / no) | Evidencia |
|---|---|---|
| El listado volvió igual | | |
| No se observó que el servidor fuera a buscar la URL | | |
