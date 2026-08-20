# utils/encoders.py
import base64
import codecs
from typing import Optional, Union

BinaryInput = Union[str, int]


def hex_to_decimal(hex_string: str) -> int:
    """Converts a hex string to an integer."""
    hex_clean = hex_string.replace("0x", "").strip()
    return int(hex_clean, 16)


def decode_base64(encoded: str) -> Optional[str]:
    """Decodes a base64 string to utf-8."""
    try:
        return base64.b64decode(encoded.strip()).decode("utf-8")
    except Exception:
        return None


def decode_rot13(text: str) -> str:
    """Decodes a ROT13 encoded string."""
    return codecs.decode(text, "rot_13")


def reverse_string(text: str) -> str:
    """Reverses the given string."""
    return text[::-1]


def binary_to_int(binary_str: str) -> Optional[int]:
    """Converts a binary string to an integer."""
    try:
        return int(binary_str.replace("0b", "").strip(), 2)
    except (ValueError, TypeError):
        return None


def int_to_binary(num: int, remove_prefix: bool = True) -> str:
    """Converts an integer to a binary representation."""
    res = bin(num)
    return res[2:] if remove_prefix else res


def _normalize_binary_operands(a: BinaryInput, b: BinaryInput) -> tuple[Optional[int], Optional[int]]:
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b
    return num_a, num_b


def binary_and(a: BinaryInput, b: BinaryInput) -> Optional[str]:
    num_a, num_b = _normalize_binary_operands(a, b)
    if num_a is None or num_b is None:
        return None
    return int_to_binary(num_a & num_b)


def binary_or(a: BinaryInput, b: BinaryInput) -> Optional[str]:
    num_a, num_b = _normalize_binary_operands(a, b)
    if num_a is None or num_b is None:
        return None
    return int_to_binary(num_a | num_b)


def binary_xor(a: BinaryInput, b: BinaryInput) -> Optional[str]:
    num_a, num_b = _normalize_binary_operands(a, b)
    if num_a is None or num_b is None:
        return None
    return int_to_binary(num_a ^ num_b)


def binary_not(a: BinaryInput, bit_width: int = 8) -> Optional[str]:
    num_a = binary_to_int(a) if isinstance(a, str) else a
    if num_a is None:
        return None
    mask = (1 << bit_width) - 1
    return int_to_binary(~num_a & mask)


def binary_nand(a: BinaryInput, b: BinaryInput, bit_width: int = 8) -> Optional[str]:
    num_a, num_b = _normalize_binary_operands(a, b)
    if num_a is None or num_b is None:
        return None
    mask = (1 << bit_width) - 1
    return int_to_binary(~(num_a & num_b) & mask)


def binary_nor(a: BinaryInput, b: BinaryInput, bit_width: int = 8) -> Optional[str]:
    num_a, num_b = _normalize_binary_operands(a, b)
    if num_a is None or num_b is None:
        return None
    mask = (1 << bit_width) - 1
    return int_to_binary(~(num_a | num_b) & mask)


def complex_binary_logic(a: BinaryInput, b: BinaryInput, c: BinaryInput) -> Optional[str]:
    num_a = binary_to_int(a) if isinstance(a, str) else a
    num_b = binary_to_int(b) if isinstance(b, str) else b
    num_c = binary_to_int(c) if isinstance(c, str) else c
    if None in (num_a, num_b, num_c):
        return None
    return int_to_binary((num_a & num_b) ^ num_c)