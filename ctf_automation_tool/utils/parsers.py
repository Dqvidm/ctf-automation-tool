# utils/parsers.py
import re

def extract_hex(text):
    """Extracts hex value from text"""
    match = re.search(r'(0x)?([0-9a-fA-F]+)', text)
    return match.group(2) if match else None

def extract_numbers(text):
    """Extracts all numbers from text"""
    return [int(n) for n in re.findall(r'\d+', text)]

def extract_word_after_keyword(text, keyword):
    """Extracts the word after a keyword (e.g., 'Reverse: hello')"""
    match = re.search(rf'{keyword}[:\s]+(\w+)', text, re.I)
    return match.group(1) if match else None

def extract_base64(text):
    """Extracts base64 string from text"""
    match = re.search(r'([A-Za-z0-9+/=]{4,})', text)
    return match.group(1) if match else None

def extract_math_expression(text):
    """Extracts mathematical expression"""
    match = re.search(r'What is (.+)\?', text)
    return match.group(1) if match else None

# === EXTRACTORS FOR BINARY LOGIC OPERATIONS ===

def extract_binary_operation(text, operation):
    """
    Extracts binary operands for logic operations
    Args:
        text: the challenge text
        operation: 'AND', 'OR', 'XOR', 'NOR', 'NAND'
    Returns:
        tuple (a, b) containing the binary numbers or None
    """
    pattern = rf'Binary {operation}.*?:\s*(\d+)\s+{operation}\s+(\d+)'
    match = re.search(pattern, text, re.I)
    if match:
        return (match.group(1), match.group(2))
    return None

def extract_binary_and(text):
    """Extracts operands for Binary AND"""
    return extract_binary_operation(text, 'AND')

def extract_binary_or(text):
    """Extracts operands for Binary OR"""
    return extract_binary_operation(text, 'OR')

def extract_binary_xor(text):
    """Extracts operands for Binary XOR"""
    return extract_binary_operation(text, 'XOR')

def extract_binary_nor(text):
    """Extracts operands for Binary NOR"""
    return extract_binary_operation(text, 'NOR')

def extract_binary_nand(text):
    """Extracts operands for Binary NAND"""
    return extract_binary_operation(text, 'NAND')

def extract_binary_not(text):
    """Extracts operand for Binary NOT"""
    match = re.search(r'NOT\s+(\d+)', text)
    return match.group(1) if match else None

def extract_complex_logic(text):
    """
    Extracts operands from complex expressions
    Example: "(1010 AND 1100) XOR 1111"
    Returns:
        tuple (a, b, c) or None
    """
    match = re.search(r'\((\d+)\s+AND\s+(\d+)\)\s+XOR\s+(\d+)', text)
    if match:
        return (match.group(1), match.group(2), match.group(3))
    return None

def binary_to_int(binary_str):
    """
    Converts binary string to int
    Args:
        binary_str: string with binary number (without 0b)
    Returns:
        int or None
    """
    try:
        return int(binary_str, 2)
    except (ValueError, TypeError):
        return None

def int_to_binary(num):
    """
    Converts int to binary string (without 0b)
    Args:
        num: integer
    Returns:
        binary string without 0b prefix
    """
    return bin(num)[2:]

def is_binary_challenge(text):
    """Checks if the challenge is a binary operation"""
    binary_keywords = ['Binary AND', 'Binary OR', 'Binary XOR',
                       'Binary NOR', 'Binary NAND', 'Binary NOT',
                       'Calculate:']
    return any(keyword in text for keyword in binary_keywords)

def get_challenge_type(text):
    """
    Detects the challenge type from text
    Returns:
        string containing the challenge type
    """
    if "Binary AND" in text:
        return "binary_and"
    elif "Binary OR" in text:
        return "binary_or"
    elif "Binary XOR" in text:
        return "binary_xor"
    elif "Binary NOR" in text:
        return "binary_nor"
    elif "Binary NAND" in text:
        return "binary_nand"
    elif "Binary NOT" in text:
        return "binary_not"
    elif "Calculate:" in text and "AND" in text and "XOR" in text:
        return "complex_logic"
    elif "Reverse" in text:
        return "reverse"
    elif "hex to decimal" in text:
        return "hex_to_decimal"
    elif "base64" in text:
        return "base64"
    elif "What is" in text:
        return "math"
    elif "sequence" in text:
        return "sequence"
    else:
        return "unknown"