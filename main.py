# main.py
import argparse
import socket
import sys
from utils.solver import solve_challenge


def run_client(host: str, port: int, timeout: float = 10.0) -> None:
    print(f"[*] Connecting to {host}:{port}...")
    try:
        with socket.create_connection((host, port), timeout=timeout) as s:
            print("[+] Connected to server.")
            buf = ""
            while True:
                data = s.recv(4096).decode("utf-8", errors="ignore")
                if not data:
                    print("[-] Server closed connection.")
                    break

                if "[Challenge" in data:
                    buf = data
                else:
                    buf += data

                print(f"[SERVER] {data}", end="", flush=True)

                if "CTF{" in data or "flag:" in data.lower():
                    print("\n[+] Flag captured successfully!")
                    break

                ans = solve_challenge(buf)
                if ans != "UNKNOWN":
                    print(f"\n[CLIENT] Sent: {ans}")
                    s.sendall(f"{ans}\n".encode("utf-8"))
                    buf = ""

    except (ConnectionRefusedError, socket.timeout) as err:
        print(f"[-] Network error: {err}")
    except KeyboardInterrupt:
        print("\n[*] Execution stopped by user.")


def main() -> None:
    parser = argparse.ArgumentParser(description="CTF Automation Socket Client")
    parser.add_argument("--host", default="127.0.0.1", help="Server host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Server port (default: 5000)")
    parser.add_argument("--timeout", type=float, default=10.0, help="Socket timeout in seconds")
    args = parser.parse_args()

    run_client(args.host, args.port, args.timeout)


if __name__ == "__main__":
    main()