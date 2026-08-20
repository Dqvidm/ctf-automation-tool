# utils/parsers.py
import ast
import operator
import re
from typing import Optional, Tuple

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.FloorDiv: operator.floordiv,
}


def parse_safe_math(expression: str) -> Optional[int]:
    """Safely evaluates basic arithmetic expressions without using eval()."""
    def _eval_node(node: ast.AST) -> int:
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return int(node.value)
        if isinstance(node, ast.BinOp):
            left = _eval_node(node.left)
            right = _eval_node(node.right)
            op_type = type(node.op)
            if op_type in _OPERATORS:
                return _OPERATORS[op_type](left, right)
        raise ValueError("Unsupported operation")

    try:
        tree = ast.parse(expression.strip(), mode="eval")
        return _eval_node(tree.body)
    except Exception:
        return None


def extract_binary_operation(text: str, operation: str) -> Optional[Tuple[str, str]]:
    pattern = rf"Binary {operation}.*?:\s*([01]+)\s+{operation}\s+([01]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.groups() if match else None


def extract_binary_not(text: str) -> Optional[str]:
    match = re.search(r"NOT\s+([01]+)", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_complex_logic(text: str) -> Optional[Tuple[str, str, str]]:
    pattern = r"\(([01]+)\s+AND\s+([01]+)\)\s+XOR\s+([01]+)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.groups() if match else None


def extract_reverse(text: str) -> Optional[str]:
    match = re.search(r"Reverse this string:\s*(\S+)", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_hex(text: str) -> Optional[str]:
    match = re.search(r"0x([0-9a-fA-F]+)", text)
    return match.group(1) if match else None


def extract_base64(text: str) -> Optional[str]:
    match = re.search(r"base64:\s*([A-Za-z0-9+/=]+)", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_math(text: str) -> Optional[str]:
    match = re.search(r"What is (.+?)\?", text, re.IGNORECASE)
    return match.group(1) if match else None


def extract_sequence(text: str) -> Optional[list[int]]:
    if "sequence" in text.lower() and "?" in text:
        numbers = re.findall(r"\d+", text)
        if len(numbers) >= 2:
            return [int(n) for n in numbers]
    return None