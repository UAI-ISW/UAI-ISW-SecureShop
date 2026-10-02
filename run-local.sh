#!/usr/bin/env bash
# Levanta SecureShop (versión base/legado) en localhost.
# Uso:  ./run-local.sh      (Ctrl-C para detener los tres procesos)
set -euo pipefail
cd "$(dirname "$0")/SecureShop"

if [ ! -d .venv ]; then
  echo "Creando entorno virtual (.venv)…"
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

echo "▶ API de datos      → http://localhost:5001  (crea la BD e inserta admin)"
python api.py &            API_PID=$!
sleep 2
echo "▶ Panel / login     → http://localhost:5002"
python securesoftware.py & PANEL_PID=$!
echo "▶ Tienda            → http://localhost:5003"
python secureshop.py &     TIENDA_PID=$!

echo ""
echo "SecureShop levantado. Ctrl-C para detener."
trap 'echo; echo "Deteniendo…"; kill "$API_PID" "$PANEL_PID" "$TIENDA_PID" 2>/dev/null || true' INT TERM
wait
