# NOTICE — SecureShop

**Obra:** SecureShop (tienda + registro de mascotas, Flask).
**Contexto original:** material docente del curso TICS317, Universidad Adolfo Ibáñez (UAI).
**Titular / autoría docente:** Prof. Romina Torres (UAI).
**Uso:** educativo, en el marco de los cursos de Ingeniería de Software y Seguridad TI de la UAI.

Este repositorio se publica en la organización **UAI-ISW** como **proyecto base del curso**:
una aplicación real e intencionalmente imperfecta que los equipos analizan, auditan y
mejoran (empezando por seguridad).

## Datos y ejemplos

- `secure_shop.db` contiene **datos de ejemplo** (incluye un usuario `admin` de demostración
  con credenciales de juguete). No usar en producción ni con datos personales reales.
- Los formularios capturan RUT y chip de mascotas. En el ejercicio se tratan como **PII de
  ejemplo**; parte de la auditoría es precisamente evitar exponer estos datos.

## Licencia

**CC BY-NC-SA 4.0** (Atribución–NoComercial–CompartirIgual). Ver `LICENSE`.
Atribución requerida: *Romina Torres / Universidad Adolfo Ibáñez (UAI)*. Uso no comercial;
las obras derivadas deben mantener la misma licencia. Al ser obra propia de la UAI/docente,
no hay restricciones de terceros que impidan reutilizarla con fines educativos.
