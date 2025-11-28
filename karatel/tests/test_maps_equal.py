from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

import pytest

from karatel.core.hero import HeroFactory
from karatel.core.map import CellType, MapSize, generate_map
from karatel.core.professions import PROFESSIONS
from karatel.storage.abstract import SQLiteSaver
from karatel.ui.abstract import NoneOutput
from karatel.utils.settings import MAX_LEVEL, MIN_LEVEL

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.core.map import Cell

output = NoneOutput()
saver = SQLiteSaver()


def heroes_equal(hero_a: Hero, hero_b: Hero) -> bool:
    """Перевірка рівності героїв"""

    # Видаляємо менеджери, бо вони завжди не збігаються,
    # але це не проблема
    IGNORE_KEYS = [
        'leveling',
        'equipment',
        'display',
        'skill_manager',
        'output',
    ]

    hero_a_dict = hero_a.__dict__.copy()
    hero_b_dict = hero_b.__dict__.copy()

    for key in IGNORE_KEYS:
        hero_a_dict.pop(key, None)
        hero_b_dict.pop(key, None)

    return hero_a_dict == hero_b_dict


def maps_equal(item_a: list | Cell, item_b: list | Cell, deep: int) -> tuple[bool, int]:
    """Перевірка рівності мап"""

    if isinstance(item_a, Iterable) and isinstance(item_b, Iterable):

        if len(item_a) != len(item_b):
            return False, deep

        for sub_a, sub_b in zip(item_a, item_b):
            is_eq, deep = maps_equal(sub_a, sub_b, deep)
            if not is_eq:
                return False, deep

        return True, deep
    else:
        if item_a.type != item_b.type:
            return False, deep

        match item_a.type.value:

            case CellType.HERO.value:
                if not heroes_equal(item_a.obj, item_b.obj):
                    return False, deep

            case CellType.ENEMY.value:

                if not heroes_equal(item_a.obj, item_b.obj):
                    return False, deep

                if item_a.gold != item_b.gold:
                    return False, deep

            case CellType.ITEM.value:

                if item_a.obj != item_b.obj:
                    return False, deep

            case CellType.GOLD.value | CellType.EXIT.value:

                if item_a.gold != item_b.gold:
                    return False, deep

            case CellType.BOOK.value:
                if item_a.experience != item_b.experience:
                    return False, deep

            case CellType.HEART.value | CellType.GAME.value | CellType.EMPTY.value:
                pass

            case _:
                return False, deep

        deep += 1
        return True, deep


@pytest.mark.parametrize("level", list(range(MIN_LEVEL, MAX_LEVEL + 1)))
@pytest.mark.parametrize("profession", list(PROFESSIONS.keys()))
def test_maps_equal(level, profession):
    """Тест рівності героїв та мап"""
    USERNAME = "test_user"
    HERO_ID = 1

    hero_a = HeroFactory.generate(output, level, profession)
    map_a = generate_map(hero_a)
    saver.save_hero(hero_a, map_a, USERNAME, False)

    hero_b, map_b = saver.load_hero(output, USERNAME, HERO_ID, False)
    saver.delete_hero(output, USERNAME, HERO_ID)

    heroes_are_equal = heroes_equal(hero_a, hero_b)
    maps_are_equal, deep = maps_equal(map_a, map_b, 0)

    assert heroes_are_equal
    assert maps_are_equal
    assert deep == MapSize.X * MapSize.Y
