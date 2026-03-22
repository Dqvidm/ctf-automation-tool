# utils/encoders.py
import base64
import codecs


def hex_to_binary(hex_string):
    """Convertește hex la binary"""
    hex_clean = hex_string.replace('0x', '')
    decimal = int(hex_clean, 16)
    return bin(decimal)[2:]


def hex_to_decimal(hex_string):
    """Convertește hex la decimal"""
    hex_clean = hex_string.replace('0x', '')
    return int(hex_clean, 16)


def decode_base64(encoded):
    """Decodează base64"""
    try:
        return base64.b64decode(encoded).decode()
    except:
        return None


def decode_rot13(text):
    """Decodează ROT13"""
    return codecs.decode(text, 'rot13')


def reverse_string(text):
    """Inversează un string"""
    return text[::-1]


# === OPERAȚII BINARE ===

def binary_to_int(binary_str):
    """
    Convertește string binar în int
    Args:
        binary_str: '11010101' sau '0b11010101'
    Returns:
        int (213)
    """
    binary_clean = binary_str.replace('0b', '')
    try:
        return int(binary_clean, 2)
    except ValueError:
        return None


def int_to_binary(num, remove_prefix=True):
    """
    Convertește int în string binar
    Args:
        num: număr întreg
        remove_prefix: dacă True, elimină '0b'
    Returns:
        '11010101' sau '0b11010101'
    """
    result = bin(num)
    return result[2:] if remove_prefix else result


def binary_to_hex(binary_str):
    """
    Convertește binar în hex
    Args:
        binary_str: '11010101'
    Returns:
        'd5' (fără 0x)
    """
    decimal = binary_to_int(binary_str)
    return hex(decimal)[2:] if decimal is not None else None


# === OPERAȚII LOGICE PE 8-BIT ===

def binary_and(a, b, bit_width=8):
    """
    Operație AND între două numere binare
    Args:
        a, b: string-uri binare ('11010101') sau int
        bit_width: lățimea în biți (default 8)
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b

    if num_a is None or num_b is None:
        return None

    result = num_a & num_b
    return int_to_binary(result)


def binary_or(a, b, bit_width=8):
    """
    Operație OR între două numere binare
    Args:
        a, b: string-uri binare sau int
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b

    if num_a is None or num_b is None:
        return None

    result = num_a | num_b
    return int_to_binary(result)


def binary_xor(a, b, bit_width=8):
    """
    Operație XOR între două numere binare
    Args:
        a, b: string-uri binare sau int
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b

    if num_a is None or num_b is None:
        return None

    result = num_a ^ num_b
    return int_to_binary(result)


def binary_not(a, bit_width=8):
    """
    Operație NOT pe un număr binar (cu mască pe bit_width)
    Args:
        a: string binar sau int
        bit_width: lățimea în biți (default 8)
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a

    if num_a is None:
        return None

    mask = (1 << bit_width) - 1  # 0xFF pentru 8-bit
    result = ~num_a & mask
    return int_to_binary(result)


def binary_nand(a, b, bit_width=8):
    """
    Operație NAND între două numere binare
    Args:
        a, b: string-uri binare sau int
        bit_width: lățimea în biți (default 8)
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b

    if num_a is None or num_b is None:
        return None

    mask = (1 << bit_width) - 1  # 0xFF pentru 8-bit
    result = ~(num_a & num_b) & mask
    return int_to_binary(result)


def binary_nor(a, b, bit_width=8):
    """
    Operație NOR între două numere binare
    Args:
        a, b: string-uri binare sau int
        bit_width: lățimea în biți (default 8)
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b

    if num_a is None or num_b is None:
        return None

    mask = (1 << bit_width) - 1  # 0xFF pentru 8-bit
    result = ~(num_a | num_b) & mask
    return int_to_binary(result)


def complex_binary_logic(a, b, c, bit_width=8):
    """
    Calculează (a AND b) XOR c
    Args:
        a, b, c: string-uri binare sau int
        bit_width: lățimea în biți (default 8)
    Returns:
        string binar fără '0b'
    """
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b
    num_c = binary_to_int(c) if isinstance(c, str) else c

    if num_a is None or num_b is None or num_c is None:
        return None

    result = (num_a & num_b) ^ num_c
    return int_to_binary(result)


# === FUNCȚII UTILITARE ===

def pad_binary(binary_str, width=8):
    """
    Adaugă zerouri la stânga pentru a ajunge la width biți
    Args:
        binary_str: '1010'
        width: 8
    Returns:
        '00001010'
    """
    return binary_str.zfill(width)


def binary_to_bytes(binary_str):
    """
    Convertește string binar în bytes
    Args:
        binary_str: '01001000' (H în ASCII)
    Returns:
        b'H'
    """
    # Împarte în grupuri de 8 biți
    byte_list = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]
    return bytes([int(byte, 2) for byte in byte_list])


def bytes_to_binary(data):
    """
    Convertește bytes în string binar
    Args:
        data: b'Hello'
    Returns:
        '0100100001100101011011000110110001101111'
    """
    return ''.join(format(byte, '08b') for byte in data)