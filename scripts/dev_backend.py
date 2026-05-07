import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the Japan AI Guide FastAPI dev backend.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8010)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    backend = root / "backend"
    python = backend / ".venv" / "Scripts" / "python.exe"
    executable = str(python) if python.exists() else sys.executable

    command = [
        executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--reload",
        "--host",
        args.host,
        "--port",
        str(args.port),
    ]
    print(f"Starting backend on http://{args.host}:{args.port}")
    print("If the port is busy, run: python scripts/kill_backend_port.py --port", args.port)
    return subprocess.call(command, cwd=backend)


if __name__ == "__main__":
    sys.exit(main())
