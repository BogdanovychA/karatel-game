# -*- coding: utf-8 -*-
from dataclasses import dataclass

from karatel.ui.abstract import ConsoleOutput, OutputSpace, SaveHero, XMLSaver


@dataclass
class GameStateManager:
    """Керує різними статусами гри"""

    output: OutputSpace
    saver: SaveHero
    can_generate_map: bool


gsm = GameStateManager(
    output=ConsoleOutput(),
    saver=XMLSaver(),
    can_generate_map=False,
)
