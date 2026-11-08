# Plan Antares (SAST) — no verificado sobre la app que usamos

`plan-owasp.txt` es la selección corta (10 CWE). `plan-owasp-todos.txt` es el barrido de 246.

El propio informe cita evidencia en `controllers/carrito_controller.py`. Eso es `SecureShopRefactorizadoMVC/`, la variante que no usamos. La clase de Seguridad TI (`TICS413/.../11-04`) dice lo mismo: si el plan nombra el controlador MVC, no es el plan de `SecureShop/secureshop.py`.

No se re-corrió Antares después de unir login y tienda en el puerto 5002. Hasta eso, estos dos archivos son el insumo de la clase, no un hallazgo confirmado de la aplicación actual.

La lectura manual sigue en [`../owasp-secureshop-hallazgos.md`](../owasp-secureshop-hallazgos.md). Antares y ZAP sobre la app que usamos: [`../../docs/operacion.md`](../../docs/operacion.md). El plan dinámico largo, no ejecutado: [`../owasp-secureshop-test-plan.md`](../owasp-secureshop-test-plan.md).
