# -*- coding: utf-8 -*-
from __future__ import annotations

import json

from typing import TYPE_CHECKING

from karatel.core.hero import Hero
from karatel.core.items import ITEMS, SHIELDS, WEAPONS
from karatel.core.professions import PROFESSIONS
from karatel.core.skills import SKILLS
from karatel.utils.settings import DEBUG, LOG
from karatel.utils.utils import obj_finder

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace


def json_hero_saver(hero: Hero, path: str, log: bool = LOG) -> None:

    the_dict: dict = {
        "name": hero.name,
        "profession": hero.profession.name,
        "experience": hero.experience,
        "lives": hero.lives,
        "money": hero.money,
        "left_hand": hero.left_hand.name,
        "right_hand": hero.right_hand.name,
        "skills": [],
        "inventory": [],
    }
    for skill in hero.skills:
        the_dict["skills"].append(skill.name)
    for item in hero.inventory:
        the_dict["inventory"].append(item.name)

    try:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(the_dict, file, indent=4, ensure_ascii=False)

        hero.output.write(f"Героя {hero.name} збережено", log=log)

    except Exception as e:
        hero.output.write(f"Сталася помилка при збереженні файлу: {e}", log=log)


def json_hero_loader(output: OutputSpace, path: str, log: bool = LOG) -> Hero | None:

    def _create_list(input_list: list, base: tuple) -> list:
        the_list = []
        for item in input_list:
            the_list.append(obj_finder(item, base))
        return the_list

    try:
        with open(path, 'r', encoding='utf-8') as file:
            the_dict = json.load(file)

        hero = Hero(
            output=output,
            name=the_dict["name"],
            profession=obj_finder(the_dict["profession"], PROFESSIONS),
            experience=int(the_dict["experience"] or "0"),
        )
        hero.lives = int(the_dict["lives"] or "1")
        hero.money = int(the_dict["money"] or "0")
        hero.right_hand = obj_finder(the_dict["right_hand"], WEAPONS)
        hero.left_hand = obj_finder(the_dict["left_hand"], SHIELDS)
        hero.inventory = _create_list(the_dict["inventory"], ITEMS)
        hero.skills = _create_list(the_dict["skills"], SKILLS)

        hero.output.write(f"Героя {hero.name} завантажено", log=log)
        return hero

    except FileNotFoundError:
        output.write(f"Помилка: Файл '{path}' не знайдено.", log=DEBUG)
    except json.JSONDecodeError:
        output.write(
            f"Помилка: Файл '{path}' містить недійсний формат JSON.", log=DEBUG
        )
