# 04 · Product Backlog (MoSCoW)

Backlog inicial construido desde cero tras entender el sistema. Prioridad **MoSCoW**.

| ID | Historia (Como… quiero… para…) | Pts | MoSCoW | Estado |
|---|---|---|---|---|
| US-01 | Como administrador, quiero iniciar sesión con identidad verificable, para que solo yo acceda al panel | 5 | Must | Ready (DoR) |
| US-02 | Como administrador, quiero que `/estadisticas` exija sesión y rol, para no exponer datos personales | 3 | Must | Ready (DoR) |
| US-03 | Como encargada de datos, quiero validar RUT/edad/chip al registrar, para tener datos confiables | 5 | Should | Backlog |
| US-04 | Como dueña, quiero un carrito por sesión, para comprar accesorios | 8 | Could | Backlog |
| US-05 | Como equipo, queremos SSO con proveedor externo real | — | Won't (aún) | Backlog |

MoSCoW: **Must** (sin esto no sirve) · **Should** (importante) · **Could** (deseable) · **Won't** (fuera de alcance).

## Secuenciación

- **Sprint 1:** US-01 + US-02 (los dos *Must*) + chore de variables de entorno (H2).
- **Sprint 2:** US-03 (validación, H5), endurecer `debug`/CORS (H4).
- **Sprint 3:** US-04 (carrito por sesión) y mejoras de UX.
