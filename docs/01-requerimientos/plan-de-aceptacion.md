# Plan de aceptación · SecureShop

Lo recibimos armado. La entrega es con el mandante, así que el plan se escribe ahora y se corre en la review. Hasta ese día los resultados reales quedan vacíos. Un caso no está aceptado porque el código exista.

Formato tomado de `TICS331/repo/testing/` (plan + caso con escenario feliz e inválido). Ese ejemplo reescribe las historias (comprador, `/catalogo`, chip duplicado) y las marca hechas. Aquí no: las historias son las del código recibido, y el chip duplicado no está implementado, así que no entra al plan.

| Campo | Contenido |
|---|---|
| Proyecto | SecureShop, caso guía |
| De dónde sale | Repo recibido. Copia única: `100-websites y repos/repos/repos-ISW-Intedisciplinario/UAI-ISW-SecureShop` |
| Mandante | Aún no corre este plan con nosotros |
| Qué se acepta en esta entrega | US-01 y US-02 |
| Qué viene en el código y no se acepta como historia | Catálogo, carrito en memoria, inscribir sin validación |

Una historia queda aceptada solo si pasan sus criterios, vistos por el mandante.

## Casos

| Caso | Historia | Criterio | Entonces |
|---|---|---|---|
| CT-001 | US-01 · iniciar sesión | CA-01.1 | Entra a la tienda y hay sesión |
| CT-001 | US-01 · iniciar sesión | CA-01.2 | Mensaje de error y no hay sesión |
| CT-002 | US-02 · ver estadísticas | CA-02.1 | Con sesión, `/estadisticas` muestra las mascotas |
| CT-002 | US-02 · ver estadísticas | CA-02.2 | Sin sesión, `/estadisticas` va a `/login` |

## No funcional

No se inventa una banda. En localhost no hay ventana de disponibilidad ni otra persona cronometrada. Queda fuera de "aceptable" hasta medirlo con el mandante.

| Caso | Qué miraríamos | Estado |
|---|---|---|
| CT-RNF-01 | Que se pueda usar cuando el mandante lo necesita | No medido |

---

# CT-001 · Iniciar sesión y entrar

| Campo | Contenido |
|---|---|
| Caso | CT-001 |
| Historia | US-01 |
| Prioridad | Must |

## Historia

Como administrador, quiero iniciar sesión, para entrar a la tienda.

## Criterios

**CA-01.1 · la clave demo entra**

- **Dado** el usuario de demo `admin` / `colocolo`
- **Cuando** envía esa clave en `/login`
- **Entonces** ve la tienda (`/`) y la barra de la aplicación

**CA-01.2 · una clave mala no entra**

- **Dado** el mismo usuario
- **Cuando** envía una clave incorrecta
- **Entonces** ve «Credenciales incorrectas» y `/` lo devuelve a `/login`

## Pasos

| Paso | Qué se hace | Qué se tiene que ver |
|---|---|---|
| 1 | Abrir http://127.0.0.1:5002/login | Formulario |
| 2 | Entrar con `admin` / `colocolo` | Tienda, con la barra |
| 3 | Salir | Vuelve el formulario |
| 4 | Entrar con una clave mala | El mensaje de error, sin barra |

## Resultados reales

| Verificación | Resultado | Evidencia |
|---|---|---|
| CA-01.1 | | |
| CA-01.2 | | |

**Estado del caso:** no corrido con el mandante.

---

# CT-002 · Ver estadísticas

| Campo | Contenido |
|---|---|
| Caso | CT-002 |
| Historia | US-02 |
| Prioridad | Must |

## Historia

Como administrador, quiero ver las estadísticas de las mascotas inscritas, para saber qué quedó registrado.

Exigir sesión no es otra historia. Es CA-02.2 de esta.

## Criterios

**CA-02.1 · con sesión se ve el listado**

- **Dado** que CA-01.1 ya pasó
- **Cuando** abre Estadísticas
- **Entonces** ve el listado

**CA-02.2 · sin sesión no se ven los datos**

- **Dado** que no hay sesión
- **Cuando** abre `/estadisticas`
- **Entonces** va a `/login` y no ve el listado

## Pasos

| Paso | Qué se hace | Qué se tiene que ver |
|---|---|---|
| 1 | Con la sesión del paso 2 de CT-001, abrir Estadísticas | La tabla |
| 2 | Salir, o usar una ventana sin cookie | Sin sesión |
| 3 | Abrir http://127.0.0.1:5002/estadisticas | El login, no la tabla |

## Resultados reales

| Verificación | Resultado | Evidencia |
|---|---|---|
| CA-02.1 | | |
| CA-02.2 | | |

**Estado del caso:** no corrido con el mandante.

## Cierre (lo llena el mandante)

| Campo | Contenido |
|---|---|
| ¿Entra a la hoja de aceptación? | Sí, cuando se corra |
| Veredicto | Pendiente |
| Si vuelve al backlog | |
