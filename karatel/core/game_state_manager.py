# -*- coding: utf-8 -*-
from dataclasses import dataclass

from karatel.ui.abstract import ConsoleOutput, OutputSpace, SaveHero, XMLSaver


@dataclass
class GameStateManager:
    """Керує різними статусами гри"""

    ui: OutputSpace
    saver: SaveHero
    can_generate_map: bool


gsm = GameStateManager(
    ui=ConsoleOutput(),
    saver=XMLSaver(),
    can_generate_map=False,
)
