# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, ConfigDict

from karatel.core.items import (
    CHARISMA_WEAPONS,
    DEXTERITY_WEAPONS,
    INTELLIGENCE_WEAPONS,
    SHIELDS,
    STRENGTH_WEAPONS,
    WEAPONS,
    WeaponType,
)


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


router = APIRouter()


@router.get("/weapons", response_model=list[WeaponSchema])
def get_weapons(
    t: WeaponType = Query(..., description="Weapon type")
) -> list[WeaponSchema]:

    match t:
        case WeaponType.STRENGTH:
            return STRENGTH_WEAPONS
        case WeaponType.DEXTERITY:
            return DEXTERITY_WEAPONS
        case WeaponType.INTELLIGENCE:
            return INTELLIGENCE_WEAPONS
        case WeaponType.CHARISMA:
            return CHARISMA_WEAPONS
        case WeaponType.ALL:
            return WEAPONS
        case _:
            raise HTTPException(status_code=400, detail=f"Unknown weapon type: {t}")


@router.get("/shields", response_model=list[ShieldSchema])
def get_shields() -> list[ShieldSchema]:
    return SHIELDS
