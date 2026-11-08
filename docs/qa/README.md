# Tarea · plan de pruebas y QA

La guía de la clase (4 nov, `11-04-guia.pdf`) pide un hacking ético con permiso: leer el fuente y, después, hablarle a la aplicación encendida. Acá está el recorrido sobre **esta** copia, no sobre el commit viejo de tres procesos.

Orden de un cambio (pytest, CI, revisión con IA, persona): [`../configuracion-y-pruebas-con-ia.md`](../configuracion-y-pruebas-con-ia.md). Esta página es el recorrido Antares, con la tienda apagada. Después, ZAP.

Cómo se instala cada herramienta: [`instalacion.md`](instalacion.md). Qué es cada una y cómo se usa en este testing: [`herramientas.md`](herramientas.md).

Los informes no se guardan dentro del repo. Si caen adentro, la próxima lectura de Antares puede analizar su propio reporte.

```bash
mkdir -p "$HOME/pentesting/SAST" "$HOME/pentesting/DAST"
```

## Revisión de código, a mano

Antes de la herramienta, una persona lee el diff. El mismo modelo que escribió el cambio no cuenta como revisor.

1. El cambio es una sola cosa y corresponde a una historia de [`../tickets.md`](../tickets.md).
2. Se lee el archivo sin el chat que lo generó.
3. Cada comentario se clasifica: **importante** (bloquea), **nit** (no bloquea) o **ya estaba** (el legado de abajo).
4. A la tercera vuelta de “arreglé lo que dijo el modelo”, se para y una persona decide si el enfoque sirve.
5. Login, sesión, `api.py` y `.env` no se mezclan con un visto bueno del bot.

Debilidades que **siguen en el código a propósito**. Una revisión no las “limpia” salvo que el ticket de esa fila lo pida:

| Qué | Dónde |
|---|---|
| `/mascotas` y `/registrar_mascota` no piden sesión; el JSON trae RUT y chip | `api.py` |
| `CORS(app)` abierto | `api.py` |
| `debug=True` al arrancar | `api.py`, `secureshop.py` |
| Clave y contraseña de relleno escritas en el fuente | los dos `.py` y `.env.example` |
| El carrito es uno solo para el proceso | `nucleo/carrito.py` |
| Quien entra queda con rol `admin`; la tabla no tiene rol | `secureshop.py` |
| El POST de login e inscribir no trae token de sesión | `templates/` |
| No hay log de quién inscribió | `secureshop.py` |
| `requirements.txt` sin versión fija | `SecureShop/requirements.txt` |
| El `INSERT` y el login usan `?` | `nucleo/repositorio.py` — mirado: no se concatena |

La guía del 4 nov decía que la tienda no pedía login. Al unir panel y tienda, la puerta web sí pide sesión (US-01). La API no. Eso no se reabre.

## Code review con Antares

Antares no confirma la falla. `plan` elige CWE candidatos. `query` devuelve archivos, no el número de línea. La línea la anota quien abre el fuente. La pauta de contraste de la clase (`11-04-pauta-antares.pdf`) se corrió sobre la carpeta MVC; **esa carpeta no se usa**. El plan de esta tarea es el de `SecureShop/`.

La tienda sigue apagada. Hacen falta dos terminales si van a hablar con el modelo. `plan` solo, en la máquina, no lo necesita.

**1.** Si van a usar `query` o `sweep`, en una terminal dejen el modelo (en la sala ya está; en casa, ver [`instalacion.md`](instalacion.md)). Esperen `modelo listo`. Si el puerto está ocupado, el modelo ya corre: no lo cierren y sigan.

**2.** Otra terminal. El modelo responde:

```bash
curl -s http://127.0.0.1:8000/health
```

Tiene que imprimir `"status": "ok"`. Si van a correr solo `plan`, salten al paso 3.

**3.** La lista de CWE, sobre la carpeta de la aplicación (no sobre `SecureShopRefactorizadoMVC/`):

```bash
export PATH="$HOME/.local/bin:$PATH"
cd "100-websites y repos/repos/repos-ISW-Intedisciplinario/UAI-ISW-SecureShop"
antares plan SecureShop --scope owasp --max-cwes 10 \
  > "$HOME/pentesting/SAST/plan-owasp.txt"
```

Abran ese archivo. Anoten un CWE, por ejemplo `CWE-287`. Si el texto nombra `controllers/carrito_controller.py`, apuntaron a la carpeta MVC: borren la salida y repitan el comando sobre `SecureShop`.

**4.** El reporte de ese CWE. Cambien `CWE-287` por el que anotaron.

```bash
export ANTARES_ENDPOINT="http://127.0.0.1:8000/v1/completions"
export ANTARES_MODEL="antares-350m"
antares query SecureShop \
  --cwe CWE-287 \
  --format markdown \
  --output "$HOME/pentesting/SAST/query-uno"
```

Abran el reporte, abran el archivo que nombra y busquen la línea. Anoten una de estas cuatro frases: el número coincide; la familia coincide y la línea sigue en pie; lo eligió y la línea dice otra cosa; la cátedra lo marcó y `plan` no lo nombró.

**5.** Para los diez de la lista, en la misma terminal:

```bash
antares sweep SecureShop \
  --scope owasp --max-cwes 10 \
  --no-tui \
  --output "$HOME/pentesting/SAST/sweep-owasp"
```

Eso no reemplaza a `plan-owasp.txt`.

## Qué se entrega de esta parte

Una fila por CWE abierto. La plantilla de la clase está en `TICS413/.../11-04/plantilla-sast.md`. Se llena fuera del repo, en `~/pentesting/SAST/hallazgos.md`.

Por cada fila marcada «está», un archivo en `~/pentesting/SAST/tickets/`:

```markdown
# T0X · CWE-___ · título corto

- Archivo:
- Líneas:
- Por qué es una debilidad:
- Cómo se mejora:
- ¿Lo nombró antares plan?  sí / no
```

El cómo es el arreglo, en una frase. No es una receta para usar la falla. No se publica en el repo mientras el análisis siga abierto.
