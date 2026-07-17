"""Cross-platform local launcher for Strategic Intelligence Decision Companion."""

from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import venv
import webbrowser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv"
REQUIREMENTS = ROOT / "requirements.txt"
HOST = os.environ.get("SIDC_HOST", "127.0.0.1")
PORT = os.environ.get("SIDC_PORT", "8000")
PYTHON = VENV_DIR / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
LOCAL_URL = f"http://localhost:{PORT}"
HEALTH_URL = f"{LOCAL_URL}/health"


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
    print(LOCAL_URL)
    print()
    print("Press Ctrl+C to stop.")
    print()


def wait_for_server(timeout_seconds: float = 20.0) -> bool:
    """Wait briefly for the local app to answer health checks."""
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(HEALTH_URL, timeout=1.0) as response:
                if response.status == 200:
                    return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(0.35)
    return False


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
    print()
    print("Strategic Intelligence Decision Companion")
    print()
    print("Launching...")
    print()
    try:
        server = subprocess.Popen(command, cwd=ROOT)
        if wait_for_server():
            print_launch_message()
            webbrowser.open(LOCAL_URL)
        else:
            print("The local server is still starting.")
            print(f"Open: {LOCAL_URL}")
            print("If the page does not load, check the terminal output for errors.")
            print("Press Ctrl+C to stop.")
        return server.wait()
    except KeyboardInterrupt:
        print()
        print("Decision Workspace stopped.")
        if "server" in locals() and server.poll() is None:
            server.terminate()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
