# Cómo funcionan Antares y ZAP, y cómo se usan acá

Son dos momentos. Una no reemplaza a la otra. El secreto escrito en un archivo se ve en el fuente. Una ruta que solo existe con la aplicación encendida se ve con ZAP.

```plantuml
@startuml
skinparam shadowing false
skinparam componentBorderColor #1F4E79

package "QA · el fuente, app apagada" {
  [Persona] --> [Antares]
  [Antares] --> [SecureShop/]
  note bottom of Antares
    plan elige CWE.
    query lista archivos.
    La línea la anota la persona.
  end note
}

package "Prueba funcional · app en 127.0.0.1" {
  [Navegador de ZAP] --> [ZAP :8080]
  [ZAP :8080] --> [secureshop.py :5002]
  [ZAP :8080] --> [api.py :5001]
  note bottom of ZAP
    Pasivo: lo que ya viajó.
    A mano: History de /mascotas.
    Activo: solo en Protected
    y solo contra 127.0.0.1.
  end note
}
@enduml
```

| | Antares | OWASP ZAP |
|---|---|---|
| Momento | El repo, antes de fusionar. La tienda apagada | La app encendida, solo en esta máquina |
| Pregunta | ¿En qué archivos miro este CWE? | ¿Qué alerta sale de esta URL? |
| Entrada | La carpeta `SecureShop/` y un CWE | `http://127.0.0.1:5002` y `:5001` |
| Salida | Archivos candidatos, informe Markdown o SARIF | Alertas del proxy y del escáner |
| Confirma | Quien abre el fuente y anota la línea | Quien lee History o Alerts y llena la ficha |
| Se le escapa | Lo que solo aparece al encender la app | La clave en el fuente y la lógica de negocio |

## Antares

Familia de modelos chicos de Cisco Foundation AI para **localizar** en un repositorio. La entrada es un CWE y la carpeta. El modelo busca en solo lectura. La salida es una lista ordenada de archivos, más el rastro. Los informes pueden ser `report.json`, `report.md` y `report.sarif`.

Tres comandos:

| Comando | Para qué |
|---|---|
| `plan` | Elige qué CWE tiene sentido en este repo. Corre en la máquina. No es un hallazgo |
| `query` | Investiga **un** CWE y propone archivos |
| `sweep` | Repite esa investigación para los CWE que eligió `plan` |

`plan --scope owasp` usa la vista empaquetada del OWASP Top 10. `--max-cwes 10` deja la mayoría afuera: que un CWE no aparezca no significa que lo haya descartado para siempre. `query` devuelve archivos, no la línea. El orden no es una probabilidad ni una gravedad.

`plan` no llama al modelo. `query` y `sweep` pueden mandar trozos de código al servidor donde corre el modelo. Solo se apunta a un repo que se tiene permiso de enviar, y el endpoint de esta clase es local (`127.0.0.1:8000`). No se manda el repositorio a un servicio de internet.

Tratar la lista como un pentest cerrado deja pasar lo que el modelo no abrió.

## ZAP

OWASP ZAP (Zed Attack Proxy) se sienta **entre el navegador y la aplicación**. Ve cada pedido y cada respuesta.

| Parte | Qué hace acá |
|---|---|
| Proxy | El navegador que abre ZAP pasa por el puerto 8080. Ahí se ve la cookie, la URL y el cuerpo |
| Pasivo | Mientras se recorre la tienda, anota lo que ya viajó (cabecera, cookie, formulario). No cambia los pedidos |
| Araña | Sigue enlaces y arma el mapa. Puede disparar una acción si está en un enlace |
| Activo | Lanza pruebas contra ese mapa. La propia guía de ZAP lo llama un ataque de prueba. Puede crear o cambiar datos de la base local |
| A mano | History del `GET /mascotas`. ZAP muestra el tráfico; el criterio lo pone la persona |

Modo **Safe**: solo lo inofensivo. Modo **Protected**: el activo solo contra los sitios incluidos en el contexto. En este curso el activo queda en Protected y el host es `127.0.0.1`.

Una alerta es un indicio. El control de acceso de la API (el JSON con RUT sin login) puede no salir como fila de Alerts: igual está, y se anota desde History. «Corrí ZAP y quedó limpio» cubre el mapa que vio y las pruebas automáticas. No cubre el permiso de cada objeto.

El escaneo activo contra un sitio de internet ajeno, sin permiso, es un ataque. Acá no se hace.
