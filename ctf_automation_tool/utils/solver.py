# utils/solver.py
import re
import base64


def solve_challenge(text):
    """
    Rezolvă challenge-uri pe baza textului primit
    """
    # Take only the last line with challenge (avoid accumulation)
    lines = text.strip().split('\n')
    current_challenge = lines[-1] if lines else text


    # Binary AND: "Binary AND: 10110101 AND 11001100 = ?"
    if "Binary AND:" in current_challenge:
        match = re.search(r'Binary AND:\s*(\d+)\s+AND\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)  # Convert from binary to decimal
            b = int(match.group(2), 2)
            result = a & b
            return bin(result)[2:]  # return without 0b

    # Binary OR: "Binary OR: 10110101 OR 11001100 = ?"
    if "Binary OR:" in current_challenge:
        match = re.search(r'Binary OR:\s*(\d+)\s+OR\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)
            b = int(match.group(2), 2)
            result = a | b
            return bin(result)[2:]

    # Binary XOR: "Binary XOR: 10110101 XOR 11001100 = ?"
    if "Binary XOR:" in current_challenge:
        match = re.search(r'Binary XOR:\s*(\d+)\s+XOR\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)
            b = int(match.group(2), 2)
            result = a ^ b
            return bin(result)[2:]

    # Binary NOR: "Binary NOR (8-bit): 10110101 NOR 11001100 = ?"
    if "Binary NOR" in current_challenge:
        match = re.search(r'Binary NOR.*?:\s*(\d+)\s+NOR\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)
            b = int(match.group(2), 2)
            result = ~(a | b) & 0xFF  # 8-bit mask
            return bin(result)[2:]

    # Binary NAND: "Binary NAND (8-bit): 10110101 NAND 11001100 = ?"
    if "Binary NAND" in current_challenge:
        match = re.search(r'Binary NAND.*?:\s*(\d+)\s+NAND\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)
            b = int(match.group(2), 2)
            result = ~(a & b) & 0xFF  # 8-bit mask
            return bin(result)[2:]

    # Binary NOT: "Binary NOT (8-bit): NOT 10110101 = ?"
    if "Binary NOT" in current_challenge:
        match = re.search(r'NOT\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)
            result = ~a & 0xFF  # 8-bit mask
            return bin(result)[2:]

    # Complex Logic: "Calculate: (1010 AND 1100) XOR 1111 = ?"
    if "Calculate:" in current_challenge and "AND" in current_challenge and "XOR" in current_challenge:
        # Extract binary numbers from expression
        match = re.search(r'\((\d+)\s+AND\s+(\d+)\)\s+XOR\s+(\d+)', current_challenge)
        if match:
            a = int(match.group(1), 2)
            b = int(match.group(2), 2)
            c = int(match.group(3), 2)
            result = (a & b) ^ c
            return bin(result)[2:]


    # Reverse string: "Reverse this string: hello"
    if "Reverse" in current_challenge:
        match = re.search(r'Reverse this string:\s*(\w+)', current_challenge)
        if match:
            return match.group(1)[::-1]

    # Hex to Decimal: "Convert hex to decimal: 0xb0"
    if "hex to decimal" in current_challenge:
        match = re.search(r'0x([0-9a-fA-F]+)', current_challenge)
        if match:
            return str(int(match.group(1), 16))

    # Base64: "Decode this base64: aGVsbG8="
    if "base64" in current_challenge:
        match = re.search(r'base64:\s*([A-Za-z0-9+/=]+)', current_challenge)
        if match:
            try:
                return base64.b64decode(match.group(1)).decode()
            except:
                pass

    # Math expression: "What is X + Y?" - Check the complete expression FIRST
    if "What is" in current_challenge:
        match = re.search(r'What is (.+)\?', current_challenge)
        if match:
            try:
                expression = match.group(1).strip()
                return str(eval(expression))
            except:
                pass

    # Addition : "45 + 32"
    if "+" in current_challenge and "What is" not in current_challenge:
        match = re.search(r'(\d+)\s*\+\s*(\d+)', current_challenge)
        if match:
            return str(int(match.group(1)) + int(match.group(2)))

    # Sequence: "Next number in sequence: 2, 4, 6, 8, ?"
    if "sequence" in current_challenge and "?" in current_challenge:
        numbers = re.findall(r'\d+', current_challenge)
        if len(numbers) >= 2:
            nums = [int(n) for n in numbers]
            diff = nums[-1] - nums[-2]
            return str(nums[-1] + diff)


    return "UNKNOWN"
