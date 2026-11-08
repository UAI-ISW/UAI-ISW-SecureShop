# Construcción

El despliegue de ISW se hace a mano, con los comandos de [`../README.md`](../README.md). Cada proceso se ve en su terminal. El `.venv` y `secure_shop.db` no se versionan.

## Build

Desde la raíz del repo:

```bash
make build
```

Eso deja `dist/secureshop-0.1.0.tar.gz` con `api.py`, `secureshop.py`, `nucleo/`, `templates/`, `requirements.txt` y `.env.example`. No entran las pruebas, `ISW/`, `seguridad-ti/` ni el `.git`.

Ese archivo es el que una automatización puede copiar a otra máquina y repetir. El CI de hoy no lo publica: corre pytest. El comando que un job llamaría después es `make build`. El reporte de pytest y la corrida de la noche están en [`../operacion.md`](../operacion.md).

## Falta el instalador

Hoy cada instalación es el árbol del repo, con el código a la vista. El instalador es el paso que no está.

Tomaría solo `dist/secureshop-0.1.0.tar.gz`, no el clon. En la máquina de destino crearía un directorio de instalación, por ejemplo `~/Aplicaciones/secureshop`, con su propio entorno virtual, instalaría `requirements.txt` y dejaría dos comandos, uno para `api.py` y otro para `secureshop.py`. Las pruebas y la documentación del curso no irían en esa máquina.

Eso todavía deja los `.py` en el directorio de instalación. Para que la instalación no lleve el código a la vista, el instalador tendría que congelar los dos procesos en la máquina de build (PyInstaller o equivalente): un ejecutable para la API y otro para la tienda, con las plantillas adentro. En el destino quedarían esos dos binarios, el `.env` y `secure_shop.db`. El fuente se queda donde se hizo el `make build`.

Este MVP no trae ese instalador. El servidor sigue siendo el de desarrollo, y el curso lee el código en el repo. Las decisiones de lenguaje están en [`../05-decisiones/tecnologias.md`](../05-decisiones/tecnologias.md).
