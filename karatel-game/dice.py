# -*- coding: utf-8 -*-
import random


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
    def roll(dice_string: str) -> int:
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
        # print(f"Кубиків: {num_dice}, Граней: {num_sides}, Модифікатор: {modifier}")

        total = 0
        for _ in range(int(num_dice)):
            value = random.randint(1, int(num_sides))
            total += value

        return total + int(modifier)
