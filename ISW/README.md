# ISW

Esta carpeta se trabaja en VS Code o en Cursor. El recorrido es: abrir el repo, levantar la tienda en la terminal del editor, y después correr las pruebas de abajo hacia arriba. Antares y ZAP quedan en el otro curso, [`../seguridad-ti/README.md`](../seguridad-ti/README.md).

La app de este árbol es `SecureShop/` (`secureshop.py` en el puerto 5002 y `api.py` en el 5001).

## 1. Abrir el proyecto

En VS Code: **Archivo → Abrir carpeta**. En Cursor: **File → Open Folder**. Se elige la raíz del repo, la carpeta donde se ven `Makefile`, `ISW/` y `SecureShop/`.

Hace falta Python 3.10 o más (`python3 --version`). Si el editor pregunta el intérprete: `SecureShop/.venv/bin/python`, después del paso 2. El arranque es a punta de comando, un proceso por terminal. `run-local.sh` es del curso de Seguridad TI.

## 2. Levantar la tienda

**Terminal → Nueva terminal** (en los dos editores el atajo es Ctrl+` ). Tiene que decir la raíz del repo.

```bash
cd SecureShop
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp -n .env.example .env
python api.py
```

Esa terminal queda en la API, http://127.0.0.1:5001. **Terminal → Nueva terminal**, otra vez:

```bash
cd SecureShop
source .venv/bin/activate
python secureshop.py
```

Esa queda en la tienda, http://127.0.0.1:5002/login. Usuario `admin`, clave `colocolo`. Para bajar un proceso: Ctrl-C en su terminal.

El build, el artefacto `dist/secureshop-0.1.0.tar.gz` y el instalador que falta están en [`06-construccion/README.md`](06-construccion/README.md). Desde la raíz: `make build`.

## 3. Pruebas, en este orden

**Terminal → Nueva terminal.** Las dos del paso 2 siguen abiertas. Estas pruebas no le pegan a esos puertos: pytest usa su propia base temporal.

```bash
cd SecureShop
source .venv/bin/activate
python -m pytest tests/test_unidad.py -q
```

Si `source` no deja `python` en el camino: `SecureShop/.venv/bin/python -m pytest …` desde la raíz, sin activar.

| Orden | Qué es | Comando | Dónde se lee |
|---|---|---|---|
| 1 | Unitarias. Cada clase sola, caso válido e inválido | `python -m pytest tests/test_unidad.py -q` | [`04-pruebas/unitarias/README.md`](04-pruebas/unitarias/README.md) |
| 2 | Integración bottom-up. Niveles 1 a 3 | `python -m pytest tests/test_integracion.py -q` | [`04-pruebas/integracion/README.md`](04-pruebas/integracion/README.md) |
| 3 | Aceptación. Login y estadísticas, con sesión y sin sesión | `python -m pytest tests/test_acceptance.py -q` | [`01-requerimientos/plan-de-aceptacion.md`](01-requerimientos/plan-de-aceptacion.md) |
| 4 | Hallazgos que se dejan. La API sigue sin sesión y `debug=True` sigue en el fuente | `python -m pytest tests/test_hallazgos.py -q` | [`01-requerimientos/historias.md`](01-requerimientos/historias.md) |
| 5 | Las cuatro juntas | `python -m pytest -q` | [`operacion.md`](operacion.md) |

Un rojo se mira en el primer comando que falló. No se salta a la pantalla para explicar un fallo de `nucleo/`.

## Evidencia

| Artefacto | Dónde |
|---|---|
| Historias y criterios | [`01-requerimientos/historias.md`](01-requerimientos/historias.md) |
| Plan de aceptación con el mandante | [`01-requerimientos/plan-de-aceptacion.md`](01-requerimientos/plan-de-aceptacion.md) |
| Arquitectura (capas, componentes, cliente-servidor) | [`02-arquitectura/README.md`](02-arquitectura/README.md) |
| Diseño: mapa de navegación y clases | [`03-diseno/README.md`](03-diseno/README.md) |
| Pruebas unitarias | [`04-pruebas/unitarias/README.md`](04-pruebas/unitarias/README.md) |
| Pruebas de integración, bottom-up | [`04-pruebas/integracion/README.md`](04-pruebas/integracion/README.md) |
| Decisiones de tecnología | [`05-decisiones/tecnologias.md`](05-decisiones/tecnologias.md) |
| Construcción y empaquetado | [`06-construccion/README.md`](06-construccion/README.md) |
| Configuración, despliegue local, CI, noche, ramas y PR | [`operacion.md`](operacion.md) |
