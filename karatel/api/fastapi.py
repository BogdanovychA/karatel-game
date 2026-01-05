# -*- coding: utf-8 -*-


from fastapi import FastAPI

from karatel.api.handlers import add_handlers
from karatel.api.routers import hero, items, next_number, root, tic_tac_toe_3x3

app = FastAPI(
    title="Karatel Game API",
    root_path="/api",
    openapi_url="/openapi.json",
    docs_url="/docs",
)

# Підключаємо маршрути
app.include_router(root.router)
app.include_router(items.router, prefix="/items")
app.include_router(hero.router, prefix="/hero")
app.include_router(next_number.router, prefix="/next-number")
app.include_router(tic_tac_toe_3x3.router, prefix="/ttt")


# Додаємо обробники помилок
add_handlers(app)
