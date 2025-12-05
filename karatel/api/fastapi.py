# -*- coding: utf-8 -*-


from fastapi import FastAPI

from karatel.api.handlers import add_handlers
from karatel.api.routers import hero, items, root

app = FastAPI(
    title="Karatel Game API",
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
    swagger_ui_parameters={"favicon": "/favicon.ico"},
)

# Підключаємо маршрути
app.include_router(root.router)
app.include_router(items.router, prefix="/items")
app.include_router(hero.router, prefix="/hero")


# Додаємо обробники помилок
add_handlers(app)
