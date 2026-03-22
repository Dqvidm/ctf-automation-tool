CTF Automation Toolset

Description:
This project is a modular automation suite designed to solve real-time computational and logical challenges during Capture The Flag (CTF) competitions. It utilizes a multi-threaded server-client architecture to handle high-speed data exchange and automated problem-solving over TCP/IP.

Key Features:
Automated Socket Communication: Implements a persistent TCP/IP connection with custom buffer management to handle fragmented network packets.
Dynamic Challenge Resolution: Automatically detects and solves multiple challenge types including Base64 decoding, hex-to-decimal conversion, and arithmetic sequences.
8-Bit Logical Processing: Support for complex bitwise operations (AND, OR, XOR, NAND, NOR, NOT) with 8-bit masking to simulate hardware-level logic.
Multi-threaded Server: A robust testing environment capable of handling multiple concurrent client connections.

Tech Stack
Language: Python 3.10+
Libraries: socket, threading, re (Regular Expressions), base64.
Concepts: Network Programming, Bitwise Logic, Multithreading, Regex Pattern Matching.

Project Structure:
ctf_automation_tool/
├── main.py              # Client entry point and socket coordinator
├── server.py            # Multi-threaded challenge generator
├── utils/
│   ├── parsers.py       # Data extraction using Regular Expressions
│   ├── solver.py        # Logic for resolving challenges
│   └── encoders.py      # Helper for data formatting
├── README.md            # Technical documentation
└── .gitignore           # Excludes __pycache__ and local environment files

Installation and Setup:
Clone the Repository:
git clone https://github.com/yourusername/ctf_automation_tool.git
cd ctf_automation_tool
Start the Server:

In one terminal, start the challenge environment:
python3 server.py

Run the Client:
In a separate terminal, execute the automation tool:
python3 main.py


Technical Highlights:
Regex-Based Parsing: Instead of simple string splitting, the project uses re.search patterns to accurately extract operands from unstructured server messages, ensuring robustness against formatting changes.

Bitwise Masking: Python integers are arbitrary-precision; this project implements & 0xFF masking to correctly simulate 8-bit NOR and NAND operations as expected in low-level CTF environments.

Stateful Buffering: The client uses a conditional buffer reset mechanism to prevent overlapping server messages from interfering with the logic of current challenges.
