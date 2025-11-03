import random

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


def select_obj() -> Hero | Item | None:

    cell = random.choice(("empty", "empty", "empty", "empty", "empty", "enemy", "item"))
    # ui.write(cell)
    match cell:
        case "enemy":
            return HeroFactory.generate()
        case "item":
            return random.choice(
                STRENGTH_WEAPONS
                + DEXTERITY_WEAPONS
                + INTELLIGENCE_WEAPONS
                + CHARISMA_WEAPONS
                + SHIELDS
            )
        case "empty" | _:
            return None


class Cell:
    def __init__(
        self,
        y: int,
        x: int,
        obj: Hero | Item | None = None,
        output: OutputSpace | None = None,
    ) -> None:
        self.y = y
        self.x = x
        self.obj = obj

        # Менеджери
        self.output = output if output is not None else ui


def check_and_print(cell: Cell) -> str or None:
    if isinstance(cell.obj, Hero):
        return " 👹 "
    elif isinstance(cell.obj, Item):
        return " 💎 "
    else:
        return " ⬜ "


game_map: list[Cell] = []

# z: int = 0
for y in range(0, 10):
    for x in range(0, 10):
        obj = select_obj()
        game_map.append(Cell(y, x, obj))
        # ui.write(game_map[z].y, game_map[z].x)
        # z+=1

for item in game_map:
    if item.x != 9:
        ui.write(check_and_print(item), end="")
    else:
        ui.write(check_and_print(item), end="\n")
