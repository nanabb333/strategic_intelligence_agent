#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$ROOT_DIR"

clear
echo
echo "Strategic Intelligence Decision Companion"
echo
echo "Preparing local launch..."
echo

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 is required to launch this product."
  echo "Install Python 3, then double-click this launcher again."
  echo
  echo "Press any key to close this window."
  read -r -n 1
  exit 1
fi

python3 launch.py

echo
echo "Decision Workspace stopped."
echo "Press any key to close this window."
read -r -n 1
