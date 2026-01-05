# -*- coding: utf-8 -*-

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ProfessionSchema(BaseModel):
    """Схема для класу професій"""

    name: str  # Назва (чол. рід)
    name_fem: str  # Назва (жін. рід)
    description: str  # Опис (чол. рід)
    description_fem: str  # Опис (жін. рід)
    main_bonuses: tuple[str, ...]
    secondary_bonuses: tuple[str, ...]
    penalties: tuple[str, ...]

    model_config = ConfigDict(from_attributes=True)


class WeaponSchema(BaseModel):
    """Схема для класу зброї"""

    name: str
    description: str
    damage: str
    stat: str
    two_handed: bool

    model_config = ConfigDict(from_attributes=True)


class ShieldSchema(BaseModel):
    """Схема для класу щитів"""

    name: str
    description: str
    ac_bonus: int

    model_config = ConfigDict(from_attributes=True)


class TTTGameBoard(BaseModel):
    """Схема дошки для хрестиків-ноликів"""

    cells: list[Literal[" ", "X", "0"]] = Field(..., min_length=9, max_length=9)


class TTTResultEnum(str, Enum):
    """Символи для повернення результату гри в хрестики-нолики"""

    WIN_X = "X"
    WIN_0 = "0"
    DRAW = "draw"
    NONE = "none"


class TTTGameResult(BaseModel):
    """Для повернення результату гри в хрестики-нолики"""

    result: TTTResultEnum
