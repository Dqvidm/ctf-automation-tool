# tests/test_solver.py
from utils.solver import solve_challenge


def test_binary_and():
    assert solve_challenge("Binary AND: 1100 AND 1010 = ?") == "1000"


def test_binary_nor_8bit():
    assert solve_challenge("Binary NOR (8-bit): 00000000 NOR 00000000 = ?") == "11111111"


def test_complex_logic():
    assert solve_challenge("Calculate: (1010 AND 1100) XOR 1111 = ?") == "111"


def test_reverse_string():
    assert solve_challenge("Reverse this string: network") == "krowten"


def test_hex_to_decimal():
    assert solve_challenge("Convert hex to decimal: 0xff") == "255"


def test_math():
    assert solve_challenge("What is 25 + 75?") == "100"


def test_sequence():
    assert solve_challenge("Next number in sequence: 3, 6, 9, 12, ?") == "15"