from collections.abc import Iterable

import pytest

from karatel.core.hero import Hero, HeroFactory
from karatel.core.map import CellType, generate_map
from karatel.ui.abstract import NoneOutput
from karatel.utils.constants import Sex

output = NoneOutput()


hero_c = HeroFactory.generate(
    output, name="Іван", sex=Sex.M, level=1, profession="commando"
)
map_a = generate_map(hero_c)
map_b = map_a.copy()
# map_b = copy.deepcopy(map_a)


def deep_eq(item_a, item_b):
    if isinstance(item_a, Iterable) and isinstance(item_b, Iterable):
        # print("Iterable - True")
        if len(item_a) == len(item_b):
            # print("len is eq")
            for sub_a, sub_b in zip(item_a, item_b):
                deep_eq(sub_a, sub_b)
    else:
        # print("Iterable - False")
        print("----------")
        # print(item_a.__dict__, item_b.__dict__)
        if item_a.type == item_b.type:

            match item_a.type.value:

                case CellType.HERO.value | CellType.ENEMY.value:
                    IGNORE_KEYS = [
                        'leveling',
                        'equipment',
                        'display',
                        'skill_manager',
                        'output',
                    ]

                    item_a_dict = item_a.obj.__dict__
                    item_b_dict = item_b.obj.__dict__

                    for key in IGNORE_KEYS:
                        item_a_dict.pop(key, None)
                        item_b_dict.pop(key, None)

                    if item_a_dict == item_b_dict:
                        print(item_a_dict)
                    else:
                        print("Not eq")

                    if hasattr(item_a, 'gold') and hasattr(item_a, 'gold'):
                        print(item_a.gold == item_b.gold)

                case CellType.ITEM.value:

                    if item_a.obj == item_b.obj:
                        print(item_a.obj)
                    else:
                        print("Not eq")

                case CellType.GOLD.value | CellType.EXIT.value:

                    if item_a.gold == item_b.gold:
                        print(item_a.gold)
                    else:
                        print("Not eq")

                case CellType.BOOK.value:
                    if item_a.experience == item_b.experience:
                        print(item_a.experience)
                    else:
                        print("Not eq")

                case CellType.HEART.value | CellType.GAME.value | CellType.EMPTY.value:
                    print(
                        "CellType.HEART.value | CellType.GAME.value | CellType.EMPTY.value"
                    )

                case _:
                    print("_")

        else:
            print("Type of Cell not eq")


deep_eq(map_a, map_b)
