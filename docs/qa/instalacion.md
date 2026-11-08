# Instalación de las herramientas

Se hace en el propio computador. En la sala del 4 nov la cátedra ya tenía el modelo escuchando; estos pasos son para repetirlo. Los dos signos menos se escriben en el teclado. Si se copian desde el PDF, a veces salen como raya larga y el comando falla.

Los informes van a `~/pentesting/`, no dentro del repo.

## Antares

Lee el fuente. No levanta SecureShop. El paquete es `cisco-antares-cli`. Pide Python 3.11 o más, y lo trae `uv`. El `python3` del Mac puede seguir en 3.9: Antares no lo usa.

```bash
python3 --version
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
uv --version
uv tool install cisco-antares-cli
antares --version
```

`uv --version` muestra un número. `antares --version` muestra `antares-cli 0.1.0` o más nueva. Si en otra terminal `uv` no aparece, repitan la línea del `PATH`.

`plan` corre en la máquina y no necesita el modelo. `query` y `sweep` sí: hablan con un servidor local.

Hay dos modelos, `antares-350m` (unos 705 MB) y `antares-1b`. La ficha en Hugging Face está cerrada.

1. Entren a Hugging Face y acepten la ficha de [antares-350m](https://huggingface.co/fdtn-ai/antares-350m).
2. Creen un token de lectura en https://huggingface.co/settings/tokens. No lo peguen en un chat.
3. En la terminal: `hf auth login`, y ahí escriben el token cuando lo pida.

El servidor que Cisco probó es vLLM y pide una GPU NVIDIA. En un Mac ese `vllm serve` no arranca. La ruta válida, cuando haya endpoint, termina en `/v1/completions` y el identificador es `antares-350m`. En la sala ese endpoint ya responde en el puerto 8000 de la máquina de la cátedra.

Comprobar, si el modelo está arriba:

```bash
curl -s http://127.0.0.1:8000/health
```

Tiene que imprimir `"status": "ok"`.

Guía corta de Cisco: https://github.com/cisco-foundation-ai/cookbook/blob/main/1_quickstarts/Quickstart_Antares.md

## OWASP ZAP

Ventana de escritorio. La versión de la guía de clase es la **2.17.0**. Se baja de https://www.zaproxy.org/download/.

| Máquina | Qué bajar |
|---|---|
| Mac con chip Apple | macOS Apple Silicon (aarch64). El instalador ya trae Java |
| Mac Intel | macOS Intel (amd64) |
| Windows | instalador de 64 bits. Hace falta Java 17 aparte |
| Linux | el paquete de la página. Hace falta Java 17 aparte |

En el Mac, el chip se ve en manzana → Acerca de este Mac.

Ábranlo desde Descargas. Licencia: Accept. Tipo: **Standard**. Finish. Si macOS dice que el desarrollador no está verificado: Cancelar, luego Ajustes del Sistema → Privacidad y seguridad, al final Abrir de todas formas. Busquen ZAP en Aplicaciones, ábranlo y acepten la licencia de arranque. Déjenlo abierto.

Para este curso el modo de la barra es **Protected** (el escaneo activo solo contra los sitios marcados). Safe se puede usar si solo quieren mirar sin atacar. No se apunta a un host que no sea `127.0.0.1`.

Primer uso: https://www.zaproxy.org/getting-started/ · escritorio: https://www.zaproxy.org/docs/desktop/
