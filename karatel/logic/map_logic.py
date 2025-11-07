# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from karatel.core.map_model import EMPTY_CELL, CellType, MapSize
from karatel.logic.combat import fight
from karatel.ui.abstract import ui
from karatel.utils.settings import LOG
from karatel.utils.utils import clamp_value

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.core.map_model import Cell


def find_hero(the_map: list) -> Tuple[int | None, int | None]:
    """Шукає героя на карті. Повертає координати Y та X"""
    for y in range(len(the_map)):
        for x in range(len(the_map[y])):
            if the_map[y][x].type == CellType.HERO:
                return y, x
    return None, None


def add_money(hero: Hero, cell: Cell, log=LOG) -> None:
    """Додавання грошей"""

    if cell.gold > 0:
        hero.money += cell.gold
        ui.write(f"{hero.name} отримує {cell.gold} грн", log=log)


def add_lives(hero: Hero, value: int | None, log=LOG) -> None:
    """Додавання життів"""

    if value != 0 and value is not None:
        if value < 0 and abs(value) > hero.lives:
            value = hero.lives * -1
        hero.lives += value
        if value > 0:
            ui.write(f"{hero.name} отримує {value} життя", log=log)
        elif value < 0:
            ui.write(f"{hero.name} втрачає {abs(value)} життя", log=log)


def move_hero(
    step_y: int,
    step_x: int,
    the_map: list,
    log: bool = LOG,
) -> list:
    """Переміщення персонажа по мапі"""

    def step():
        """Винесено в окрему функцію для забезпечення принципу DRY"""

        # Додаємо гроші
        add_money(the_map[pos_y][pos_x].obj, the_map[new_y][new_x], log=log)
        # Додаємо досвід
        the_map[pos_y][pos_x].obj.leveling.add_experience(
            the_map[new_y][new_x].experience, log=log
        )
        # Переміщуємо об'єкт персонажа в новий Cell
        the_map[new_y][new_x] = the_map[pos_y][pos_x]
        if new_y != pos_y or new_x != pos_x:
            the_map[pos_y][pos_x] = EMPTY_CELL

    pos_y, pos_x = find_hero(the_map)
    if pos_y is None or pos_x is None:
        return the_map
    else:
        new_y = clamp_value((pos_y + step_y), 0, MapSize.Y - 1)
        new_x = clamp_value((pos_x + step_x), 0, MapSize.X - 1)

        match the_map[new_y][new_x].type:
            case CellType.EMPTY | CellType.GOLD | CellType.BOOK:
                step()
            case CellType.ITEM:
                the_map[pos_y][pos_x].obj.equipment.add_item(
                    the_map[new_y][new_x].obj, log=log
                )
                step()
            case CellType.HEART:
                add_lives(the_map[pos_y][pos_x].obj, 1)
                step()
            case CellType.ENEMY:
                ui.write(
                    f"Ваш ворог:\n"
                    + f"{the_map[new_y][new_x].obj}\n"
                    + f"{the_map[new_y][new_x].obj.display.hp()} "
                    + f"{the_map[new_y][new_x].obj.display.level()}\n"
                    + f"{the_map[new_y][new_x].obj.display.stats()}\n"
                    + f"{the_map[new_y][new_x].obj.display.ac()}\n"
                    + f"{the_map[new_y][new_x].obj.display.modifiers()}\n",
                    log=log,
                )
                fight(the_map[pos_y][pos_x].obj, the_map[new_y][new_x].obj)
                if the_map[pos_y][pos_x].obj.alive:
                    step()
            case CellType.EXIT:
                ui.write(
                    f"{the_map[pos_y][pos_x].obj.name} знаходить вихід з підземелля",
                    log=log,
                )
                add_lives(the_map[pos_y][pos_x].obj, 1)
                step()

        return the_map
