"""Cross-platform local launcher for Strategic Intelligence Decision Companion."""

from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"
HOST = os.environ.get("SIDC_HOST", "0.0.0.0")
PORT = os.environ.get("SIDC_PORT", "80")
PYTHON = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def print_launch_message() -> None:
    """Print the product-facing startup message."""
    print()
    print("Strategic Intelligence Decision Companion")
    print()
    print("Launching...")
    print()
    print("Decision Workspace is ready.")
    print()
    print("Open")
    print()
    if PORT == "80":
        print("http://localhost")
    else:
        print(f"http://localhost:{PORT}")
    print()


def ensure_virtual_environment() -> None:
    """Create the local virtual environment if it does not exist."""
    if PYTHON.exists():
        return
    print("Preparing local application environment...")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)


def install_requirements() -> None:
    """Install requirements when core dependencies are unavailable."""
    check = subprocess.run(
        [str(PYTHON), "-c", "import fastapi, uvicorn"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if check.returncode == 0:
        return
    print("Installing local application requirements...")
    subprocess.check_call([str(PYTHON), "-m", "pip", "install", "-r", str(REQUIREMENTS)], cwd=ROOT)


def main() -> int:
    """Launch the local FastAPI application with product-facing wording."""
    if sys.version_info < (3, 10):
        print("Python 3.10 or newer is required.")
        return 1

    try:
        ensure_virtual_environment()
        install_requirements()
    except subprocess.CalledProcessError as exc:
        print("Could not prepare the local application environment.")
        print(f"Command failed with exit code {exc.returncode}.")
        return exc.returncode or 1

    print_launch_message()
    command = [
        str(PYTHON),
        "-m",
        "uvicorn",
        "app:app",
        "--host",
        HOST,
        "--port",
        PORT,
        "--log-level",
        "warning",
    ]
    try:
        return subprocess.call(command, cwd=ROOT)
    except KeyboardInterrupt:
        print()
        print("Decision Workspace stopped.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
