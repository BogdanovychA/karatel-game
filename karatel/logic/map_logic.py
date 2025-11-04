# -*- coding: utf-8 -*-

from typing import Tuple

from karatel.core.map_model import EMPTY_CELL, CellType, MapSize
from karatel.logic.combat import fight
from karatel.utils.settings import LOG
from karatel.utils.utils import clamp_value


def find_hero(the_map: list) -> Tuple[int | None, int | None]:
    """Шукає героя на карті. Повертає координати Y та X"""
    for y in range(len(the_map)):
        for x in range(len(the_map[y])):
            if the_map[y][x].type == CellType.HERO:
                return y, x
    return None, None


def move_hero(step_y: int, step_x: int, the_map: list) -> list:

    def step():
        the_map[new_y][new_x] = the_map[pos_y][pos_x]
        if new_y != pos_y or new_x != pos_x:
            the_map[pos_y][pos_x] = EMPTY_CELL

    pos_y, pos_x = find_hero(the_map)
    if pos_y is None or pos_x is None:
        return the_map
    else:
        new_y = clamp_value((pos_y + step_y), 0, MapSize.Y - 1)
        new_x = clamp_value((pos_x + step_x), 0, MapSize.X - 1)

        if the_map[new_y][new_x].type == CellType.EMPTY:
            step()
        elif the_map[new_y][new_x].type == CellType.ITEM:
            the_map[pos_y][pos_x].obj.equipment.add_item(
                the_map[new_y][new_x].obj, log=LOG
            )
            step()
        elif the_map[new_y][new_x].type == CellType.EXIT:
            pass
        elif the_map[new_y][new_x].type == CellType.ENEMY:
            fight(the_map[pos_y][pos_x].obj, the_map[new_y][new_x].obj)
            if the_map[pos_y][pos_x].obj.alive:
                step()

        return the_map
