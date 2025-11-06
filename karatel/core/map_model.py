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
    BOOK = " 📖 "


class CellType(Enum):
    """Enum-клас для зберігання змінних, що
    відповідають за типи наповнення клітинок"""

    EMPTY = "empty"
    ENEMY = "enemy"
    ITEM = "item"
    HERO = "hero"
    EXIT = "exit"
    GOLD = "gold"
    BOOK = "book"


class MapSize(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за розмір мапи"""

    X = 19
    Y = 15


class GoldLimits(IntEnum):
    """Ліміти грошай при генерації клітинок з золотом"""

    MIN = 1
    MAX = 5
    ENEMY = 10


class ExpLimits(IntEnum):
    """Ліміти досвіду при генерації клітинок з книжками"""

    MIN = 100
    MAX = 500


class StartHeroPosition(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за стартову позицію героя"""

    X = random.randint(0, 4)
    Y = random.randint(0, 4)


class EnemyLine(IntEnum):
    """Кількість рядів монстрів перед виходом
    та бонус до їх рівня"""

    X = 3
    Y = 3
    MULTIPLIER = 5


class CellMultiplier(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за мультиплікатор типів клітинок"""

    EMPTY = 10
    ENEMY = 5
    ITEM = 5
    GOLD = 1
    BOOK = 1


TYPES_OF_CELL = (
    [CellType.EMPTY] * CellMultiplier.EMPTY
    + [CellType.ENEMY] * CellMultiplier.ENEMY
    + [CellType.ITEM] * CellMultiplier.ITEM
    + [CellType.GOLD] * CellMultiplier.GOLD
    + [CellType.BOOK] * CellMultiplier.BOOK
)


class Cell:
    """Клас, що описує клітинку мапи"""

    def __init__(
        self,
        cell_type: CellType,
        obj: Hero | Item | None = None,
        emoji: str | None = None,
        gold: int = 0,
        experience: int = 0,
        output: OutputSpace | None = None,
    ) -> None:
        self.type = cell_type
        self.obj = obj
        self.emoji = emoji or Emoji.EMPTY.value
        self.gold = gold
        self.experience = experience

        # Менеджери
        self.output = output if output is not None else ui


EMPTY_CELL = Cell(CellType.EMPTY, None, Emoji.EMPTY.value)


def select_obj(
    cell_type: CellType | None = None, enemy_level: int | None = None
) -> Cell:

    def generate_enemy(level: int | None = None) -> Cell:
        enemy = HeroFactory.generate(level)
        enemy_cell = Cell(
            cell_type=CellType.ENEMY,
            obj=enemy,
            emoji=Emoji.ENEMY.value,
            gold=random.randint(GoldLimits.MIN, GoldLimits.ENEMY * enemy.level),
        )
        return enemy_cell

    def generate_item() -> Cell:
        all_items = list(
            STRENGTH_WEAPONS
            + SHIELDS
            + DEXTERITY_WEAPONS
            + INTELLIGENCE_WEAPONS
            + CHARISMA_WEAPONS
        )
        all_items.remove(UNARMED_STRIKE)
        all_items.remove(JUST_HAND)
        item_cell = Cell(
            cell_type=CellType.ITEM,
            obj=random.choice(all_items),
            emoji=Emoji.ITEM.value,
        )
        return item_cell

    def generate_gold() -> Cell:
        gold_cell = Cell(
            cell_type=CellType.GOLD,
            obj=None,
            emoji=Emoji.GOLD.value,
            gold=random.randint(GoldLimits.MIN, GoldLimits.MAX),
        )
        return gold_cell

    def generate_book() -> Cell:
        book_cell = Cell(
            cell_type=CellType.BOOK,
            obj=None,
            emoji=Emoji.BOOK.value,
            experience=random.randint(ExpLimits.MIN, ExpLimits.MAX),
        )
        return book_cell

    def create() -> Cell:
        match cell_type:
            case CellType.ENEMY:
                return generate_enemy(enemy_level)
            case CellType.ITEM:
                return generate_item()
            case CellType.GOLD:
                return generate_gold()
            case CellType.BOOK:
                return generate_book()
            case CellType.EMPTY | _:
                return EMPTY_CELL

    if cell_type is None:
        cell_type = random.choice(TYPES_OF_CELL)

    return create()


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
            elif (
                MapSize.Y - EnemyLine.Y <= coordinate_y <= MapSize.Y - 1
                and MapSize.X - EnemyLine.X <= coordinate_x <= MapSize.X - 1
            ) and (coordinate_y != MapSize.Y - 1 or coordinate_x != MapSize.X - 1):
                cell = select_obj(
                    CellType.ENEMY, enemy_level=hero.level + EnemyLine.MULTIPLIER
                )
            elif coordinate_y == MapSize.Y - 1 and coordinate_x == MapSize.X - 1:
                cell = Cell(CellType.EXIT, None, Emoji.EXIT.value)
            else:
                cell = select_obj(enemy_level=hero.level)

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
