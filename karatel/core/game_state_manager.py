# -*- coding: utf-8 -*-
from dataclasses import dataclass


@dataclass
class GameStateManager:
    """Керує різними статусами гри"""

    can_generate_map: bool | None


gsm = GameStateManager(can_generate_map=False)
