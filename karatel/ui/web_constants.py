# -*- coding: utf-8 -*-
from enum import Enum

TITLE = "КАРАТЄЛЬ"

BUTTON_WIDTH = 150


class GameState(Enum):

    HERO = "hero"
    ON_MAP = "on_map"
    LOAD_HERO = "load_hero"
