from fastapi import FastAPI
from fastapi.responses import FileResponse

from karatel.core.hero import HeroFactory
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
    the_hero = HeroFactory.generate(ConsoleOutput())
    return HeroFactory.hero_to_dict(the_hero)
