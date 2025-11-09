# -*- coding: utf-8 -*-

import random
from enum import Enum, IntEnum

from karatel.core.game_state_manager import gsm
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
from karatel.ui.abstract import OutputSpace
from karatel.utils.constants import Emoji


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
    HEART = "heart"


class MapSize(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за розмір мапи"""

    X = 15
    Y = 15


class GoldLimits(IntEnum):
    """Ліміти грошай при генерації клітинок з золотом"""

    MIN = 1
    MAX = 5
    ENEMY = 10
    EXIT = 500


class ExpLimits(IntEnum):
    """Ліміти досвіду при генерації клітинок з книжками"""

    MIN = 300
    MAX = 500


class StartHeroPosition(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за стартову позицію героя.
    Герой встановлюється на позицію від 0 до X|Y"""

    X = 2
    Y = 2


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
    HEART = 1


TYPES_OF_CELL = (
    [CellType.EMPTY] * CellMultiplier.EMPTY
    + [CellType.ENEMY] * CellMultiplier.ENEMY
    + [CellType.ITEM] * CellMultiplier.ITEM
    + [CellType.GOLD] * CellMultiplier.GOLD
    + [CellType.BOOK] * CellMultiplier.BOOK
    + [CellType.HEART] * CellMultiplier.HEART
)


class Cell:
    """Клас, що описує клітинку мапи"""

    def __init__(
        self,
        cell_type: CellType,
        obj: Hero | Item | None = None,
        gold: int = 0,
        experience: int = 0,
        output: OutputSpace | None = None,
    ) -> None:
        self.type = cell_type
        self.obj = obj
        self.gold = gold
        self.experience = experience

        # Менеджери
        self.output = output if output is not None else gsm.ui

    @property
    def emoji(self) -> str:
        """Встановлює емодзі, яке відповідає типу клітинки"""

        match self.type:
            case CellType.ENEMY:
                return Emoji.ENEMY.value
            case CellType.ITEM:
                return Emoji.ITEM.value
            case CellType.GOLD:
                return Emoji.GOLD.value
            case CellType.BOOK:
                return Emoji.BOOK.value
            case CellType.HEART:
                return Emoji.HEART.value
            case CellType.EMPTY:
                return Emoji.EMPTY.value
            case CellType.EXIT:
                return Emoji.EXIT.value
            case CellType.HERO:
                if self.obj.alive:
                    return Emoji.HERO.value
                else:
                    return Emoji.TOMB.value


EMPTY_CELL = Cell(CellType.EMPTY, None)  # Пуста клітинка


def select_obj(
    cell_type: CellType | None = None, enemy_level: int | None = None
) -> Cell:
    """Вибір клітинки. Якщо не задано тип -- випадковий"""

    def generate_enemy(level: int | None = None) -> Cell:
        """Створення клітинки з ворогом"""

        enemy = HeroFactory.generate(level)
        enemy_cell = Cell(
            cell_type=CellType.ENEMY,
            obj=enemy,
            gold=random.randint(GoldLimits.MIN, GoldLimits.ENEMY * enemy.level),
        )
        return enemy_cell

    def generate_item() -> Cell:
        """Створення клітинки з предметом"""

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
        )
        return item_cell

    def generate_gold() -> Cell:
        """Створення клітинки з грошима"""

        gold_cell = Cell(
            cell_type=CellType.GOLD,
            obj=None,
            gold=random.randint(GoldLimits.MIN, GoldLimits.MAX),
        )
        return gold_cell

    def generate_book() -> Cell:
        """Створення клітинки з досвідом"""

        book_cell = Cell(
            cell_type=CellType.BOOK,
            obj=None,
            experience=random.randint(ExpLimits.MIN, ExpLimits.MAX),
        )
        return book_cell

    def generate_heart() -> Cell:
        """Створення клітинки з життям"""

        heart_cell = Cell(
            cell_type=CellType.HEART,
            obj=None,
        )
        return heart_cell

    def create() -> Cell:
        """Допоміжна функція, для створення клітинки.
        Для забезпечення принципу DRY"""

        match cell_type:
            case CellType.ENEMY:
                return generate_enemy(enemy_level)
            case CellType.ITEM:
                return generate_item()
            case CellType.GOLD:
                return generate_gold()
            case CellType.BOOK:
                return generate_book()
            case CellType.HEART:
                return generate_heart()
            case CellType.EMPTY | _:
                return EMPTY_CELL

    if cell_type is None:
        cell_type = random.choice(TYPES_OF_CELL)

    return create()


def generate_map(hero: Hero) -> list[list[Cell]]:
    """Генерація мапи"""

    start_hero_position_y = random.randint(0, StartHeroPosition.Y)
    start_hero_position_x = random.randint(0, StartHeroPosition.X)

    line_y: list[list] = []
    for coordinate_y in range(MapSize.Y):
        line_x: list[Cell] = []
        for coordinate_x in range(0, MapSize.X):

            # Встановлюємо гравця на стартову позицію
            if (
                coordinate_y == start_hero_position_y
                and coordinate_x == start_hero_position_x
            ):
                cell = Cell(CellType.HERO, hero)

            # Встановлюємо ворогів перед виходом з підземелля
            elif (
                MapSize.Y - EnemyLine.Y <= coordinate_y <= MapSize.Y - 1
                and MapSize.X - EnemyLine.X <= coordinate_x <= MapSize.X - 1
            ) and (coordinate_y != MapSize.Y - 1 or coordinate_x != MapSize.X - 1):
                cell = select_obj(
                    CellType.ENEMY, enemy_level=hero.level + EnemyLine.MULTIPLIER
                )

            # Встановлюємо вихід
            elif coordinate_y == MapSize.Y - 1 and coordinate_x == MapSize.X - 1:
                cell = Cell(
                    CellType.EXIT,
                    None,
                    gold=random.randint((GoldLimits.EXIT // 2), GoldLimits.EXIT),
                )

            # Генеруємо випадкові клітинки мапи
            else:
                cell = select_obj(enemy_level=hero.level)

            line_x.append(cell)
        line_y.append(line_x)
    return line_y


def render_map(the_map: list) -> None:
    """Рендеринг мапи"""

    text = ""
    for y in the_map:
        for x in y:
            text += " " + x.emoji + " "
        text += "\n"
    gsm.ui.write(text)
