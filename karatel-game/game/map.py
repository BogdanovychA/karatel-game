import random
from enum import Enum, IntEnum
from typing import Tuple

from .hero import Hero, HeroFactory
from .items import (
    CHARISMA_WEAPONS,
    DEXTERITY_WEAPONS,
    INTELLIGENCE_WEAPONS,
    SHIELDS,
    STRENGTH_WEAPONS,
    Item,
)
from .ui import OutputSpace, ui
from .utils import clamp_value


class Emoji(Enum):
    EMPTY = " ⬜ "
    ENEMY = " 👹 "
    ITEM = " 💎 "
    HERO = " 🧙 "
    EXIT = " 🚪 "


class CellType(Enum):
    """Enum-клас для зберігання змінних, що
    відповідають за типи наповнення клітинок"""

    EMPTY = "empty"
    ENEMY = "enemy"
    ITEM = "item"
    HERO = "hero"
    EXIT = "exit"


class MapSize(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за розмір мапи"""

    X = 10
    Y = 10


class StartHeroPosition(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за стартову позицію героя"""

    x = 0
    y = 0


class CellMultiplier(IntEnum):
    """Enum-клас для зберігання змінних, що
    відповідають за мультиплікатор типів клітинок"""

    EMPTY = 10
    ENEMY = 5
    ITEM = 5


TYPES_OF_CELL = (
    [CellType.EMPTY] * CellMultiplier.EMPTY
    + [CellType.ENEMY] * CellMultiplier.ENEMY
    + [CellType.ITEM] * CellMultiplier.ITEM
)


def set_empty_cell() -> Tuple[CellType, None, str]:
    return CellType.EMPTY, None, Emoji.EMPTY.value


def select_obj() -> Tuple[CellType, Hero | Item | None, str]:
    cell = random.choice(TYPES_OF_CELL)
    match cell:
        case CellType.ENEMY:
            return CellType.ENEMY, HeroFactory.generate(), Emoji.ENEMY.value
        case CellType.ITEM:
            return (
                CellType.ITEM,
                random.choice(
                    STRENGTH_WEAPONS
                    + DEXTERITY_WEAPONS
                    + INTELLIGENCE_WEAPONS
                    + CHARISMA_WEAPONS
                    + SHIELDS
                ),
                Emoji.ITEM.value,
            )
        case CellType.EMPTY | _:
            return set_empty_cell()


class Cell:
    def __init__(
        self,
        cell_type: CellType,
        obj: Hero | Item | None = None,
        emoji: str | None = None,
        output: OutputSpace | None = None,
    ) -> None:
        self.type = cell_type
        self.obj = obj
        self.emoji = emoji or Emoji.EMPTY.value

        # Менеджери
        self.output = output if output is not None else ui


def generate_map(hero: Hero) -> list:
    line_y: list[list] = []
    for coordinate_y in range(MapSize.Y):
        line_x: list[Cell] = []
        for coordinate_x in range(0, MapSize.X):
            if (
                coordinate_y == StartHeroPosition.y
                and coordinate_x == StartHeroPosition.x
            ):
                cell_type = CellType.HERO
                obj = hero
                emoji = Emoji.HERO.value
            elif coordinate_y == MapSize.Y - 1 and coordinate_x == MapSize.X - 1:
                cell_type = CellType.EXIT
                obj = None
                emoji = Emoji.EXIT.value
            else:
                cell_type, obj, emoji = select_obj()

            line_x.append(Cell(cell_type, obj, emoji))
        line_y.append(line_x)
    return line_y


def render_map(the_map: list) -> None:
    for y in the_map:
        for x in y:
            print(x.emoji, end="")
        print()


def find_hero(the_map: list) -> Tuple[int | None, int | None]:
    """Шукає героя на карті. Повертає координати Y та X"""
    for y in range(len(the_map)):
        for x in range(len(the_map[y])):
            if the_map[y][x].type == CellType.HERO:
                return y, x
    return None, None


def move_hero(step_y: int, step_x: int, the_map: list) -> list:
    pos_y, pos_x = find_hero(the_map)
    if pos_y is None or pos_x is None:
        return the_map
    else:
        cell_type, obj, emoji = set_empty_cell()
        empty_cell = Cell(cell_type, obj, emoji)

        new_y = clamp_value((pos_y + step_y), 0, MapSize.Y - 1)
        new_x = clamp_value((pos_x + step_x), 0, MapSize.X - 1)

        the_map[new_y][new_x] = the_map[pos_y][pos_x]

        if new_y != pos_y or new_x != pos_x:
            the_map[pos_y][pos_x] = empty_cell

        return the_map


if __name__ == "__main__":
    hero_a = HeroFactory.generate(1)
    my_map = generate_map(hero_a)
    render_map(my_map)
    my_map = move_hero(1, 0, my_map)
    print()
    render_map(my_map)
    my_map = move_hero(1, 0, my_map)
    print()
    render_map(my_map)
    my_map = move_hero(0, 1, my_map)
    print()
    render_map(my_map)
    my_map = move_hero(0, 1, my_map)
    print()
    render_map(my_map)
    my_map = move_hero(1, 1, my_map)
    print()
