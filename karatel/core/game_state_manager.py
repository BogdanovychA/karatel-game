# -*- coding: utf-8 -*-

from dataclasses import dataclass

from karatel.storage.abstract import SQLSaver
from karatel.ui.abstract import OutputSpace


@dataclass
class GameStateManager:
    """Керує різними статусами гри"""

    output: OutputSpace
    saver: SQLSaver
    can_generate_map: bool
    username: str | None
    sex: str | None


# gsm = GameStateManager(
#     output=ConsoleOutput(),
#     saver=XMLHeroSaver(),
#     can_generate_map=False,
# )
