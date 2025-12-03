# -*- coding: utf-8 -*-

from dataclasses import dataclass

from karatel.storage.abstract import StorageManager
from karatel.ui.abstract import OutputSpace


@dataclass
class GameStateManager:
    """Керує різними статусами гри"""

    output: OutputSpace
    saver: StorageManager
    can_generate_map: bool
    username: str | None
    user_id: str | None = None
    idToken: str | None = None
    refreshToken: str | None = None
