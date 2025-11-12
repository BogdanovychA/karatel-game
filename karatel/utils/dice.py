# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import TYPE_CHECKING

from karatel.utils.settings import DEBUG

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace


class Dice:
    """
    Клас-утиліта для операцій з кидками кубиків (dice rolls),
    використовує формат D&D/Pathfinder (XdY+Z).
    """

    @staticmethod
    def make_string(num_dice: int, num_sides: int, modifier: int = 0) -> str:
        """Створює строку формату XdY+Z для кидка кубика."""
        return f"{num_dice}d{num_sides}+{modifier}"

    @staticmethod
    def roll(output: OutputSpace, dice_string: str) -> int:
        """
        Виконує кидок кубика у форматі XdY+Z.
        Повертає суму кидків + модифікатор.

        Примітка: цей парсер очікує формат "XdY" або "XdY+Z".
        Не підтримує від'ємні модифікатори (-Z).
        """
        # Беремо строку, розділювач "d"
        num_dice, dice_expression = dice_string.lower().split("d")
        # Беремо строку, розділювач "+", додаємо "0", якщо в функцію
        # не передали модифікатор, вибираємо тільки два перші елементи
        num_sides, modifier = (dice_expression.split("+") + [0])[:2]
        output.write(
            f"Кубиків: {num_dice}, Граней: {num_sides}, Модифікатор: {modifier}",
            log=DEBUG,
        )

        total = 0
        for _ in range(int(num_dice)):
            value = random.randint(1, int(num_sides))
            total += value

        result = total + int(modifier)
        output.write(
            f"Загальний результат: {result} це сума кидків: {total} "
            + f"плюс модифікатор: {modifier}\n",
            log=DEBUG,
        )

        return result
