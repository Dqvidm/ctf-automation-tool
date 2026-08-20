# CTF Network Automation & Live Telemetry

A full-stack Python automation suite engineered to intercept, parse, and solve low-level algorithmic and logical challenges in real-time over TCP/IP sockets during Capture The Flag (CTF) competitions.

## Features
- Real-Time Socket Orchestration: High-performance TCP/IP client-server communication with stateful stream buffer management and configurable timeouts.
- Live Telemetry Dashboard: Integrated FastAPI backend streaming real-time socket events, parsing telemetry, and live metrics over WebSockets to a modern dashboard.
- Safe Mathematical Evaluation: Secure expression evaluation powered by Python's Abstract Syntax Tree (`ast`) engine, completely preventing Remote Code Execution (RCE) vulnerabilities.
- 8-Bit Hardware Logic Simulation: Complete support for bitwise operations (`AND`, `OR`, `XOR`, `NOR`, `NAND`, `NOT`, and multi-operand chains) using strict `0xFF` masking.
- Regex-Based Payload Extraction: Regular expression parsing pipelines designed to isolate dynamic operands from raw TCP byte streams.
- Automated Unit Testing: Comprehensive test suite written with `pytest` covering all bitwise, AST arithmetic, and decoding routines.

## Project Structure

<img width="880" height="425" alt="image" src="https://github.com/user-attachments/assets/ec0987fc-6965-41f6-8818-1f84cf4c1684" />


**Tech Stack & Dependencies**
- Core: Python 3.10+
- Networking & Async: socket, threading, asyncio, websockets
- Web Framework: FastAPI, Uvicorn
- Parsing & Security: ast, re, operator, base64
- Testing: Pytest

**Installation & Setup**
1. Clone the repository:
Bash:
  git clone [https://github.com/](https://github.com/)<your-username>/ctf_automation_tool.git
  cd ctf_automation_tool

2. Install dependencies:
Bash:
  pip install -r requirements.txt

**Usage**
1. Start the Challenge Server
Bash:
  python server.py --host 127.0.0.1 --port 5000

2. Run with Web Dashboard (Recommended)
Bash:
  python app.py

Open http://127.0.0.1:8000 in your web browser and click START ENGINE.

3. Run via CLI Client
Bash:
  python main.py --host 127.0.0.1 --port 5000 --timeout 10.0

4. Run Unit Tests
Bash:
  pytest -v
