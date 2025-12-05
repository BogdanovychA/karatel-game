# -*- coding: utf-8 -*-

from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse

from karatel.api.schemas import ProfessionSchema, ShieldSchema, WeaponSchema
from karatel.core.hero import HeroFactory
from karatel.core.items import (
    CHARISMA_WEAPONS,
    DEXTERITY_WEAPONS,
    INTELLIGENCE_WEAPONS,
    SHIELDS,
    STRENGTH_WEAPONS,
    WEAPONS,
    WeaponType,
)
from karatel.core.professions import PROFESSIONS
from karatel.ui.abstract import ConsoleOutput

app = FastAPI(
    title="Karatel Game API",
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
)


@app.exception_handler(404)
async def handler(request: Request, exception: HTTPException):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.detail,
            "timestamp": datetime.now().isoformat(),
            "status": "failure",
        },
    )


@app.get("/")
def root() -> dict[str, list[dict[str, Any]]]:
    routes = [
        {"path": r.path, "name": r.name, "methods": list(r.methods)} for r in app.routes
    ]
    return {"available_routes": routes}


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("./karatel/images/favicon.png")


@app.get("/generate_hero")
def generate_hero() -> dict[str, Any]:
    return HeroFactory.hero_to_dict(HeroFactory.generate(ConsoleOutput()))


@app.get("/professions", response_model=dict[str, ProfessionSchema])
def get_professions() -> dict[str, ProfessionSchema]:
    return PROFESSIONS


@app.get("/weapons", response_model=list[WeaponSchema])
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


@app.get("/shields", response_model=list[ShieldSchema])
def get_shields() -> list[ShieldSchema]:
    return SHIELDS
