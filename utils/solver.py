# utils/solver.py
from utils import encoders, parsers


def solve_challenge(text: str) -> str:
    """Dispatches the challenge line to the respective parsers and encoders."""
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    if not lines:
        return "UNKNOWN"

    challenge_line = lines[-1]

    # Binary Logic
    if "Binary AND" in challenge_line:
        operands = parsers.extract_binary_operation(challenge_line, "AND")
        if operands:
            return encoders.binary_and(*operands) or "UNKNOWN"

    if "Binary OR" in challenge_line:
        operands = parsers.extract_binary_operation(challenge_line, "OR")
        if operands:
            return encoders.binary_or(*operands) or "UNKNOWN"

    if "Binary XOR" in challenge_line:
        operands = parsers.extract_binary_operation(challenge_line, "XOR")
        if operands:
            return encoders.binary_xor(*operands) or "UNKNOWN"

    if "Binary NOR" in challenge_line:
        operands = parsers.extract_binary_operation(challenge_line, "NOR")
        if operands:
            return encoders.binary_nor(*operands) or "UNKNOWN"

    if "Binary NAND" in challenge_line:
        operands = parsers.extract_binary_operation(challenge_line, "NAND")
        if operands:
            return encoders.binary_nand(*operands) or "UNKNOWN"

    if "Binary NOT" in challenge_line:
        operand = parsers.extract_binary_not(challenge_line)
        if operand:
            return encoders.binary_not(operand) or "UNKNOWN"

    if "Calculate:" in challenge_line and "AND" in challenge_line and "XOR" in challenge_line:
        operands = parsers.extract_complex_logic(challenge_line)
        if operands:
            return encoders.complex_binary_logic(*operands) or "UNKNOWN"

    # Encoding / Classical
    if "Reverse" in challenge_line:
        word = parsers.extract_reverse(challenge_line)
        return encoders.reverse_string(word) if word else "UNKNOWN"

    if "hex to decimal" in challenge_line.lower():
        hex_val = parsers.extract_hex(challenge_line)
        return str(encoders.hex_to_decimal(hex_val)) if hex_val else "UNKNOWN"

    if "base64" in challenge_line.lower():
        b64_val = parsers.extract_base64(challenge_line)
        res = encoders.decode_base64(b64_val) if b64_val else None
        return res if res else "UNKNOWN"

    if "What is" in challenge_line:
        expr = parsers.extract_math(challenge_line)
        if expr:
            val = parsers.parse_safe_math(expr)
            return str(val) if val is not None else "UNKNOWN"

    seq = parsers.extract_sequence(challenge_line)
    if seq:
        diff = seq[-1] - seq[-2]
        return str(seq[-1] + diff)

    return "UNKNOWN"