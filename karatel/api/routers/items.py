# -*- coding: utf-8 -*-

from fastapi import APIRouter, HTTPException, Query

from karatel.api.schemas import ShieldSchema, WeaponSchema
from karatel.core.items import (
    CHARISMA_WEAPONS,
    DEXTERITY_WEAPONS,
    INTELLIGENCE_WEAPONS,
    SHIELDS,
    STRENGTH_WEAPONS,
    WEAPONS,
    WeaponType,
)

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
