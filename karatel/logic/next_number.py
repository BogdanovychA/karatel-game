# -*- coding: utf-8 -*-

from karatel.utils.constants import PRIMES


# Easy
def arithmetic_sequence(start: int, step: int, length: int) -> tuple[int, ...]:
    """Арифметична послідовність"""
    if length <= 0:
        raise ValueError("length має бути > 0")
    return tuple(start + i * step for i in range(length))


def geometric_sequence(start: int, ratio: int, length: int) -> tuple[int, ...]:
    """Геометрична послідовність"""
    if length <= 0:
        raise ValueError("length має бути > 0")
    if ratio == 0 or ratio == 1 or ratio == -1:
        raise ValueError(f"ratio не може = {ratio}")
    if start == 0:
        raise ValueError("start не може = 0")
    return tuple(start * (ratio**i) for i in range(length))


# Medium
def arithmetic_plus_sequence(
    start: int, step: int, multiplier: int, length: int
) -> tuple[int, ...]:
    """Арифметична послідовність зі збільшенням кроку"""
    if length <= 0:
        raise ValueError("length має бути > 0")
    sequence = [start]
    for i in range(length - 1):
        sequence.append(start := start + step)
        step += multiplier

    return tuple(sequence)


# Hard
def power_sequence(base: int, power: int, length: int) -> tuple[int, ...]:
    """Послідовність степенів числа"""
    if length <= 0:
        raise ValueError("length має бути > 0")
    if power <= 0:
        raise ValueError("power має бути > 0")
    if base <= 1:
        raise ValueError("base має бути > 1")
    return tuple(base ** (power * i) for i in range(1, length + 1))


def primes_sequence(start_index: int, length: int) -> tuple[int, ...]:
    """Послідовність простих чисел"""
    length_tuple = len(PRIMES)
    if start_index + length > length_tuple:
        raise ValueError(f"start_index + length не може бути > {length_tuple}")
    return PRIMES[start_index : start_index + length]


# def fibonacci_sequence(start_index: int, length: int) -> tuple[int, ...]:
#     """Послідовність Фібоначчі. Використання формули Бінета"""
#     if start_index < 0:
#         raise ValueError("start_index має бути більше чи дорівнювати 0")
#
#     if length <= 0:
#         raise ValueError("length має бути > 0")
#
#     _GOLDEN_RATIO = (1 + 5 ** 0.5) / 2
#     _CONJUGATE_RATIO = (1 - 5 ** 0.5) / 2
#
#     def _fibonacci_number(n: int) -> int:
#         return int(round((_GOLDEN_RATIO ** n - _CONJUGATE_RATIO ** n) / (5 ** 0.5)))
#
#     return tuple(_fibonacci_number(n) for n in range(start_index, start_index + length))


def fibonacci_sequence(start_index: int, length: int) -> tuple[int, ...]:
    """Послідовність Фібоначчі"""
    if start_index < 0:
        raise ValueError("start_index має бути більше чи дорівнювати 0")

    if length <= 0:
        raise ValueError("length має бути > 0")

    a, b = 0, 1
    for _ in range(start_index):
        a, b = b, a + b

    sequence = []
    for _ in range(length):
        sequence.append(a)
        a, b = b, a + b

    return tuple(sequence)


if __name__ == "__main__":
    _LENGTH = 10
    print(f"{arithmetic_sequence.__doc__}:", arithmetic_sequence(2, 3, _LENGTH))
    print(f"{arithmetic_sequence.__doc__}:", arithmetic_sequence(2, -3, 10))
    print(
        f"{arithmetic_plus_sequence.__doc__}:",
        arithmetic_plus_sequence(2, 3, 1, _LENGTH),
    )
    print(
        f"{arithmetic_plus_sequence.__doc__}:",
        arithmetic_plus_sequence(2, 3, -1, _LENGTH),
    )
    print(
        f"{arithmetic_plus_sequence.__doc__}:",
        arithmetic_plus_sequence(2, -3, 1, _LENGTH),
    )
    print(
        f"{arithmetic_plus_sequence.__doc__}:",
        arithmetic_plus_sequence(2, -3, -1, _LENGTH),
    )
    print(f"{geometric_sequence.__doc__}:", geometric_sequence(1, 3, _LENGTH))
    print(f"{power_sequence.__doc__}:", power_sequence(2, 3, _LENGTH))
    print(f"{fibonacci_sequence.__doc__}:", fibonacci_sequence(0, _LENGTH))
    print(f"{primes_sequence.__doc__}:", primes_sequence(90, _LENGTH))
