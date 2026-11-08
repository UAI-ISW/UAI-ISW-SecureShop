#!/usr/bin/env bash
# Levanta la API (:5001) y la aplicación (:5002). Ctrl-C detiene las dos.
set -euo pipefail
cd "$(dirname "$0")/SecureShop"

if [ ! -x .venv/bin/python ]; then
  echo "Creando entorno virtual (.venv)…"
  rm -rf .venv
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Creé .env desde .env.example."
fi

echo "▶ API          → http://127.0.0.1:5001"
python api.py &
API_PID=$!
sleep 2
echo "▶ Aplicación   → http://127.0.0.1:5002/login   (admin / colocolo)"
python secureshop.py &
APP_PID=$!

echo ""
echo "Entrá por el login. Ctrl-C para detener."
trap 'echo; echo "Deteniendo…"; kill "$API_PID" "$APP_PID" 2>/dev/null || true' INT TERM
wait
