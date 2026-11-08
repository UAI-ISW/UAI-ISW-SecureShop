# Configuración y pruebas con IA

La línea de base es esta carpeta. Un cambio entra por una rama y un pull request. La IA puede escribir y puede revisar. No aprueba, y no cierra sola un hallazgo.

Nada de esto se sube desde el editor del agente. El commit lo hace una persona.

## Qué se versiona

| Ítem | Dónde | En git |
|---|---|---|
| Aplicación y API | `SecureShop/secureshop.py`, `api.py`, `nucleo/` | Sí |
| Plantillas y pruebas | `SecureShop/templates/`, `SecureShop/tests/` | Sí |
| Dependencias | `requirements.txt`, `requirements-dev.txt` | Sí, sin versión fija (eso sigue abierto) |
| Plantilla de secretos | `SecureShop/.env.example` | Sí. El `.env` real no |
| Cómo se levanta y cómo se prueba | `run-local.sh`, `docs/`, `.github/workflows/ci.yml` | Sí |
| Base local, entorno, informes de Antares o ZAP | `secure_shop.db`, `.venv/`, `~/pentesting/` | No |

La base y el `.env` se recrean en la máquina. Si `git status` los muestra, no se agregan.

`SecureShopRefactorizadoMVC/` está en el árbol y no es la línea de base. No se levanta junto con `./run-local.sh`.

## Cómo entra un cambio

1. Rama desde `main`. Un cambio, una historia de [`tickets.md`](tickets.md).
2. En la máquina: `cd SecureShop && python -m pytest -q`. Rojo: no se abre el pull request.
3. Otra persona, u otro chat sin el historial que escribió el diff, lee el cambio.
4. Pull request. El CI corre el mismo `pytest`. Rojo bloquea el merge.
5. Una persona aprueba. La aprobación del modelo que escribió el código no cuenta.
6. Antes de mezclar, el mismo `pytest` contra el `main` más nuevo.

Riesgo de la aprobación humana:

| Cambio | Personas |
|---|---|
| Solo documentación | 0, si el CI no aplica |
| Textos, catálogo, plantilla que no toca sesión | 1 |
| Login, sesión, `api.py`, `.env`, `nucleo/repositorio.py` | 2, y una de ellas no es un bot |

## Seis revisiones (prueba con IA)

Cada capa pregunta una cosa distinta. Un `pytest` verde no cierra la seguridad.

| # | Qué | En este repo |
|---|---|---|
| 1 | Antes del PR | `pytest`. Después, lectura del diff en frío |
| 2 | CI obligatorio | `.github/workflows/ci.yml`. Rojo bloquea. Hoy es un solo sistema (Ubuntu, Python 3.13), sin lint ni tipos |
| 3 | Revisión de IA | Cada comentario es **importante** (bloquea), **nit** (no bloquea) o **ya estaba** |
| 4 | Seguridad | Antares con la app apagada ([`qa/README.md`](qa/README.md)). ZAP con la app en `127.0.0.1` ([`qa/pruebas-funcionales-zap.md`](qa/pruebas-funcionales-zap.md)). Un hallazgo nuevo bloquea hasta corregirlo o cerrarlo con motivo |
| 5 | Persona según riesgo | La tabla de arriba. El bot no sustituye a la persona |
| 6 | Antes de mezclar | `pytest` otra vez sobre el `main` actual. No hay flags ni despliegue escalonado |

Las filas abiertas de [`qa/README.md`](qa/README.md) (API sin sesión, CORS, `debug=True`, carrito único, rol fijo, sin log) son **ya estaba**. Si la revisión de IA las vuelve a marcar en un PR que no las toca, no se abre otra vuelta para “arreglarlas”.

Cuando un agente revisa a otro, cada nit corregido dispara otra revisión. En un caso público un PR dio más de 50 vueltas en una noche, y cerca del 59 % de los hallazgos ya estaban en la primera ronda. Acá el corte es a las 3 vueltas. De ahí en adelante se mira solo el diff nuevo. Si a la tercera el enfoque no cierra, una persona decide.

## Qué no se le pasa a la IA

No van al chat el `.env`, la base, un RUT que no sea de juguete, ni el informe de ZAP con datos de una corrida. Antares `query` y `sweep` hablan con un modelo local (`127.0.0.1:8000`), no con un servicio de internet. `plan` no necesita ese modelo y no declara una falla.

La IA no escribe el veredicto del mandante. Eso sigue vacío en [`plan-de-aceptacion.md`](plan-de-aceptacion.md) hasta la review.
