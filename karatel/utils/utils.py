# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.core.items import Item
    from karatel.core.professions import Profession
    from karatel.core.skills import Skill


def get_modifier(stat_value: int) -> int:
    """Для типових DnD-розрахунків бонусів"""
    return (stat_value - 10) // 2


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


def hero_to_dict(hero: Hero) -> dict:
    the_dict: dict = {
        "name": hero.name,
        "profession": hero.profession.name,
        "experience": hero.experience,
        "lives": hero.lives,
        "money": hero.money,
        "left_hand": hero.left_hand.name,
        "right_hand": hero.right_hand.name,
        "skills": [],
        "inventory": [],
    }
    for skill in hero.skills:
        the_dict["skills"].append(skill.name)
    for item in hero.inventory:
        the_dict["inventory"].append(item.name)

    return the_dict
