# -*- coding: utf-8 -*-

from typing import Any

from fastapi import FastAPI
from fastapi.responses import FileResponse

from karatel.api.handlers import add_handlers
from karatel.api.routers import hero, items

app = FastAPI(
    title="Karatel Game API",
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

# Підключаємо маршрути
app.include_router(items.router, prefix="/items")
app.include_router(hero.router, prefix="/hero")

# Додаємо обробники помилок
add_handlers(app)


@app.get("/")
def root() -> dict[str, list[dict[str, Any]]]:
    routes = [
        {"path": r.path, "name": r.name, "methods": list(r.methods)} for r in app.routes
    ]
    return {"available_routes": routes}


@app.get("/favicon.ico")
def favicon() -> FileResponse:
    return FileResponse("./karatel/images/favicon.png")
