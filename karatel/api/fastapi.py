# -*- coding: utf-8 -*-
from unittest import case

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from karatel.api.schemas import ProfessionSchema, WeaponSchema, WeaponType
from karatel.core.hero import HeroFactory
from karatel.core.items import (
    CHARISMA_WEAPONS,
    DEXTERITY_WEAPONS,
    INTELLIGENCE_WEAPONS,
    SHIELDS,
    STRENGTH_WEAPONS,
    WEAPONS,
)
from karatel.core.professions import PROFESSIONS
from karatel.ui.abstract import ConsoleOutput

app = FastAPI(
    title="Karatel Game API",
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


@app.get("/")
def root():
    routes = [
        {"path": r.path, "name": r.name, "methods": list(r.methods)} for r in app.routes
    ]
    return {"available_routes": routes}


@app.get("/favicon.ico")
def favicon():
    return FileResponse("./karatel/images/favicon.png")


@app.get("/generate_hero")
def generate_hero():
    return HeroFactory.hero_to_dict(HeroFactory.generate(ConsoleOutput()))


@app.get("/professions", response_model=dict[str, ProfessionSchema])
def get_professions():
    return PROFESSIONS


@app.get("/weapons", response_model=list[WeaponSchema])
def get_weapons(t: WeaponType):

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
