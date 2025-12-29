# -*- coding: utf-8 -*-

import random

from karatel.utils.constants import PRIMES, Difficulty


# Easy
def arithmetic_sequence(start: int, step: int, length: int) -> tuple[int, ...]:
    """Арифметична послідовність"""
    if length <= 0:
        raise ValueError("length має бути > 0")
    if step == 0:
        raise ValueError("step не може = 0")
    return tuple(start + i * step for i in range(length))


def geometric_sequence(start: int, ratio: int, length: int) -> tuple[int, ...]:
    """Геометрична послідовність"""
    if length <= 0:
        raise ValueError("length має бути > 0")
    if ratio in (0, 1, -1):
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
    if base <= 1:
        raise ValueError("base має бути > 1")
    if power <= 0:
        raise ValueError("power має бути > 0")
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


def get_game(
    length: int,
    difficulty: Difficulty = Difficulty.RANDOM,
    random_game: bool = True,
) -> tuple | tuple[tuple, ...]:
    """Фабрика функцій.
    Створює кортеж для виклику гри (враховуючи рівень складності):
    функція, яка створює послідовність,
    аргументи для цієї функції,
    крок для зрізу (прямий (1) чи зворотній (-1))
    опис послідовності.
    Якщо random_game = False, створює кортеж кортежів.
    """

    easy: tuple = (
        (
            arithmetic_sequence,
            (random.randint(-100, 100), random.randint(1, 10), length),
            1,
            "Арифметична послідовність",
        ),
        (
            arithmetic_sequence,
            (random.randint(-100, 100), random.randint(-10, -1), length),
            1,
            "Арифметична послідовність (від'ємний крок)",
        ),
        (
            power_sequence,
            (random.randint(2, 3), random.randint(1, 3), length),
            1,
            "Послідовність степенів",
        ),
        (
            geometric_sequence,
            (random.randint(1, 9), random.randint(2, 9), length),
            1,
            "Геометрична послідовність",
        ),
        (
            primes_sequence,
            (random.randint(0, len(PRIMES) - length), length),
            1,
            "Послідовність простих чисел",
        ),
    )

    medium: tuple = (
        (
            geometric_sequence,
            (random.randint(1, 9), random.randint(2, 9), length),
            -1,
            "Геометрична послідовність (інверсія)",
        ),
        (
            geometric_sequence,
            (random.randint(1, 9), random.randint(-9, -2), length),
            1,
            "Геометрична послідовність (зміна знаку)",
        ),
        (
            primes_sequence,
            (random.randint(0, len(PRIMES) - length), length),
            -1,
            "Послідовність простих чисел (інверсія)",
        ),
        (
            fibonacci_sequence,
            (random.randint(0, 10), length),
            1,
            "Послідовність Фібоначчі",
        ),
    )

    hard: tuple = (
        (
            geometric_sequence,
            (random.randint(1, 9), random.randint(-9, -2), length),
            -1,
            "Геометрична послідовність (зміна знаку, інверсія)",
        ),
        (
            fibonacci_sequence,
            (random.randint(0, 10), length),
            -1,
            "Послідовність Фібоначчі (інверсія)",
        ),
        (
            arithmetic_plus_sequence,
            (
                random.randint(1, 100),
                random.randint(1, 10),
                random.randint(1, 5),
                length,
            ),
            1,
            "Арифметична послідовність зі збільшенням кроку",
        ),
        (
            arithmetic_plus_sequence,
            (
                random.randint(1, 100),
                random.randint(1, 10),
                random.randint(-5, -1),
                length,
            ),
            1,
            "Арифметична послідовність зі зменшенням кроку",
        ),
        (
            arithmetic_plus_sequence,
            (
                random.randint(1, 100),
                random.randint(-10, -1),
                random.randint(1, 5),
                length,
            ),
            1,
            "Арифметична послідовність зі збільшенням кроку (від'ємний крок)",
        ),
        (
            arithmetic_plus_sequence,
            (
                random.randint(1, 100),
                random.randint(-10, -1),
                random.randint(-5, -1),
                length,
            ),
            1,
            "Арифметична послідовність зі зменшенням кроку (від'ємний крок)",
        ),
    )

    the_tuple = None

    match difficulty:
        case Difficulty.EASY:
            the_tuple = easy
        case Difficulty.MEDIUM:
            the_tuple = medium
        case Difficulty.HARD:
            the_tuple = hard
        case Difficulty.ALL:
            the_tuple = easy + medium + hard
        case Difficulty.RANDOM | _:
            the_tuple = random.choice((easy, medium, hard))

    if random_game:
        return random.choice(the_tuple)
    else:
        return the_tuple


def get_sequence(
    length: int, difficulty: Difficulty = Difficulty.RANDOM, random_game: bool = True
) -> tuple | tuple[tuple, ...]:
    """Використовує фабрику функцій, створює послідовність та повертає
    кортеж з неї та опису.
    Якщо random_game = False, повертає кортеж кортежів"""

    game_config = get_game(length, difficulty, random_game)

    if random_game:
        func, args, step, text = game_config
        sequence = func(*args)[::step]
        return sequence, text
    else:
        list_sequence = [
            (func(*args)[::step], text) for func, args, step, text in game_config
        ]
        return tuple(list_sequence)


if __name__ == "__main__":

    _LENGTH = 6

    print("EASY")
    print(get_sequence(_LENGTH, Difficulty.EASY, False))
    print("-" * 20)

    print("MEDIUM")
    print(get_sequence(_LENGTH, Difficulty.MEDIUM, False))
    print("-" * 20)

    print("HARD")
    print(get_sequence(_LENGTH, Difficulty.HARD, False))
    print("-" * 20)

    print("ALL")
    print(get_sequence(_LENGTH, Difficulty.ALL, False))
    print("-" * 20)

    print("RANDOM")
    print("EASY: ", get_sequence(_LENGTH, Difficulty.EASY))
    print("MEDIUM: ", get_sequence(_LENGTH, Difficulty.MEDIUM))
    print("HARD: ", get_sequence(_LENGTH, Difficulty.HARD))
    print("RANDOM: ", get_sequence(_LENGTH, Difficulty.RANDOM))
    print("-" * 20)
