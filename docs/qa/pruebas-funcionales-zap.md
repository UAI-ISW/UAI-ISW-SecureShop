# Pruebas funcionales con OWASP ZAP

ZAP es la ventana de escritorio. La aplicación es una terminal que no se cierra. El recorrido se hace en el navegador que abre ZAP, para que cada caso tenga tráfico que leer.

Solo `127.0.0.1`, puertos **5002** (la aplicación: login, tienda, carrito, inscribir, estadísticas) y **5001** (la API). La guía del 4 nov todavía dice tienda en el 5003 y panel en el 5002. Esa separación ya no está. Si en Sites aparece otro host, no se escanea.

Instalación: [`instalacion.md`](instalacion.md). Qué hace cada modo: [`herramientas.md`](herramientas.md).

## 1. Levantar la aplicación

Si otra terminal tiene la variante MVC (`python app.py`), Ctrl-C. Desde la raíz del repo:

```bash
./run-local.sh
```

En el texto tienen que aparecer el 5001 y el 5002. Esa terminal se queda así. Ctrl-C, al final, baja los dos. El `.venv` y la base no se suben.

## 2. ZAP, antes de navegar

En la barra, el modo pasa de Standard a **Protected**. Pestaña **Quick Start**, **Manual Explore**, URL `http://127.0.0.1:5002/login`, **Launch Browser**.

Cuando `127.0.0.1` aparezca en **Sites**, clic derecho → **Include in Context** → **Default Context**. Repitan con `http://127.0.0.1:5001` para que la API entre al alcance.

## 3. Recorrer, en ese navegador

1. Entrá con `admin` / `colocolo`. Tiene que verse la tienda.
2. Agregar un producto. Abrir Carrito. El producto tiene que estar.
3. Inscribir una mascota de prueba (RUT y chip ficticios). Tiene que avisar que quedó registrada y mostrar la fila en estadísticas.
4. Salir.
5. Abrir `http://127.0.0.1:5001/mascotas`. Tiene que verse el JSON, con RUT y chip, sin haber vuelto a entrar.

## 4. Caso pasivo

Pestaña **Alerts**. Elijan una fila de la tienda o del login. Completen la ficha de abajo. Suele ser de cabecera o de cookie. Es una alerta que la herramienta levantó sin apretar Attack.

## 5. Caso a mano · la lista de mascotas

En **History**, abran el pedido del puerto 5001, ruta `/mascotas`, y lean la respuesta. La pregunta es si ZAP puso una fila en **Alerts** para esa URL.

El cuerpo trae RUT y chip, y ese pedido no pasó por el login. Si Alerts no tiene una fila para esa URL, la debilidad igual está: la vieron ustedes en History. Se contrasta con `api.py`. ZAP mostró el tráfico. El juicio lo pone la ficha.

## 6. Caso de escaneo

Sigan en Protected. Quick Start, **Automated Scan**, URL `http://127.0.0.1:5002`, botón Attack. Puede crear o cambiar datos de la base local. Al terminar: menú **Report**, formato HTML, carpeta `~/pentesting/DAST/`. Elijan **una** alerta y completen la ficha. Si queda tiempo, el mismo botón con `http://127.0.0.1:5001`. Un host que no sea `127.0.0.1` no se escanea.

## Ficha (una por caso, en `~/pentesting/DAST/`)

```text
Caso __  ·  pasivo / a mano / escaneo

Qué se quiere ver:
URL (solo 127.0.0.1):
Qué se hace en ZAP:
Dónde se mira:   Alerts / History / Report
¿ZAP nombró una alerta?   sí / no
Nombre y URL de la alerta:
Si no la nombró, qué se vio en la respuesta:
¿Vulnerabilidad, aviso, o mirado y no está?
```

«¿ZAP la nombró?» es sí solo cuando hay una fila en Alerts o en el reporte.
