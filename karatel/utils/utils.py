# -*- coding: utf-8 -*-
from __future__ import annotations

import random
import string
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from karatel.core.items import Item
    from karatel.core.professions import Profession
    from karatel.core.skills import Skill


def get_modifier(stat_value: int) -> int:
    """Для типових DnD-розрахунків бонусів"""
    return (stat_value - 10) // 2


def sanitize_word(word: str) -> str | bool:
    if not word or word is True:
        return False
    word = word.replace(" ", "_")
    return ''.join(c for c in word if c.isalnum() or c == '_')


def clamp_value(
    value: int | float, min_value: int | float | None, max_value: int | float | None
) -> int | float:
    """Обмеження значення між min та max.
    Якщо щось обмежувати не треба -- передаємо None"""

    if min_value is not None:
        value = max(value, min_value)
    if max_value is not None:
        value = min(value, max_value)
    return value


def obj_finder(
    name: str, data_container: dict | tuple | list
) -> Profession | Item | Skill | None:
    """Шукає об'єкт по базі предметів, навичок або професій"""

    if isinstance(data_container, dict):
        iterable = data_container.values()
    elif isinstance(data_container, (tuple, list)):
        iterable = data_container
    else:
        return None

    for obj in iterable:
        if getattr(obj, "name", None) == name:
            return obj
    return None


def generate_random_prefix(length=5):
    """
    Генерує випадковий рядок з маленьких латинських літер заданої довжини.
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
