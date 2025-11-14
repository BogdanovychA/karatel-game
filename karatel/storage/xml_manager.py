# -*- coding: utf-8 -*-
from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import TYPE_CHECKING

from karatel.core.hero import Hero
from karatel.core.items import ITEMS, SHIELDS, WEAPONS
from karatel.core.professions import PROFESSIONS
from karatel.core.skills import SKILLS
from karatel.utils.settings import DEBUG, LOG
from karatel.utils.utils import obj_finder

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace


def xml_hero_saver(hero: Hero, path: str, log: bool = LOG) -> None:
    """Збереження героя"""

    root = ET.Element('hero')

    ET.SubElement(root, "name").text = hero.name
    ET.SubElement(root, "profession").text = hero.profession.name
    ET.SubElement(root, "experience").text = str(hero.experience)
    ET.SubElement(root, "lives").text = str(hero.lives)
    ET.SubElement(root, "money").text = str(hero.money)

    skills_root = ET.SubElement(root, 'skills')
    for skill in hero.skills:
        ET.SubElement(skills_root, "skill").text = skill.name

    inventory_root = ET.SubElement(root, 'inventory')
    for item in hero.inventory:
        ET.SubElement(inventory_root, "item").text = item.name

    ET.SubElement(root, "left_hand").text = hero.left_hand.name
    ET.SubElement(root, "right_hand").text = hero.right_hand.name

    tree = ET.ElementTree(root)

    try:
        with open(path, "wb") as file:
            tree.write(file, encoding="utf-8", xml_declaration=True)

        hero.output.write(f"Героя {hero.name} збережено", log=log)

    except Exception as e:
        hero.output.write(f"Сталася помилка при збереженні файлу: {e}", log=log)


def xml_hero_loader(output: OutputSpace, path: str, log: bool = LOG) -> Hero | None:
    """Завантаження героя"""

    def _create_list(parent_tag: str, child_tag: str, base: tuple) -> list:
        """Допоміжна функція для забезпечення DRY"""

        the_list: list = []
        parent_root = root.find(parent_tag)
        if parent_root is not None:
            tags = parent_root.findall(child_tag)
            for tag in tags:
                the_list.append(obj_finder(tag.text, base))

        return the_list

    def _find_text(text: str) -> str | None:
        """Допоміжна функція для забезпечення DRY"""
        element = root.find(text)
        if element is not None and element.text:
            return element.text
        else:
            return None

    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except FileNotFoundError:
        output.write(f"Помилка: файл {path} не знайдено", log=DEBUG)
        return None
    except Exception as e:
        output.write(f"Помилка завантаження XML: {e}", log=DEBUG)
        return None

    hero = Hero(
        output=output,
        name=_find_text("name"),
        profession=obj_finder(_find_text("profession"), PROFESSIONS),
        experience=int(_find_text("experience") or "0"),
    )
    hero.lives = int(_find_text("lives") or "1")
    hero.money = int(_find_text("money") or "0")
    hero.right_hand = obj_finder(_find_text("right_hand"), WEAPONS)
    hero.left_hand = obj_finder(_find_text("left_hand"), SHIELDS)
    hero.inventory = _create_list('inventory', 'item', ITEMS)
    hero.skills = _create_list('skills', 'skill', SKILLS)

    hero.output.write(f"Героя {hero.name} завантажено", log=log)
    return hero
