#!/bin/bash

set -u

APP_URL="http://127.0.0.1:8000/dashboard/"
HEALTH_URL="http://127.0.0.1:8000/health"

cd "$(dirname "$0")" || exit 1

echo
echo "Strategic Intelligence Decision Companion"
echo "Starting local dashboard..."
echo
echo "Repository: $(pwd)"
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: python3 was not found."
  echo "Install Python 3, then run this launcher again."
  exit 1
fi

echo "Python: $(python3 --version)"

if ! python3 -m pip --version >/dev/null 2>&1; then
  echo "ERROR: pip is not available for this Python installation."
  echo "Install pip for Python 3, then run this launcher again."
  exit 1
fi

echo
echo "Installing or confirming local dependencies..."
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
  echo
  echo "ERROR: Dependency installation failed."
  exit 1
fi

open_dashboard() {
  echo
  echo "Opening dashboard:"
  echo "$APP_URL"

  if command -v open >/dev/null 2>&1; then
    open "$APP_URL"
  else
    echo "Open this URL in your browser:"
    echo "$APP_URL"
  fi
}

if python3 -c "import urllib.request; urllib.request.urlopen('$HEALTH_URL', timeout=1).read()" >/dev/null 2>&1; then
  echo
  echo "A local app is already responding on http://127.0.0.1:8000."
  open_dashboard
  echo
  echo "Using the existing local server."
  exit 0
fi

echo
echo "Starting FastAPI app on http://127.0.0.1:8000 ..."
python3 -m uvicorn app:app --host 127.0.0.1 --port 8000 &
SERVER_PID=$!

cleanup() {
  if kill -0 "$SERVER_PID" >/dev/null 2>&1; then
    echo
    echo "Stopping local app..."
    kill "$SERVER_PID" >/dev/null 2>&1
  fi
}

trap cleanup INT TERM EXIT

echo "Waiting for the local server to become ready..."
READY=0
for _ in {1..30}; do
  if ! kill -0 "$SERVER_PID" >/dev/null 2>&1; then
    echo
    echo "ERROR: The FastAPI server stopped before it became ready."
    echo "Check the terminal output above for details."
    exit 1
  fi

  if python3 -c "import urllib.request; urllib.request.urlopen('$HEALTH_URL', timeout=1).read()" >/dev/null 2>&1; then
    sleep 1
    if ! kill -0 "$SERVER_PID" >/dev/null 2>&1; then
      echo
      echo "ERROR: The FastAPI server stopped after the health check."
      echo "Check whether another app is already using port 8000."
      exit 1
    fi
    READY=1
    break
  fi

  sleep 1
done

if [ "$READY" -ne 1 ]; then
  echo
  echo "ERROR: The local server did not become ready within 30 seconds."
  echo "Check the terminal output above for details."
  exit 1
fi

open_dashboard

echo
echo "The local app is running. Keep this window open while reviewing."
echo "Press Control-C in this window to stop the app."
echo

wait "$SERVER_PID"
