# -*- coding: utf-8 -*-

import random
from enum import Enum, IntEnum

from karatel.core.hero import Hero, HeroFactory
from karatel.core.items import (
    CHARISMA_WEAPONS,
    DEXTERITY_WEAPONS,
    INTELLIGENCE_WEAPONS,
    JUST_HAND,
    SHIELDS,
    STRENGTH_WEAPONS,
    UNARMED_STRIKE,
    Item,
)
from karatel.ui.abstract import OutputSpace, ui


class Emoji(Enum):
    """Enum-клас для зберігання емоджі"""

    EMPTY = " ⬜ "
    ENEMY = " 👹 "
    ITEM = " 💎 "
    HERO = " 🧙 "
    EXIT = " 🚪 "
    TOMB = " 🪦 "
    GOLD = " 🪙 "


class CellType(Enum):
    """Enum-клас для зберігання змінних, що
    відповідають за типи наповнення клітинок"""

    EMPTY = "empty"
    ENEMY = "enemy"
    ITEM = "item"
    HERO = "hero"
    EXIT = "exit"
    GOLD = "gold"


class MapSize(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за розмір мапи"""

    X = 19
    Y = 15


class GoldLimits(IntEnum):
    """Ліміти грошай при генерації клітинок з золотом"""

    MIN = 1
    MAX = 10


class StartHeroPosition(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за стартову позицію героя"""

    X = random.randint(0, 4)
    Y = random.randint(0, 4)


class CellMultiplier(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за мультиплікатор типів клітинок"""

    EMPTY = 10
    ENEMY = 5
    ITEM = 5
    GOLD = 1


TYPES_OF_CELL = (
    [CellType.EMPTY] * CellMultiplier.EMPTY
    + [CellType.ENEMY] * CellMultiplier.ENEMY
    + [CellType.ITEM] * CellMultiplier.ITEM
    + [CellType.GOLD] * CellMultiplier.GOLD
)


class Cell:
    """Клас, що описує клітинку мапи"""

    def __init__(
        self,
        cell_type: CellType,
        obj: Hero | Item | None = None,
        emoji: str | None = None,
        gold: int = 0,
        output: OutputSpace | None = None,
    ) -> None:
        self.type = cell_type
        self.obj = obj
        self.emoji = emoji or Emoji.EMPTY.value
        self.gold = gold

        # Менеджери
        self.output = output if output is not None else ui


EMPTY_CELL = Cell(CellType.EMPTY, None, Emoji.EMPTY.value)


def select_obj() -> Cell:
    cell = random.choice(TYPES_OF_CELL)
    match cell:
        case CellType.ENEMY:
            cell = Cell(CellType.ENEMY, HeroFactory.generate(), Emoji.ENEMY.value)
            return cell
        case CellType.ITEM:
            all_items = list(
                STRENGTH_WEAPONS
                + SHIELDS
                + DEXTERITY_WEAPONS
                + INTELLIGENCE_WEAPONS
                + CHARISMA_WEAPONS
            )
            all_items.remove(UNARMED_STRIKE)
            all_items.remove(JUST_HAND)
            cell = Cell(CellType.ITEM, random.choice(all_items), Emoji.ITEM.value)
            return cell
        case CellType.GOLD:
            return Cell(
                CellType.GOLD,
                None,
                Emoji.GOLD.value,
                random.randint(GoldLimits.MIN, GoldLimits.MAX),
            )
        case CellType.EMPTY | _:
            return EMPTY_CELL


def generate_map(hero: Hero) -> list[list[Cell]]:
    line_y: list[list] = []
    for coordinate_y in range(MapSize.Y):
        line_x: list[Cell] = []
        for coordinate_x in range(0, MapSize.X):
            if (
                coordinate_y == StartHeroPosition.X
                and coordinate_x == StartHeroPosition.Y
            ):
                cell = Cell(CellType.HERO, hero, Emoji.HERO.value)
            elif coordinate_y == MapSize.Y - 1 and coordinate_x == MapSize.X - 1:
                cell = Cell(CellType.EXIT, None, Emoji.EXIT.value)
            else:
                cell = select_obj()

            line_x.append(cell)
        line_y.append(line_x)
    return line_y


def render_map(the_map: list) -> None:
    text = ""
    for y in the_map:
        for x in y:
            text += x.emoji
        text += "\n"
    ui.write(text)
