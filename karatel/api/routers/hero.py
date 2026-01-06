# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict

from karatel.core.hero import HeroFactory
from karatel.core.professions import PROFESSIONS
from karatel.ui.abstract import ConsoleOutput


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


router = APIRouter()


@router.get("/generate")
def generate_hero() -> dict[str, Any]:
    return HeroFactory.hero_to_dict(HeroFactory.generate(ConsoleOutput()))


@router.get("/professions", response_model=dict[str, ProfessionSchema])
def get_professions() -> dict[str, ProfessionSchema]:
    return PROFESSIONS
