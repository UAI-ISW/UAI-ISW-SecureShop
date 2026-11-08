# Pruebas unitarias

El archivo es `SecureShop/tests/test_unidad.py`. Una prueba unitaria ejercita un componente solo. No levanta Flask, no abre el puerto 5001 ni el 5002, y no llama a otro componente para hacer el trabajo.

```bash
cd SecureShop && source .venv/bin/activate
python -m pytest tests/test_unidad.py -q
```

Cómo se juntan después está en [`../integracion/README.md`](../integracion/README.md). Esta página no repite esa estrategia.

## Qué cuenta como unidad acá

| Componente | Qué se le pasa | Qué no entra en la prueba |
|---|---|---|
| `Repositorio` | Una base temporal (`tmp_path`) | La API HTTP |
| `Carrito` | Un objeto `Carrito()` nuevo, o el del proceso cuando el caso es ese | La pantalla del carrito |
| `buscar` | Un id | Flask |
| `StubWebpay` | Un monto y un medio | El carrito y el botón Finalizar compra |

`_repo` crea la base, carga el usuario `admin` / `colocolo` y devuelve el repositorio. Cada caso válido o inválido de datos usa la suya. No comparten filas.

Un caso válido afirma el comportamiento que el componente debe cumplir. Un caso inválido afirma que la entrada mala no se disfraza de éxito: clave que no calza, id que no existe, monto que no se puede cobrar.

## Repositorio · datos

| Prueba | Qué demuestra |
|---|---|
| `test_valido_clave_correcta` | `admin` / `colocolo` pasa |
| `test_invalido_clave_incorrecta` | La misma cuenta con otra clave no pasa |
| `test_invalido_usuario_que_no_existe` | Un nombre que no está en la tabla no pasa |
| `test_valido_la_clave_queda_como_hash_con_salt` | En la fila no está `colocolo`. El texto parte `pbkdf2:sha256`, y tiene salt y hash. Aun así la clave demo verifica |
| `test_valido_registrar_y_listar_conserva_rut_y_chip` | El alta guarda y el listado devuelve RUT y chip. Sin foto, `tiene_imagen` es falso |
| `test_invalido_registrar_sin_nombre` | Falta un campo obligatorio y `registrar` lanza `KeyError`. Sigue así a propósito |
| `test_valido_leer_imagen` | Los bytes y el tipo que se guardaron son los que se leen |
| `test_invalido_leer_imagen_de_un_id_que_no_existe` | El id 999 devuelve vacío, no una excepción |

## Carrito y catálogo · lógica

| Prueba | Qué demuestra |
|---|---|
| `test_valido_agregar_suma_el_precio` | Un collar (id 1) deja el total en 5000 |
| `test_invalido_carrito_vacio_total_cero` | Sin productos el total es 0, y vaciar no falla |
| `test_valido_el_carrito_del_proceso_es_uno_solo` | `carrito_del_proceso` es la lista compartida. El caso fija ese comportamiento. El carrito por sesión es US-04 y no está hecho |
| `test_valido_buscar_producto` | El id 4 es el juguete para gato |
| `test_invalido_buscar_producto_que_no_existe` | El id 99 devuelve `None` |

## StubWebpay · lógica

La unidad no arma un carrito. Llama a `cobrar` directo.

| Prueba | Qué demuestra |
|---|---|
| `test_valido_stub_webpay_autoriza` | 5000 y medio `webpay` → `autorizado` |
| `test_invalido_stub_webpay_monto_cero` | 0 → `monto-invalido` |
| `test_invalido_stub_webpay_monto_negativo` | −1 → `monto-invalido` |
| `test_invalido_stub_webpay_rechazo` | 5000 y medio `rechazo` → `rechazado` |

Si una de estas falla, el defecto está en esa clase. No se depura la plantilla ni el puerto.
