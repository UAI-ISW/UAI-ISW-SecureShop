# Seguridad TI

Esta carpeta es el curso de hacking ético. Se trabaja con el ZIP de la rama `main` y con la terminal.

| Archivo | Para qué |
|---|---|
| [`../LEVANTAR.md`](../LEVANTAR.md) | `./run-local.sh` deja la API y la tienda listas |
| [`antares.md`](antares.md) | Modelo y `sweep`, con la app apagada |
| [`zap.md`](zap.md) | Dejar ZAP entre el navegador y los dos puertos |
| [`casos.md`](casos.md) | Los diez casos: id, objetivo, entrada, procedimiento, salida esperada |
| [`casos.sh`](casos.sh) | El mismo caso, por terminal |
| [`reporte.md`](reporte.md) | Dónde quedan el informe de Antares y el de ZAP |
| [`hallazgos.md`](hallazgos.md) | Foto del código anterior. Los casos que se corren hoy son los de `casos.md` |
| [`antares-zap.png`](antares-zap.png) | Antares con la app apagada. ZAP entre el navegador y los puertos |

ISW es la otra carpeta. Allá cada proceso se levanta con su comando. Acá el arranque es el script.

Alcance: solo `127.0.0.1`, puertos 5001 y 5002. Los informes van a `~/pentesting/`, nunca dentro del repo. T01–T06 siguen abiertos.

## Orden

1. Antares, con la app apagada: [`antares.md`](antares.md). El reporte queda en `~/pentesting/SAST/sweep-owasp/report.md`.
2. Encender con `./run-local.sh`: [`../LEVANTAR.md`](../LEVANTAR.md). Esa terminal queda abierta.
3. Abrir ZAP: [`zap.md`](zap.md). Correr [`casos.md`](casos.md).
4. Juntar los dos informes: [`reporte.md`](reporte.md).

```bash
./seguridad-ti/casos.sh a01
```

`./seguridad-ti/casos.sh` sin argumento lista los diez. `./seguridad-ti/casos.sh todos` los corre uno detrás de otro.
