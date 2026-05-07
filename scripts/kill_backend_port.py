import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect or stop a local backend port on Windows.")
    parser.add_argument("--port", type=int, default=8010, help="Port to inspect. Default: 8010.")
    parser.add_argument("--kill", action="store_true", help="Stop the detected PID. Without this flag, only prints PID.")
    args = parser.parse_args()

    rows = _netstat(args.port)
    pids = sorted({row[-1] for row in rows if row and row[-1].isdigit() and row[-1] != "0"})
    if not pids:
        print(f"No listening process found on port {args.port}.")
        return 0

    print(f"Port {args.port} appears to be used by PID(s): {', '.join(pids)}")
    if not args.kill:
        print("No process was killed. Re-run with --kill after confirming the PID is safe to stop.")
        return 0

    for pid in pids:
        subprocess.run(["taskkill", "/PID", pid, "/F"], check=False)
    return 0


def _netstat(port: int) -> list[list[str]]:
    completed = subprocess.run(["netstat", "-ano"], check=False, capture_output=True, text=True)
    rows: list[list[str]] = []
    marker = f":{port}"
    for line in completed.stdout.splitlines():
        if marker in line and "LISTENING" in line:
            rows.append(line.split())
    return rows


if __name__ == "__main__":
    sys.exit(main())
