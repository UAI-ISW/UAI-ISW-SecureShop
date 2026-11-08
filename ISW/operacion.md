# Operación · ISW

Configuración, despliegue en la máquina del alumno, integración continua, la corrida de la noche, y la norma de ramas, commits y pull requests. Las historias no se copian acá: están en [`01-requerimientos/historias.md`](01-requerimientos/historias.md).

Antares, ZAP y los casos del OWASP Top 10 son del otro curso: [`../seguridad-ti/README.md`](../seguridad-ti/README.md).

El commit lo hace una persona. El editor no sube solo.

## Gestión de la configuración

| Ítem | En git |
|---|---|
| `SecureShop/secureshop.py`, `api.py`, `nucleo/`, `templates/`, `tests/` | Sí |
| `requirements.txt`, `requirements-dev.txt` | Sí. Sin versión fija: eso sigue abierto |
| `SecureShop/.env.example` | Sí. El `.env` real no |
| `Makefile`, `run-local.sh`, `ISW/`, `seguridad-ti/`, `.github/workflows/` | Sí. `dist/` no |
| `secure_shop.db`, `.venv/`, informes de Antares o ZAP | No. Informes en `~/pentesting/` |

Si `git status` muestra `.env` o un `.db`, no se agregan.

## Norma de rama, commit y pull request

Una rama, una historia o un ticket. El nombre lleva el id:

```text
us-02-ver-estadisticas
ca-02-2-sesion
t01-api-sin-sesion
```

El commit nombra el mismo id y dice qué prueba lo cubre:

```text
US-02: el listado de estadísticas exige sesión

Cubre CA-02.2. pytest tests/test_acceptance.py
```

Reglas:

1. La rama sale de `main`.
2. En la máquina, antes de abrir el pull request: `cd SecureShop && python -m pytest -q`. Rojo: no se abre.
3. El título del pull request empieza por el id (`US-02`, `CA-02.2` o `T01`).
4. El diff incluye el test nuevo, o el test que ya cubría ese id sigue en verde. Un cambio en `nucleo/` sin un caso en `tests/test_unidad.py` o `tests/test_integracion.py` no se mezcla.
5. GitHub corre el mismo pytest en [`.github/workflows/ci.yml`](../.github/workflows/ci.yml). Rojo bloquea el merge.
6. Aprueba una persona. Quien escribió el cambio con un modelo no cuenta como revisor.
7. Login, sesión, `api.py`, `.env` y `nucleo/repositorio.py` piden dos personas, y una de ellas no es un bot.
8. Documentación sola puede entrar sin esa segunda persona. El pytest igual corre si el workflow se dispara.
9. A la tercera vuelta de “arreglé lo que dijo el modelo”, se para. Se mira solo el diff nuevo. Los tickets T01–T06 son “ya estaba”: si el modelo los vuelve a marcar en un PR que no los toca, no se abre otra vuelta para cerrarlos.

La plantilla que GitHub muestra al abrir el PR está en [`.github/pull_request_template.md`](../.github/pull_request_template.md).

No van al chat el `.env`, la base, un RUT que no sea de juguete, ni un informe de ZAP con datos de una corrida.

## Despliegue local

No hay un servidor de producción. El ambiente del alumno es esta máquina. El CI no despliega: prueba. El arranque, comando por comando, está en [`README.md`](README.md): un terminal para `python api.py` (puerto 5001) y otro para `python secureshop.py` (http://127.0.0.1:5002/login, `admin` / `colocolo`). `run-local.sh` es de Seguridad TI.

El dibujo de esos procesos es [`02-arquitectura/despliegue.png`](02-arquitectura/despliegue.png). Sin sesión, `/`, `/carrito`, `/inscribir` y `/estadisticas` vuelven al login. Si el puerto está ocupado: `lsof -i :5001 -i :5002`. Si el login rechaza la clave demo, borrar `SecureShop/secure_shop.db` y volver a levantar los dos procesos.

`make build` deja el artefacto en `dist/`. El instalador que tomaría ese archivo, y que evitaría dejar el código a la vista, no está. El detalle es [`06-construccion/README.md`](06-construccion/README.md).

## Integración continua

En cada push a `main`, `sprint-1`, `sprint-2` o `sprint-3`, y en cada pull request, GitHub (Ubuntu, Python 3.13) instala `SecureShop/requirements-dev.txt` y corre:

```bash
python -m pytest -q
```

Eso incluye unidad, integración, los hallazgos que se conservan y la aceptación automática. No incluye Antares ni ZAP: esos piden el modelo local o una persona en el escritorio, y viven en `seguridad-ti/`.

## Corrida de la noche

[`.github/workflows/noche.yml`](../.github/workflows/noche.yml) corre todos los días a la **01:00**, hora de Chile (UTC−3). En cron de GitHub eso es `0 4 * * *`. También se puede disparar a mano: Actions → Noche → Run workflow.

Hace el mismo pytest, escribe `reporte-noche.xml` (JUnit) y lo deja como artefacto del run. El resumen sale en la página del workflow. Si algo falla, el run queda rojo y el XML igual se guarda.

Esa corrida no levanta la tienda, no llama a Antares y no abre ZAP. El reporte es el de las pruebas que pueden correr solas en GitHub.
