from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING

from karatel.core.hero import HeroFactory
from karatel.core.map import CellType, MapSize, generate_map
from karatel.ui.abstract import NoneOutput
from karatel.utils.constants import Sex

if TYPE_CHECKING:
    from karatel.core.map import Cell

output = NoneOutput()


def deep_eq(item_a: list | Cell, item_b: list | Cell, deep: int) -> tuple[bool, int]:

    if isinstance(item_a, Iterable) and isinstance(item_b, Iterable):

        if len(item_a) != len(item_b):
            return False, deep

        for sub_a, sub_b in zip(item_a, item_b):
            is_eq, deep = deep_eq(sub_a, sub_b, deep)
            if not is_eq:
                return False, deep

        return True, deep
    else:
        if item_a.type != item_b.type:
            return False, deep

        match item_a.type.value:

            case CellType.HERO.value | CellType.ENEMY.value:
                IGNORE_KEYS = [
                    'leveling',
                    'equipment',
                    'display',
                    'skill_manager',
                    'output',
                ]

                item_a_dict = item_a.obj.__dict__.copy()
                item_b_dict = item_b.obj.__dict__.copy()

                for key in IGNORE_KEYS:
                    item_a_dict.pop(key, None)
                    item_b_dict.pop(key, None)

                if item_a_dict != item_b_dict:
                    return False, deep

                if (
                    hasattr(item_a, 'gold')
                    and hasattr(item_a, 'gold')
                    and item_a.gold != item_b.gold
                ):
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


def test_map_eq():

    hero_c = HeroFactory.generate(
        output, name="Іван", sex=Sex.M, level=1, profession="commando"
    )
    map_a = generate_map(hero_c)
    map_b = map_a.copy()

    is_eq, deep = deep_eq(map_a, map_b, 0)

    assert deep == MapSize.X * MapSize.Y
    assert is_eq
