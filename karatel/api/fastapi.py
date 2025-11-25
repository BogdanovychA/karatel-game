from fastapi import FastAPI
from fastapi.responses import FileResponse

from karatel.core.hero import HeroFactory
from karatel.ui.abstract import ConsoleOutput

app = FastAPI(
    title="Karatel Game API",
)


@app.get("/favicon.ico")
def favicon():
    return FileResponse("./karatel/images/favicon.png")


@app.get("/generate_hero")
def generate_hero():
    the_hero = HeroFactory.generate(ConsoleOutput())
    return HeroFactory.hero_to_dict(the_hero)
