# Reporte de lo que falló

Acá se junta la entrega de Seguridad TI. Dos informes, los dos fuera del repo:

| Herramienta | App | Informe |
|---|---|---|
| Antares | Apagada | `~/pentesting/SAST/sweep-owasp/report.md` |
| ZAP | Encendida con `./run-local.sh` | `~/pentesting/DAST/zap-report.html` y las fichas de la misma carpeta |

Una fila cuenta como falla cuando la debilidad se vio. A03 y A10 pueden quedar en «no se observó»: eso también se entrega.

## 1. Antares

La tienda tiene que estar apagada. El recorrido del modelo está en [`antares.md`](antares.md). Al terminar el `sweep`, el archivo es este:

```text
~/pentesting/SAST/sweep-owasp/report.md
```

Ese es el reporte de Antares. Lista archivos candidatos, agrupados por CWE. No dice la línea y no prueba el puerto. Por cada CWE que el reporte nombra se agrega una ficha en la misma carpeta `~/pentesting/SAST/`:

```text
CWE:
Archivo que nombró report.md:
Línea que vi al abrir ese archivo en SecureShop/:
¿Quedó marcada la debilidad en el fuente?   sí / no
```

`report.md` más esas fichas es lo que se entrega de la prueba estática. Si `sweep` no escribió el archivo, el modelo no estaba en el puerto 8000: se repite desde el paso 2 de [`antares.md`](antares.md).

## 2. Encender, con el script

Ctrl-C si quedó algo del paso anterior. Desde la raíz del ZIP:

```bash
./run-local.sh
```

Esa terminal sigue abierta. Tienen que verse el puerto 5001 y el 5002. El detalle, el login y la compra del collar están en [`../LEVANTAR.md`](../LEVANTAR.md).

## 3. ZAP

Con esa terminal abierta se abren ZAP ([`zap.md`](zap.md)) y los diez casos ([`casos.md`](casos.md)). El resultado de cada caso va a `~/pentesting/DAST/`. En «sí / no» se marca lo que se vio.

Al final del mismo archivo está el Automated Scan. El HTML se guarda con este nombre:

```text
~/pentesting/DAST/zap-report.html
```

En ZAP: Report → Generate Report → Traditional HTML, y esa ruta. Cada alerta del HTML se anota junto al código A01–A10 de la ficha, o como alerta que no cae en ninguno.

## 4. Qué se entrega

```text
~/pentesting/SAST/sweep-owasp/report.md
~/pentesting/SAST/ficha-cwe-….txt
~/pentesting/DAST/zap-report.html
~/pentesting/DAST/ficha-a01.txt
…
~/pentesting/DAST/ficha-a10.txt
```

Nada de eso se copia al repo ni al chat. El formato del caso, y el mismo pedido por terminal, están en [`casos.md`](casos.md).
