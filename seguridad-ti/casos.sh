#!/usr/bin/env bash
# Casos OWASP Top 10:2021 contra la copia local. Solo 127.0.0.1.
# Uso: ./seguridad-ti/casos.sh a01
#      ./seguridad-ti/casos.sh todos

set -u

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

API="http://127.0.0.1:5001"
WEB="http://127.0.0.1:5002"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

arriba() {
  curl -sf -o /dev/null --max-time 3 "$API/mascotas" \
    && curl -sf -o /dev/null --max-time 3 "$WEB/login"
}

entrar() {
  local jar="$1"
  curl -s -c "$jar" -b "$jar" -o /dev/null \
    -X POST "$WEB/login" \
    --data 'usuario=admin&password=colocolo'
}

a01() {
  echo "== A01 Control de acceso roto =="
  echo "POST /registrar_mascota y GET /mascotas, sin cookie."
  curl -s -X POST "$API/registrar_mascota" \
    -H 'Content-Type: application/json' \
    -d '{"nombre":"CasoA01","rut":"1-9","chip":"CASO-A01","edad":"1","color":"gris","tipo":"Gato"}'
  echo
  curl -s "$API/mascotas" | python3 -c '
import json, sys
filas = json.load(sys.stdin)
propia = [f for f in filas if f.get("chip") == "CASO-A01"]
print("filas:", len(filas))
print("la fila trae rut:", bool(propia and "rut" in propia[-1]))
print("rut de juguete:", propia[-1]["rut"] if propia else "(no está)")
'
  echo "Anotá: el 5001 entregó el RUT sin sesión. La puerta web de estadísticas sí pide login."
}

a02() {
  echo "== A02 Fallas criptográficas =="
  echo "Set-Cookie del login:"
  curl -s -D - -o /dev/null -X POST "$WEB/login" \
    --data 'usuario=admin&password=colocolo' | grep -i '^set-cookie:'
  python3 - <<'PY'
import sqlite3
fila = sqlite3.connect("SecureShop/secure_shop.db").execute(
    "select password from usuarios where usuario = 'admin'"
).fetchone()
guardada = fila[0]
print("en la tabla empieza por:", guardada.split("$", 1)[0])
print("la celda es la palabra colocolo:", guardada == "colocolo")
PY
  echo "Anotá las dos: la cookie va en HTTP y no trae Secure. La celda no es la clave en claro."
}

a03() {
  echo "== A03 Inyección =="
  local nombre="Bobby' OR '1'='1"
  curl -s -X POST "$API/registrar_mascota" \
    -H 'Content-Type: application/json' \
    --data "$(python3 -c 'import json; print(json.dumps({"nombre":"Bobby'\'' OR '\''1'\''='\''1","rut":"1-9","chip":"CASO-A03","edad":"1","color":"negro","tipo":"Perro"}))')" \
    -o "$TMP/a03-alta.txt"
  echo "alta: $(cat "$TMP/a03-alta.txt")"
  curl -s "$API/mascotas" | python3 -c '
import json, sys
filas = json.load(sys.stdin)
propia = [f for f in filas if f.get("chip") == "CASO-A03"]
print("sigue siendo una lista:", isinstance(filas, list))
print("el nombre quedó como texto:", propia[-1]["nombre"] if propia else "(no está)")
'
  echo "Login con la misma comilla en el usuario:"
  curl -s -X POST "$WEB/login" \
    --data "usuario=admin%27%20OR%20%271%27%3D%271&password=x" \
    | python3 -c 'import sys; t=sys.stdin.read(); print("dice credenciales incorrectas:", "Credenciales incorrectas" in t)'
  echo "Anotá: en este MVP la consulta aguanta. El caso igual se lanza."
}

a04() {
  echo "== A04 Diseño inseguro =="
  local ja="$TMP/a.jar" jb="$TMP/b.jar"
  entrar "$ja"
  entrar "$jb"
  curl -s -b "$ja" -c "$ja" -o /dev/null -X POST "$WEB/comprar"
  curl -s -b "$ja" -c "$ja" -o /dev/null "$WEB/agregar/1"
  curl -s -b "$jb" -c "$jb" "$WEB/carrito" > "$TMP/carrito-b.html"
  if grep -q 'Collar para perro' "$TMP/carrito-b.html"; then
    echo "La sesión B ve «Collar para perro». B no llamó a /agregar."
  else
    echo "La sesión B no muestra el collar."
  fi
  echo "Anotá: el carrito es uno solo para el proceso. T04 sigue abierto."
}

a05() {
  echo "== A05 Configuración insegura =="
  local codigo
  codigo="$(curl -s -o "$TMP/a05.html" -w '%{http_code}' \
    -X POST "$API/registrar_mascota" \
    -H 'Content-Type: application/json' \
    -d '{}')"
  echo "POST vacío, código: $codigo"
  if grep -qi 'debugger' "$TMP/a05.html"; then
    echo "El HTML nombra al depurador. No abras la consola y no copies el PIN de la otra terminal."
  else
    echo "El HTML no nombra al depurador. Abrí el código de respuesta a mano si hace falta."
  fi
  rm -f "$TMP/a05.html"
  echo "CORS del listado:"
  curl -sI "$API/mascotas" | grep -i '^access-control-allow-origin:'
}

a06() {
  echo "== A06 Componentes vulnerables o viejos =="
  echo "requirements.txt:"
  cat SecureShop/requirements.txt
  echo "Flask que está corriendo esta copia:"
  if [[ -x SecureShop/.venv/bin/python ]]; then
    SecureShop/.venv/bin/python -m pip show Flask | awk '/^(Name|Version):/'
  else
    echo "No está SecureShop/.venv. Corré ./run-local.sh una vez y repetí este caso."
  fi
  echo "Anotá el número que pip muestra y que el archivo no lo fija. No hace falta explotar un CVE."
}

a07() {
  echo "== A07 Fallas de identificación =="
  if curl -s "$WEB/login" | grep -q 'admin / colocolo'; then
    echo "La página de login muestra admin / colocolo."
  else
    echo "La página de login no muestra esa frase."
  fi
  local i codigo
  for i in 1 2 3; do
    curl -s -o /dev/null -X POST "$WEB/login" --data 'usuario=admin&password=mala'
  done
  codigo="$(curl -s -o /dev/null -w '%{http_code}' -X POST "$WEB/login" \
    --data 'usuario=admin&password=colocolo')"
  echo "Después de 3 claves malas, la demo responde HTTP $codigo (302 es que sigue entrando)."
}

a08() {
  echo "== A08 Fallas de integridad =="
  printf 'no-es-una-imagen' > "$TMP/falso.bin"
  curl -s -X POST "$API/registrar_mascota" \
    -F 'nombre=CasoA08' -F 'rut=1-9' -F 'chip=CASO-A08' \
    -F 'edad=1' -F 'color=gris' -F 'tipo=Perro' \
    -F "imagen=@$TMP/falso.bin;type=image/png"
  echo
  local id
  id="$(curl -s "$API/mascotas" | python3 -c '
import json, sys
filas = json.load(sys.stdin)
propias = [f["id"] for f in filas if f.get("chip") == "CASO-A08"]
print(propias[-1] if propias else "")
')"
  if [[ -z "$id" ]]; then
    echo "No quedó la fila CASO-A08."
    return
  fi
  curl -s "$API/mascotas/$id/imagen" -o "$TMP/bajada.bin"
  echo "id $id, bytes guardados: $(cat "$TMP/bajada.bin")"
  echo "Anotá: el servidor confió en el tipo que mandó el cliente."
}

a09() {
  echo "== A09 Fallas de registro y monitoreo =="
  curl -s -X POST "$API/registrar_mascota" \
    -H 'Content-Type: application/json' \
    -d '{"nombre":"CasoA09","rut":"1-9","chip":"CASO-A09","edad":"1","color":"gris","tipo":"Gato"}'
  echo
  echo "Mirá la terminal donde sigue ./run-local.sh."
  echo "Tiene que verse la línea de acceso POST /registrar_mascota."
  echo "No tiene que verse una línea de auditoría de quién inscribió. T06 sigue abierto."
}

a10() {
  echo "== A10 SSRF =="
  local codigo
  codigo="$(curl -s -o "$TMP/a10.json" -w '%{http_code}' \
    "$API/mascotas?url=http://127.0.0.1:9/no-existe")"
  echo "código: $codigo"
  python3 -c '
import json
filas = json.load(open("'"$TMP/a10.json"'"))
print("sigue siendo el listado:", isinstance(filas, list), "filas", len(filas))
'
  echo "Anotá: el servidor no fue a buscar http://127.0.0.1:9/. En este MVP no hay un parámetro que dispare SSRF."
}

uso() {
  cat <<'EOF'
Uso: ./seguridad-ti/casos.sh <caso>

  a01  control de acceso roto
  a02  fallas criptográficas
  a03  inyección
  a04  diseño inseguro
  a05  configuración insegura
  a06  componentes vulnerables o viejos
  a07  fallas de identificación
  a08  fallas de integridad
  a09  fallas de registro y monitoreo
  a10  SSRF
  todos

La app tiene que estar en 127.0.0.1:5001 y :5002. El caso, con entrada y salida esperada: seguridad-ti/casos.md
EOF
}

main() {
  local caso="${1:-}"
  if [[ -z "$caso" || "$caso" == "-h" || "$caso" == "--help" ]]; then
    uso
    exit 0
  fi
  if ! arriba; then
    echo "No responde $API o $WEB. En otra terminal, desde la raíz: ./run-local.sh"
    exit 1
  fi
  case "$caso" in
    a01|A01) a01 ;;
    a02|A02) a02 ;;
    a03|A03) a03 ;;
    a04|A04) a04 ;;
    a05|A05) a05 ;;
    a06|A06) a06 ;;
    a07|A07) a07 ;;
    a08|A08) a08 ;;
    a09|A09) a09 ;;
    a10|A10) a10 ;;
    todos)
      a01; echo; a02; echo; a03; echo; a04; echo; a05; echo
      a06; echo; a07; echo; a08; echo; a09; echo; a10
      ;;
    *)
      uso
      exit 1
      ;;
  esac
}

main "${1:-}"
