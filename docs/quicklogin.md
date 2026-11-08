# Lab · QuickLogin en SecureShop

Ancla: **AwareLab / TICS331**. Lab siguiente, no es la línea de base de hoy. El dueño entraría por `http://127.0.0.1:5002/login` con Neuro-Access. El Flask no reimplementa KYC ni deja de tener el valor de relleno `admin` / `colocolo` hasta que este lab se haga.

Docs TAG: [Quick-Login](https://lab.tagroot.io/QuickLogin.md) · app [Android](https://play.google.com/store/apps/details?id=com.tag.NeuroAccess) / [iOS](https://apps.apple.com/app/neuro-access/id6478277647).

```
dueña (Neuro-Access) → escanea QR en :5002/login
    → Neuron verifica → Flask: session['usuario'] = jid  (sin password)
        → /  (la tienda; /estadisticas sigue en la misma app)
```

---

## 1. Que la app funcione (antes de tocar Flask)

1. Instalar **Neuro-Access** (Play / App Store). No el clone MAUI del Hands-On.
2. Crear cuenta (mail + teléfono). No pedir RUT real en el repo.
3. Humo **sin** SecureShop: abrir [lab.tagroot.io/QuickLogin.md](https://lab.tagroot.io/QuickLogin.md), escanear el QR. Si no firma, no sigan al código.
4. Foto de esa pantalla → evidencia (recortar el mail si hace falta).

Sin cuenta Neuron propia: usan `lab.tagroot.io`.

---

## 2. Cómo entra al aplicativo

El celular **no** habla con `127.0.0.1`. El QR es un `tagsign:` del Neuron. El browser muestra el QR; la app firma en TAG; el JS avisa; Flask crea la cookie.

Modo del lab: **web-client**. El equipo hace `POST /login/quicklogin` y **solo entonces** setea sesión. `/estadisticas` se protege en servidor (`@login_required` del S1 no se saca).

En localhost no hay HTTPS público (back-end mode TAG = Could / ngrok). Declararlo fake.

---

## 3. Código (rama `feat/us-ql-quicklogin`)

1. Rama desde `main`.
2. En `templates/login.html`: QR en el camino feliz; password fuera (flag `ALLOW_PASSWORD_LOGIN=0`).

```html
<meta name="NEURON" content="lab.tagroot.io">
<script src="https://lab.tagroot.io/Events.js"></script>
<script src="https://lab.tagroot.io/QuickLogin.js"></script>
<link rel="stylesheet" href="https://lab.tagroot.io/QuickLogin.css">

<div id="quickLoginCode"
     data-mode="image"
     data-purpose="Entrar al panel de mascotas SecureShop (lab TICS331). Válido 5 minutos.">
</div>
```

3. En `SignatureReceived`: `fetch('/login/quicklogin', {method:'POST', ...})` y redirect a `/`.
4. En `secureshop.py`: `POST /login/quicklogin` lee un id/JID, rechaza `{}`, setea `session['usuario']` y `session['rol']='admin'`. No comparar `colocolo`.
5. No cambiar `ApplicationId` (`com.tag.NeuroAccess`).

---

## 4. Aceptación

| Caso | Qué tiene que pasar |
|---|---|
| AC-QL-OK | Escaneo + firma → sesión → `/estadisticas` 200. Sin usuario/clave. |
| AI-EST-DIRECT | GET `/estadisticas` sin cookie → 302 a `/login`. |
| AI-QL-SIN-FIRMA | QR visible, nadie firma → sigue 302. |
| AI-QL-BODY-VACIO | POST `/login/quicklogin` `{}` → no hay sesión. |
| AI-PASSWORD-OFF | POST `/login` con `admin`/`colocolo` no abre el panel. |

pytest (sin celular): body vacío + sesión inyectada en el cliente Flask. El feliz es demo con la app, no un JWT inventado.

---

## 5. DoD

- [ ] Humo en lab.tagroot.io (foto).
- [ ] `/login` muestra QR; password fuera del camino feliz.
- [ ] AI-EST-DIRECT y AC-QL-OK en vivo.
- [ ] pytest de los casos sin celular, verdes.
- [ ] Sin PII real; `.env` no se sube.
- [ ] README: app + Neuron `lab.tagroot.io` + `./run-local.sh`.

Identidad (este lab) ≠ catálogo (chatbot) ≠ stock (ML). Un olor, un contrato, un PR.
