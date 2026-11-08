# Decisiones de tecnología

Esto es un MVP de un proyecto académico. No se lleva a producción.

Se usa Python, Flask, HTML de plantilla (Jinja), CSS, SQLite y pytest. El navegador recibe una página entera en cada clic. El puerto 5002 arma ese HTML. El puerto 5001 es la API (JSON y la foto). Las capas están en [`../02-arquitectura/README.md`](../02-arquitectura/README.md).

## Por qué esta pila, acá

El curso necesita ver el pedido, el HTML, el SQL y la prueba. Flask con plantillas se levanta con `run-local.sh`, sin compilar. La tienda y la API son dos procesos: ZAP y la revisión de código pueden mirar cada borde. SQLite es un archivo: la mascota, la foto y el hash siguen ahí después de bajar los procesos. `nucleo/` se prueba con pytest, caso válido e inválido, sin abrir el navegador.

Node.js o una pantalla reactiva (React, Vue, Svelte) servirían para otra meta: muchas conexiones a la vez, o un carrito que se redibuja sin recargar. Acá esconderían el recorrido detrás de un empaquetador.

## Si se quisiera llevar a producción

No es el caso. Este corte no aguanta eso:

- El servidor es el de desarrollo de Flask, de a un pedido, con `debug=True`.
- El carrito vive en la memoria de un solo proceso.
- SQLite no está para varios servidores escribiendo a la vez.
- La API no publica un contrato. Las dependencias no tienen versión fija, a propósito, para el ejercicio.

Un producto real cambiaría esas cuatro cosas. Este repositorio se queda como MVP para aprender requerimientos, diseño y testing.
