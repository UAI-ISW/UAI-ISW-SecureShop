# ZAP

ZAP se sienta entre el navegador y la aplicación encendida. Solo `127.0.0.1`, puertos 5002 y 5001. El modo de la barra es **Protected**. No se escanea otro host. El dibujo está en [`antares.md`](antares.md).

Los diez casos, con id, objetivo, entrada, procedimiento y salida esperada, están en [`casos.md`](casos.md). Esta página es solo cómo dejar ZAP listo para correrlos.

1. `./run-local.sh` queda abierto. Tienen que verse el 5001 y el 5002. El arranque está en [`../LEVANTAR.md`](../LEVANTAR.md).
2. ZAP 2.17.0, desde https://www.zaproxy.org/download/. En el Mac con Apple Silicon, el instalador aarch64. Modo **Protected**.
3. Quick Start → Manual Explore → `http://127.0.0.1:5002/login` → Launch Browser. Cuando `127.0.0.1` aparezca en Sites, **Include in Context**. Lo mismo con `http://127.0.0.1:5001`.
4. Cada caso de [`casos.md`](casos.md) se hace en ese navegador o con Manual Request Editor. Después se mira **History** y **Alerts**, y se llena la tabla Resultado del caso. Si ZAP no nombró una alerta, igual vale lo que se vio en la respuesta.
5. Al terminar los diez: Automated Scan de `http://127.0.0.1:5002` y, si queda tiempo, de `http://127.0.0.1:5001`. El HTML se guarda como `~/pentesting/DAST/zap-report.html`. Cada alerta se anota en el caso A01–A10 que le corresponda.

Cómo se junta con el reporte de Antares: [`reporte.md`](reporte.md).
