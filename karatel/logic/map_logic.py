# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

from karatel.core.map_model import EMPTY_CELL, CellType, Emoji, MapSize
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


def move_hero(step_y: int, step_x: int, the_map: list) -> list:
    """Переміщення персонажа по мапі"""

    def step():
        """Винесено в окрему функцію для забезпечення принципу DRY"""

        # Додаємо гроші
        add_money(the_map[pos_y][pos_x].obj, the_map[new_y][new_x], log=LOG)
        # Додаємо досвід
        the_map[pos_y][pos_x].obj.leveling.add_experience(
            the_map[new_y][new_x].experience, log=LOG
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
                    the_map[new_y][new_x].obj, log=LOG
                )
                step()
            case CellType.ENEMY:
                fight(the_map[pos_y][pos_x].obj, the_map[new_y][new_x].obj)
                if the_map[pos_y][pos_x].obj.alive:
                    step()
                else:
                    the_map[pos_y][pos_x].emoji = Emoji.TOMB.value
            case CellType.EXIT:
                ui.write(f"{the_map[pos_y][pos_x].obj.name} перемагає", log=LOG)
                step()

        return the_map
