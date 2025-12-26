# -*- coding: utf-8 -*-

from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/")
def root(request: Request) -> dict[str, list[dict[str, Any]]]:
    routes = [
        {"path": r.path, "name": r.name, "methods": list(r.methods)}
        for r in request.app.routes
    ]
    return {"available_routes": routes}


@router.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("./karatel/images/favicon.png")
