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
    email: str | None = None
    local_id: str | None = None
    id_token: str | None = None
    refresh_token: str | None = None
