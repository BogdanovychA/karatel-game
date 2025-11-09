# -*- coding: utf-8 -*-
from dataclasses import dataclass

from karatel.ui.abstract import ConsoleOutput, OutputSpace


@dataclass
class GameStateManager:
    """Керує різними статусами гри"""

    ui: OutputSpace
    can_generate_map: bool


gsm = GameStateManager(
    ui=ConsoleOutput(),
    can_generate_map=False,
)
