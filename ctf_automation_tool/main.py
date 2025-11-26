# main.py
import socket
from utils.solver import solve_challenge

HOST = "127.0.0.1"
PORT = 5000

buf = ""

with (socket.create_connection((HOST, PORT)) as s):
    try:
        while True:
            data = s.recv(4096).decode(errors='ignore')
            if not data:
                continue
            if "[Challenge" in data:  # new challenge - resets buffer
                buf = data
            else:
                buf += data
            print("[SERVER]", data, end='', flush=True)

            # Ignore flag messages
            if "flag" in data.lower() or "CTF{" in data:
                continue

            # challenge solving
            ans = solve_challenge(buf)
            if ans != "UNKNOWN":
                print("[SENT]", ans)
                s.sendall((ans + "\n").encode())
                buf = ""
    except KeyboardInterrupt:
        print("\n[Stop]")

