# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter

from karatel.api.schemas import ProfessionSchema
from karatel.core.hero import HeroFactory
from karatel.core.professions import PROFESSIONS
from karatel.ui.abstract import ConsoleOutput

router = APIRouter()


@router.get("/generate")
def generate_hero() -> dict[str, Any]:
    return HeroFactory.hero_to_dict(HeroFactory.generate(ConsoleOutput()))


@router.get("/professions", response_model=dict[str, ProfessionSchema])
def get_professions() -> dict[str, ProfessionSchema]:
    return PROFESSIONS
