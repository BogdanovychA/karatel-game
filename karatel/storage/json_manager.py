# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from typing import TYPE_CHECKING

from karatel.core.hero import HeroFactory
from karatel.utils.settings import DEBUG, LOG

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.ui.abstract import OutputSpace


def json_hero_saver(hero: Hero, path: str, log: bool = LOG) -> None:
    """Збереження героя"""

    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(
                HeroFactory.hero_to_dict(hero), file, indent=4, ensure_ascii=False
            )

        hero.output.write(f"Героя {hero.name} збережено", log=log)

    except Exception as e:
        hero.output.write(f"Сталася помилка при збереженні файлу: {e}", log=log)


def json_hero_loader(output: OutputSpace, path: str) -> Hero | None:
    """Завантаження героя"""

    try:
        with open(path, 'r', encoding='utf-8') as file:
            the_dict = json.load(file)
        return HeroFactory.dict_to_hero(output, the_dict)

    except FileNotFoundError:
        output.write(f"Помилка: Файл '{path}' не знайдено.", log=DEBUG)
        return None
    except json.JSONDecodeError:
        output.write(
            f"Помилка: Файл '{path}' містить недійсний формат JSON.", log=DEBUG
        )
        return None
