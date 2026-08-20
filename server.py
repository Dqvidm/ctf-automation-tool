# server.py
import argparse
import random
import socket
import threading
import time


def generate_challenge() -> tuple[str, str]:
    chal_type = random.choice([
        "and", "or", "xor", "nor", "nand", "not", "complex",
        "math", "reverse", "hex", "seq"
    ])

    if chal_type == "and":
        a, b = random.randint(8, 255), random.randint(8, 255)
        return f"Binary AND: {bin(a)[2:]} AND {bin(b)[2:]} = ?", bin(a & b)[2:]
    if chal_type == "or":
        a, b = random.randint(8, 255), random.randint(8, 255)
        return f"Binary OR: {bin(a)[2:]} OR {bin(b)[2:]} = ?", bin(a | b)[2:]
    if chal_type == "xor":
        a, b = random.randint(8, 255), random.randint(8, 255)
        return f"Binary XOR: {bin(a)[2:]} XOR {bin(b)[2:]} = ?", bin(a ^ b)[2:]
    if chal_type == "nor":
        a, b = random.randint(8, 255), random.randint(8, 255)
        return f"Binary NOR (8-bit): {bin(a)[2:]} NOR {bin(b)[2:]} = ?", bin(~(a | b) & 0xFF)[2:]
    if chal_type == "nand":
        a, b = random.randint(8, 255), random.randint(8, 255)
        return f"Binary NAND (8-bit): {bin(a)[2:]} NAND {bin(b)[2:]} = ?", bin(~(a & b) & 0xFF)[2:]
    if chal_type == "not":
        a = random.randint(8, 255)
        return f"Binary NOT (8-bit): NOT {bin(a)[2:]} = ?", bin(~a & 0xFF)[2:]
    if chal_type == "complex":
        a, b, c = random.randint(8, 63), random.randint(8, 63), random.randint(8, 63)
        return f"Calculate: ({bin(a)[2:]} AND {bin(b)[2:]}) XOR {bin(c)[2:]} = ?", bin((a & b) ^ c)[2:]
    if chal_type == "math":
        a, b = random.randint(10, 99), random.randint(10, 99)
        return f"What is {a} + {b}?", str(a + b)
    if chal_type == "reverse":
        words = ["python", "socket", "binary", "buffer", "packet"]
        chosen = random.choice(words)
        return f"Reverse this string: {chosen}", chosen[::-1]
    if chal_type == "hex":
        val = random.randint(16, 255)
        return f"Convert hex to decimal: {hex(val)}", str(val)

    # seq
    start, step = random.randint(1, 10), random.randint(2, 5)
    seq = [start + step * i for i in range(4)]
    return f"Next number in sequence: {', '.join(map(str, seq))}, ?", str(seq[-1] + step)


def handle_client(conn: socket.socket, addr: tuple[str, int], total_rounds: int = 12) -> None:
    print(f"[+] Client {addr} connected.")
    try:
        conn.sendall(b"=== CTF Challenge Server ===\nSolve the challenges to get the flag!\n\n")
        correct = 0

        for i in range(total_rounds):
            question, expected = generate_challenge()
            conn.sendall(f"[Challenge {i + 1}/{total_rounds}] {question}\n".encode("utf-8"))

            data = conn.recv(4096).decode("utf-8", errors="ignore").strip()
            if not data:
                break

            if data == expected:
                conn.sendall(b"Correct!\n\n")
                correct += 1
            else:
                conn.sendall(f"Wrong! Expected: {expected}\n\n".encode("utf-8"))

            time.sleep(0.05)

        if correct == total_rounds:
            conn.sendall(b"Here's your flag: CTF{SOLVER_MASTER_2026}\n\n")
        else:
            conn.sendall(b"Try again!\n\n")
    except Exception as e:
        print(f"[-] Error handling {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Client {addr} disconnected.")


def start_server(host: str, port: int) -> None:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\n[*] Shutting down server.")
    finally:
        server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CTF Challenge Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind (default: 5000)")
    args = parser.parse_args()

    start_server(args.host, args.port)