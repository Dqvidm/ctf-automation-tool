import socket
import threading
import time
import random

HOST = "0.0.0.0"
PORT = 5000

# Challenge-uri simple
SIMPLE_CHALLENGES = [
    {
        "type": "math",
        "question": lambda: f"What is {random.randint(10, 100)} + {random.randint(10, 100)}?",
        "solver": lambda q: str(eval(q.split("What is ")[1].replace("?", "")))
    },
    {
        "type": "reverse",
        "question": lambda: f"Reverse this string: {random.choice(['hello', 'world', 'python', 'ctf', 'hacker'])}",
        "solver": lambda q: q.split("Reverse this string: ")[1][::-1]
    },
    {
        "type": "base64",
        "question": lambda: f"Decode this base64: aGVsbG8=",
        "solver": lambda q: "hello"
    },
    {
        "type": "sequence",
        "question": lambda: f"Next number in sequence: 2, 4, 6, 8, ?",
        "solver": lambda q: "10"
    },
    {
        "type": "hex",
        "question": lambda: f"Convert hex to decimal: {hex(random.randint(10, 255))}",
        "solver": lambda q: str(int(q.split("Convert hex to decimal: ")[1], 16))
    },
]

# Challenge-uri cu operații logice
LOGICAL_CHALLENGES = [
    {
        "type": "and",
        "question": lambda: (
            lambda a, b: (f"Binary AND: {bin(a)[2:]} AND {bin(b)[2:]} = ? (answer in binary, e.g., 1010)",
                          bin(a & b)[2:]))(random.randint(8, 255), random.randint(8, 255)),
        # solver not needed for tuple-style questions
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
    {
        "type": "or",
        "question": lambda: (
            lambda a, b: (f"Binary OR: {bin(a)[2:]} OR {bin(b)[2:]} = ? (answer in binary)", bin(a | b)[2:]))(
            random.randint(8, 255), random.randint(8, 255)),
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
    {
        "type": "xor",
        "question": lambda: (
            lambda a, b: (f"Binary XOR: {bin(a)[2:]} XOR {bin(b)[2:]} = ? (answer in binary)", bin(a ^ b)[2:]))(
            random.randint(8, 255), random.randint(8, 255)),
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
    {
        "type": "nor",
        "question": lambda: (lambda a, b: (f"Binary NOR (8-bit): {bin(a)[2:]} NOR {bin(b)[2:]} = ? (answer in binary)",
                                           bin(~(a | b) & 0xFF)[2:]))(random.randint(8, 255), random.randint(8, 255)),
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
    {
        "type": "nand",
        "question": lambda: (
            lambda a, b: (f"Binary NAND (8-bit): {bin(a)[2:]} NAND {bin(b)[2:]} = ? (answer in binary)",
                          bin(~(a & b) & 0xFF)[2:]))(random.randint(8, 255), random.randint(8, 255)),
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
    {
        "type": "complex_logic",
        "question": lambda: (
            lambda a, b, c: (f"Calculate: ({bin(a)[2:]} AND {bin(b)[2:]}) XOR {bin(c)[2:]} = ? (answer in binary)",
                             bin((a & b) ^ c)[2:]))(random.randint(8, 63), random.randint(8, 63),
                                                    random.randint(8, 63)),
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
    {
        "type": "not",
        "question": lambda: (
            lambda a: (f"Binary NOT (8-bit): NOT {bin(a)[2:]} = ? (answer in binary)", bin(~a & 0xFF)[2:]))(
            random.randint(8, 255)),
        "solver": lambda q: q[1] if isinstance(q, tuple) else None
    },
]

# Combină toate challenge-urile
CHALLENGES = SIMPLE_CHALLENGES + LOGICAL_CHALLENGES


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    try:
        conn.sendall(b"=== CTF Challenge Server ===\n")
        conn.sendall(b"Solve the challenges to get the flag!\n")
        conn.sendall(b"You have 12 challenges to complete.\n")
        conn.sendall(b"Hint: For binary operations, answer in binary format WITHOUT 0b (e.g., 1010).\n\n")
        time.sleep(0.2)

        correct_answers = 0
        total_challenges = 12

        for i in range(total_challenges):
            # 65% șanse pentru operații logice, 35% pentru altele
            if random.random() < 0.65:
                challenge = random.choice(LOGICAL_CHALLENGES)
            else:
                challenge = random.choice(SIMPLE_CHALLENGES)

            question_result = challenge["question"]()

            # Gestionează tuple (question, answer) pentru operații logice
            if isinstance(question_result, tuple):
                question, correct_answer = question_result[0], question_result[1]
            else:
                question = question_result
                # Ensure solver returns a string
                correct_answer = str(challenge["solver"](question))

            # Trimite challenge-ul
            msg = f"[Challenge {i + 1}/{total_challenges}] {question}\n"
            conn.sendall(msg.encode())
            print(f"[{addr}] Sent: {msg.strip()}")

            # Așteaptă răspuns
            try:
                data = conn.recv(4096)
                if not data:
                    print(f"[{addr}] Connection closed by client")
                    break
                data = data.decode(errors='ignore').strip()
            except socket.timeout:
                conn.sendall(b"Timeout waiting for answer. Moving to next challenge.\n\n")
                print(f"[{addr}] Timeout waiting for response")
                continue

            print(f"[{addr}] Received: {data} (Expected: {correct_answer})")

            if data == correct_answer:
                conn.sendall(b"Correct!\n\n")
                correct_answers += 1
            else:
                conn.sendall(f"Wrong! The answer was: {correct_answer}\n\n".encode())

            time.sleep(0.5)

        # Rezultat final
        conn.sendall(b"\n=== Results ===\n")
        result_msg = f"You solved {correct_answers}/{total_challenges} challenges!\n"
        conn.sendall(result_msg.encode())

        if correct_answers == total_challenges:
            flag = "CTF{YAMIL ANGURA LA U13, DA MA?}"

            conn.sendall(f"Here's your flag: {flag}\n\n".encode())
        elif correct_answers >= 5:
            conn.sendall(b"\nClose! You need all correct for the flag!\n")
        else:
            conn.sendall(b"\nTry again!\n")

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        try:
            conn.close()
        except Exception:
            pass
        print(f"[DISCONNECTED] {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"🚀 CTF Challenge Server started")
    print(f"📡 Listening on {HOST}:{PORT}")
    print(f"🎯 Waiting for connections...\n")
    print(f"📋 Available challenge types:")
    print(f"   - Math operations")
    print(f"   - String reversal")
    print(f"   - Base64 decode")
    print(f"   - Number sequences")
    print(f"   - Hex conversions")
    print(f"   - Logical operations (AND, OR, XOR, NOR, NAND) - 8-bit")
    print(f"   - Binary operations - 8-bit (without 0b prefix)")
    print(f"   - Complex logic chains\n")

    try:
        while True:
            conn, addr = server.accept()
            # optional: set a recv timeout per-client
            conn.settimeout(120)
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server stopping...")
    finally:
        server.close()


if __name__ == "__main__":
    start_server()
