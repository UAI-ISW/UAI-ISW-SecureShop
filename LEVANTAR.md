# Levantar SecureShop · Seguridad TI

Este archivo es del curso de Seguridad TI. `./run-local.sh` deja la API y la tienda listas para Antares (con la app apagada, antes de este script) y para ZAP (con este script abierto). ISW no lo usa: levanta cada proceso a mano, en [`ISW/README.md`](ISW/README.md).

Sirve si bajaste la rama `main` como ZIP y vas a usar la terminal.

Hace falta Python 3.10 o más (`python3 --version`).

## 1. Descomprimir y entrar

El ZIP se llama `UAI-ISW-SecureShop-main.zip`. Al abrirlo queda una carpeta con ese nombre.

```bash
cd ~/Downloads/UAI-ISW-SecureShop-main
chmod +x run-local.sh
./run-local.sh
```

Si el ZIP quedó en otro lado, `cd` a esa carpeta. Tiene que verse el archivo `run-local.sh` al hacer `ls`.

La terminal se queda abierta. Ahí aparecen la API en el puerto 5001 y la tienda en el 5002. Para bajar las dos: Ctrl-C.

## 2. Entrar

En el navegador: http://127.0.0.1:5002/login

Usuario `admin`, clave `colocolo`. Quedás en la tienda.

## 3. Inscribir una mascota

En la barra, **Inscribir**. Completá con datos ficticios, por ejemplo:

| Campo | Valor |
|---|---|
| Nombre | Luna |
| RUT del dueño | 12.345.678-9 |
| Chip | 9988 |
| Edad | 3 |
| Color | blanco |
| Tipo | Gato |

La foto es opcional. **Registrar**. Tiene que decir que la mascota quedó registrada y mostrar la fila en Estadísticas.

## 4. Comprar un collar

En la barra, **Tienda**. En **Collar para perro**, **Agregar al carrito**.

En el carrito el total es $5.000. **Finalizar compra**. Volvés a la tienda con el aviso de que el pago lo autorizó el stub de Webpay. No sale a Transbank.

## Después de tenerlo arriba

El reporte de lo que falló en Antares y en ZAP se junta en [`seguridad-ti/reporte.md`](seguridad-ti/reporte.md). Antares se corre con esta tienda apagada. ZAP se corre con esta terminal todavía abierta.

## Si no parte

Puerto ocupado: `lsof -i :5001 -i :5002` y cerrá esos procesos. Si el login rechaza `colocolo`, borrá `SecureShop/secure_shop.db` y volvé a correr `./run-local.sh`.
