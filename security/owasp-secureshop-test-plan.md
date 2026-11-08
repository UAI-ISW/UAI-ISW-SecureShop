# Plan de pruebas de seguridad — SecureShop (OWASP)

**Proyecto:** SecureShop (proyecto base ISW · UAI)
**Documento hermano:** [`owasp-secureshop-hallazgos.md`](owasp-secureshop-hallazgos.md) (hallazgos de la auditoría estática)
**Estándares de referencia:** OWASP **Top 10:2021** (clasificación de riesgo) · OWASP **WSTG v4.2** (*Web Security Testing Guide*, casos de prueba) · OWASP **ASVS** (criterios de verificación).
**Uso:** material docente (Prof. Romina Torres) · CC BY-NC-SA 4.0 · solo entornos de laboratorio autorizados.

---

## 1. Propósito y alcance

Este plan define **cómo se probó y cómo debe probarse** la seguridad de SecureShop en dos modos complementarios:

| Modo | Qué es | Con qué se hace | Estado |
|------|--------|-----------------|--------|
| **Estático (SAST)** | Auditoría **sin ejecutar** la app: lectura de código, configuración y datos sembrados. | Revisión manual de código + mapeo OWASP Top 10. | **Hecho** → hallazgos H1–H8 |
| **Dinámico (DAST)** | Pruebas **con la app en ejecución**: peticiones reales contra los endpoints. | OWASP ZAP + `curl`/`http` + scripts. | **Pendiente** → este plan lo especifica |

**En alcance:** la aplicación que usamos, `SecureShop/secureshop.py` (`:5002`) y `SecureShop/api.py` (`:5001`), sus plantillas y `secure_shop.db`. `SecureShopRefactorizadoMVC/` no se prueba: no es la app de esta entrega.

**Fuera de alcance:** infraestructura de despliegue real, pruebas de estrés/DoS, ingeniería social, y cualquier sistema que **no** sea la instancia local de laboratorio. **No** se prueban sistemas de terceros ni entornos productivos.

---

## 2. Ambiente de prueba (identificado)

> **Regla:** todas las pruebas corren en una instancia **local y aislada**, con **datos sintéticos**. Nunca contra un despliegue real ni con PII real (Ley 21.719).

### 2.1 Topología

```
[Tester / OWASP ZAP :8080]
        │  (proxy HTTP)
        ▼
┌──────────────────── host local (127.0.0.1) ────────────────────┐
│  secureshop.py :5002                    api.py :5001            │
│  login, tienda, carrito,                API de mascotas + CORS  │
│  inscribir, estadísticas                       │                │
│            └──────────── HTTP ─────────────────┘                │
│                                                    ▼             │
│                                           SQLite: secure_shop.db │
└──────────────────────────────────────────────────────────────────┘
```

### 2.2 Componentes y superficie de ataque

| Componente | Puerto | Endpoints expuestos | Notas de seguridad |
|------------|--------|---------------------|--------------------|
| `api.py` | `:5001` | `POST /registrar_mascota` · `GET /mascotas` | Sin auth · `CORS(app)` abierto · devuelve PII (rut, chip) |
| `secureshop.py` | `:5002` | `/login` · `/` · `/carrito` · `/inscribir` · `/estadisticas` · `/logout` | La tienda y estadísticas exigen sesión. La API no |

### 2.3 Datos de prueba (sandbox)

- **Cuenta sembrada:** `admin` / `colocolo` (credencial de laboratorio, no secreto real).
- **Registros de mascotas:** usar RUT/chip **ficticios** (p. ej. `11.111.111-1`, chip `CHIP-TEST-001`). Prohibido cargar datos de personas o mascotas reales.

### 2.4 Prerrequisitos y puesta en marcha

```bash
./run-local.sh
# API :5001 y aplicación :5002. Entrar por http://127.0.0.1:5002/login
```

### 2.5 Estado limpio / reset entre corridas

```bash
# Detener procesos y regenerar BD desde cero (borra datos de la corrida anterior)
rm -f SecureShop/secure_shop.db
python SecureShop/api.py   # vuelve a crear tablas + admin
```

### 2.6 Aislamiento

- Ejecutar en máquina/VM/contenedor del alumno, sin exponer los puertos a Internet.
- `debug=True` está activo en el código **a propósito** (es el hallazgo H5); no navegar con esa instancia fuera del laboratorio.

---

## 3. Cómo se hizo la auditoría estática (SAST) — reproducible

Procedimiento aplicado (todo por **lectura de código**, sin ejecutar):

1. **Inventario de superficie:** listar rutas/decoradores `@app.route` en los 3 archivos y clasificarlas por sensibilidad (autenticadas vs públicas).
2. **Rastreo de datos sensibles:** seguir `rut`, `chip`, `password` desde el input hasta la BD y la respuesta (¿se hashea?, ¿se expone?).
3. **Revisión de identidad/sesión:** verificar si `login` crea sesión/token y si las rutas sensibles la exigen.
4. **Revisión de configuración:** buscar `debug=True`, `secret_key` hardcodeada, `CORS(app)`, credenciales sembradas.
5. **Chequeo de inyección/XSS:** confirmar consultas parametrizadas (`?`) y autoescape de Jinja2.
6. **Mapeo a OWASP Top 10:2021** y asignación de severidad → tabla de hallazgos H1–H8.

**Herramientas opcionales para automatizar el SAST** (recomendadas para el curso):

| Herramienta | Qué detecta aquí |
|-------------|------------------|
| `bandit -r SecureShop/` | `debug=True`, secretos hardcodeados, SQL construida por concatenación, uso inseguro. |
| `pip-audit` / `safety` | Vulnerabilidades conocidas en dependencias (`requirements.txt`). |
| `semgrep --config p/flask` | Patrones inseguros específicos de Flask. |
| `gitleaks detect` | Secretos filtrados en el historial git. |

---

## 4. Plan de pruebas dinámicas (DAST) — casos por hallazgo

Cada caso indica: **objetivo**, **OWASP** (Top 10 + WSTG), **pasos/PoC**, **evidencia esperada** y **criterio de resultado** (Pass = seguro / Fail = vulnerable). Hoy, con el código base, **se espera FAIL** en H1–H8; los mismos casos sirven de regresión cuando una remediación entre.

### TC-01 — Control de acceso roto en la API (H2)
- **OWASP:** A01:2021 · WSTG-ATHZ-02 (bypass del esquema de autorización).
- **Pasos:**
  ```bash
  curl -s http://localhost:5001/mascotas | jq .
  curl -s -X POST http://localhost:5001/registrar_mascota \
       -H "Content-Type: application/json" \
       -d '{"nombre":"Test","rut":"11.111.111-1","chip":"CHIP-TEST-001","edad":"2","color":"cafe","tipo":"perro"}'
  ```
- **Evidencia esperada:** ambas respuestas exitosas **sin ninguna credencial**.
- **Resultado:** *Fail* si un anónimo puede leer/insertar. *Pass* cuando devuelva `401/403` sin identidad válida.

### TC-02 — Exposición de PII sin autenticación (H4)
- **OWASP:** A01/A02:2021 · WSTG-ATHZ-01 · WSTG-CRYP-03 (información sensible).
- **Pasos:** `curl -s http://localhost:5001/mascotas` y abrir `http://localhost:5002/estadisticas` en el navegador.
- **Evidencia esperada:** `rut` y `chip` visibles para cualquiera.
- **Resultado:** *Fail* si se exponen; *Pass* con acceso autenticado + minimización/enmascarado de RUT.

### TC-03 — Autenticación decorativa / sin sesión (H3)
- **OWASP:** A04/A07:2021 · WSTG-ATHN-01 · WSTG-SESS-01 (esquema de gestión de sesión).
- **Pasos:**
  1. Acceder directo a `http://localhost:5002/estadisticas` **sin** pasar por `/login`.
  2. Hacer login válido e inspeccionar cookies/headers (¿se emite cookie de sesión o token?).
- **Evidencia esperada:** `/estadisticas` carga sin login; el login **no** setea sesión/token.
- **Resultado:** *Fail*. *Pass* cuando exista sesión/token con expiración y las rutas sensibles la exijan.

### TC-04 — Credenciales débiles / almacenamiento inseguro (H1)
- **OWASP:** A07:2021 · WSTG-ATHN-03 (política de credenciales) · WSTG-ATHN-07.
- **Pasos:**
  1. Login con `admin/colocolo`.
  2. Inspeccionar la BD: `sqlite3 SecureShop/secure_shop.db "select usuario,password from usuarios;"` → contraseña en claro.
  3. Probar ausencia de bloqueo por fuerza bruta (repetir logins fallidos).
- **Evidencia esperada:** password legible en claro; sin lockout ni rate-limit.
- **Resultado:** *Fail*. *Pass* con hash (bcrypt/argon2) y control de intentos. No guardar ninguna clave propia es US-05 y no está en esta entrega.

### TC-05 — Debugger de Werkzeug expuesto (H5)
- **OWASP:** A05:2021 · WSTG-ERRH-02 (stack traces) · WSTG-CONF-02.
- **Pasos:** provocar una excepción (p. ej. `POST /registrar_mascota` con JSON incompleto) y observar si aparece la consola interactiva de Werkzeug.
  ```bash
  curl -s -X POST http://localhost:5001/registrar_mascota \
       -H "Content-Type: application/json" -d '{"nombre":"solo-nombre"}'
  ```
- **Evidencia esperada:** traza detallada / debugger interactivo (riesgo de RCE con el PIN).
- **Resultado:** *Fail* con `debug=True`. *Pass* con `debug=False` y páginas de error genéricas.

### TC-06 — CORS abierto (H7)
- **OWASP:** A05:2021 · WSTG-CLNT-07 (Cross Origin Resource Sharing).
- **Pasos:**
  ```bash
  curl -s -I http://localhost:5001/mascotas -H "Origin: https://evil.example"
  ```
- **Evidencia esperada:** `Access-Control-Allow-Origin` refleja/permite cualquier origen.
- **Resultado:** *Fail* si permite `*`/orígenes arbitrarios; *Pass* con allowlist acotada.

### TC-07 — Secretos hardcodeados (H6)
- **OWASP:** A05/A07:2021 · WSTG-CONF-. (gestión de secretos).
- **Pasos:** confirmar en runtime que la `secret_key` y `admin/colocolo` provienen del código (no de variables de entorno). Cruce con `gitleaks`.
- **Resultado:** *Fail*. *Pass* cuando secretos vengan de entorno/gestor de secretos y no estén en el repo.

### TC-08 — Falta de registro/auditoría (H8)
- **OWASP:** A09:2021 · WSTG-. (logging & monitoring).
- **Pasos:** ejecutar TC-01..TC-06 y revisar si queda **algún** registro de accesos/operaciones sensibles.
- **Evidencia esperada:** sin logs de acceso a PII ni de login.
- **Resultado:** *Fail*. *Pass* con un registro de la acción, sin volcar el RUT (T06).

### TC-09 — Regresión: inyección SQL y XSS (no regresionar)
- **OWASP:** A03:2021 · WSTG-INPV-05 (SQLi) · WSTG-INPV-01 (XSS reflejado).
- **Pasos:** payloads `' OR '1'='1` en el login y `<script>alert(1)</script>` en campos del formulario `/inscribir`; observar en `/estadisticas`.
- **Evidencia esperada (deseada):** login no se evade (consultas parametrizadas) y el `<script>` aparece **escapado** (autoescape Jinja2).
- **Resultado:** *Pass* esperado hoy; el caso vigila que futuras refactorizaciones **no** introduzcan la falla.

---

## 5. Herramientas dinámicas (incluyendo enfoque GenAI)

### 5.1 OWASP ZAP — herramienta principal (la "que empieza por zap")

**OWASP ZAP** (*Zed Attack Proxy*) es el proxy de intercepción/scanner DAST de OWASP. Uso recomendado para SecureShop:

1. **Modo proxy manual + exploración:** configurar el navegador para usar ZAP (`127.0.0.1:8080`), navegar tienda/login/estadísticas para poblar el árbol de sitios.
2. **Spider / Ajax Spider:** descubrir rutas de la aplicación `:5002` y de la API `:5001`.
3. **Active Scan:** lanzar el escaneo activo contra `:5001` y `:5002` (detecta CORS, cabeceras faltantes, errores/stack traces, etc.).
4. **Automation Framework (repetible en CI):**

```yaml
# zap-secureshop.yaml  (ejecutar: zap.sh -cmd -autorun zap-secureshop.yaml)
env:
  contexts:
    - name: secureshop
      urls:
        - http://localhost:5001
        - http://localhost:5002
jobs:
  - type: spider
    parameters: { context: secureshop, maxDuration: 5 }
  - type: activeScan
    parameters: { context: secureshop }
  - type: report
    parameters:
      template: traditional-html
      reportFile: zap-report-secureshop
```

> Complementos útiles de ZAP: *OpenAPI/GraphQL add-ons* si se documenta la API; reglas de alerta para CORS y cabeceras de seguridad.

### 5.2 Enfoque GenAI (IA generativa en el pentest)

Hay dos usos distintos y ambos aplican al curso:

1. **IA como asistente del pentester (sobre esta app):**
   - Generar/expandir **casos de prueba** y payloads a partir de los hallazgos (este mismo plan puede ampliarse con un LLM).
   - **Triage** de los resultados de ZAP: pedir al modelo que priorice alertas, descarte falsos positivos y redacte remediaciones.
   - Add-ons/experimentos de ZAP que integran LLM para sugerir vectores; existen extensiones comunitarias que conectan ZAP con modelos. **Regla:** nunca pegar PII/secretos reales en un LLM externo; usar solo datos sandbox.

2. **Si más adelante la tienda incorpora un modelo de lenguaje:**
   - Aplicar **OWASP Top 10 for LLM Applications** (p. ej. *prompt injection*, fuga de datos, salida insegura) además del Top 10 web.
   - Añadir casos TC específicos de LLM en ese momento.

### 5.3 Alternativas / complementos

| Herramienta | Rol |
|-------------|-----|
| `curl` / HTTPie | PoC manual reproducible (usado en los TC). |
| **Nikto** | Escaneo rápido de configuración/servidor web. |
| **Nuclei** | Plantillas de detección (CORS, exposición de debug, cabeceras). |
| **sqlmap** | Confirmar (ausencia de) SQLi en login/inputs. |
| **Burp Suite Community** | Alternativa al proxy de ZAP. |
| **bandit / semgrep / pip-audit / gitleaks** | Refuerzan la parte **estática** (§3). |

---

## 6. Runbook de ejecución (orden sugerido)

1. Preparar ambiente (§2.4) y dejar BD limpia (§2.5).
2. Correr **PoC manuales** TC-01 … TC-09 con `curl`/navegador y guardar salida.
3. Levantar **OWASP ZAP**, ejecutar spider + active scan (§5.1) y exportar el reporte HTML.
4. (Opcional) Correr Nikto/Nuclei/sqlmap para complementar.
5. (Opcional) Usar GenAI para **triage** del reporte y borrador de remediaciones (§5.2).
6. Consolidar resultados en la **matriz de trazabilidad** (§7).
7. Reset del ambiente (§2.5).

---

## 7. Matriz de trazabilidad hallazgo → caso → resultado

| Hallazgo | OWASP 2021 | Caso dinámico | Resultado esperado (código base) | Resultado tras remediación |
|----------|------------|---------------|----------------------------------|----------------------------|
| H1 | A07 | TC-04 | Fail | Pass |
| H2 | A01 | TC-01 | Fail | Pass |
| H3 | A04/A07 | TC-03 | Fail | Pass |
| H4 | A01/A02 | TC-02 | Fail | Pass |
| H5 | A05 | TC-05 | Fail | Pass |
| H6 | A05/A07 | TC-07 | Fail | Pass |
| H7 | A05 | TC-06 | Fail | Pass |
| H8 | A09 | TC-08 | Fail | Pass |
| (no regresión) | A03 | TC-09 | Pass | Pass |

---

## 8. Criterios de aceptación (DoD de seguridad del sprint)

Un incremento de seguridad se considera **Hecho** cuando:

- [ ] TC-01..TC-08 pasan de *Fail* a **Pass** (o el riesgo residual queda documentado y aceptado por el PO).
- [ ] TC-09 sigue en **Pass** (sin regresiones de SQLi/XSS).
- [ ] Reporte de OWASP ZAP adjunto, con alertas altas/medias resueltas o justificadas.
- [ ] Cero PII real y cero secretos en el repo (verificado con `gitleaks`).
- [ ] Logging y trazabilidad de inscribir, sin volcar el RUT (T06). US-05, identidad sin clave propia, no es esta entrega.

---

## 9. Ética y límites

Pruebas **solo** sobre la instancia local autorizada del laboratorio. Prohibido escanear sistemas de terceros o de la universidad/municipalidad sin autorización escrita. Los datos deben ser sintéticos; cualquier PII real queda fuera por Ley 21.719 y por las reglas del piloto.
