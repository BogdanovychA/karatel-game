# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sqlite3
from typing import TYPE_CHECKING

from karatel.core.hero import Hero
from karatel.utils.settings import DEBUG, SQLITE_PATH

# from karatel.core.hero import Hero
# from karatel.core.items import ITEMS, SHIELDS, WEAPONS
# from karatel.core.professions import PROFESSIONS
# from karatel.core.skills import SKILLS
# from karatel.utils.settings import DEBUG, LOG
from karatel.utils.utils import hero_to_dict, obj_finder

# from karatel.utils.constants import FORBIDDEN_SQL_CHARS


if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace

# connection = sqlite3.connect(':memory:')
# connection = sqlite3.connect(SQLITE_PATH)
# connection = sqlite3.connect("../saves/karatel.db")

DEBUG = True

FORBIDDEN_SQL_CHARS = (
    "'",
    '"',
    ';',
    '--',
    '*',
    '/',
    '+',
    '=',
    '>',
    '<',
    '!',
    '@',
    '#',
    '$',
    '%',
    '^',
    '&',
    '(',
    ')',
    '[',
    ']',
    '{',
    '}',
    '`',
    '~',
    '|',
    '\\',
    '?',
    '.',
    ',',
    ' ',
)


def check_word(word) -> bool:
    if not word:
        return False
    for char in word:
        if char in FORBIDDEN_SQL_CHARS:
            return False
    return True


def table_exists(output: OutputSpace, table_name: str) -> bool | None:
    """Перевіряє, чи таблиця з такою назвою вже існує."""

    if not check_word(table_name):
        output.write(
            "Неможливо перевірити таблицю: містить заборонені символи", log=DEBUG
        )
        return None

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:
            cursor = connection.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )

        if cursor.fetchone() is not None:
            output.write(f"Таблиця {table_name} існує", log=DEBUG)
            return True
        else:
            output.write(f"Таблиця {table_name} не існує", log=DEBUG)
            return False

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: {e}", log=DEBUG)

        return None


def create_table(output: OutputSpace, table_name: str) -> None:

    if not check_word(table_name):
        output.write(
            "Неможливо створити таблицю: містить заборонені символи", log=DEBUG
        )
        return

    sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                data TEXT NOT NULL
            )"""

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:
            cursor = connection.cursor()

            if table_exists(output, table_name):
                output.write(f"Таблиця {table_name} вже існує", log=DEBUG)
            else:
                output.write(f"Таблицю {table_name} успішно створено", log=DEBUG)

            cursor.execute(sql)

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: {e}", log=DEBUG)


def delete_table(output: OutputSpace, table_name: str) -> None:
    try:
        with sqlite3.connect(SQLITE_PATH) as connection:
            cursor = connection.cursor()

        if not check_word(table_name):
            output.write(
                "Неможливо видалити таблицю: містить заборонені символи", log=DEBUG
            )
            return

        cursor.execute(f"DROP TABLE {table_name}")
        output.write("Таблицю успішно видалено", log=DEBUG)

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: {e}", log=DEBUG)


def insert_hero(hero: Hero, table_name: str) -> int | None:

    create_table(hero.output, table_name)

    data = hero_to_dict(hero)
    json_data = json.dumps(data, ensure_ascii=False)

    if not check_word(table_name):
        hero.output.write(
            "Неможливо записати в таблицю: містить заборонені символи", log=DEBUG
        )
        return None

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:
            cursor = connection.cursor()

            cursor.execute(
                f"INSERT INTO {table_name} (name, data) VALUES (?, ?)",
                (hero.name, json_data),
            )

            hero_id = cursor.lastrowid
            hero.output.write(
                f"Герой '{hero.name}' збережений з ID: {hero_id}", log=DEBUG
            )

        return hero_id

    except sqlite3.Error as e:
        hero.output.write(f"Помилка SQLite: {e}", log=DEBUG)
        return None


# cursor.execute("SELECT * FROM heroes")
# print(cursor.fetchall())
# cursor.execute("SELECT * FROM heroes")
# print(cursor.fetchmany(1))
# cursor.execute("SELECT * FROM heroes")
# print(cursor.fetchone())


# def sqlite_hero_saver(hero: Hero, path: str, log: bool = LOG) -> None:
#     """Збереження героя"""
#
#     the_dict: dict = {
#         "name": hero.name,
#         "profession": hero.profession.name,
#         "experience": hero.experience,
#         "lives": hero.lives,
#         "money": hero.money,
#         "left_hand": hero.left_hand.name,
#         "right_hand": hero.right_hand.name,
#         "skills": [],
#         "inventory": [],
#     }
#     for skill in hero.skills:
#         the_dict["skills"].append(skill.name)
#     for item in hero.inventory:
#         the_dict["inventory"].append(item.name)
#
#     try:
#         with open(path, 'w', encoding='utf-8') as file:
#             json.dump(the_dict, file, indent=4, ensure_ascii=False)
#
#         hero.output.write(f"Героя {hero.name} збережено", log=log)
#
#     except Exception as e:
#         hero.output.write(f"Сталася помилка при збереженні файлу: {e}", log=log)
#
#
# def sqlite_hero_loader(output: OutputSpace, path: str, log: bool = LOG) -> Hero | None:
#     """Завантаження героя"""
#
#     def _create_list(input_list: list, base: tuple) -> list:
#         """Допоміжна функція для забезпечення DRY"""
#         the_list = []
#         for item in input_list:
#             the_list.append(obj_finder(item, base))
#         return the_list
#
#     try:
#         with open(path, 'r', encoding='utf-8') as file:
#             the_dict = json.load(file)
#
#         hero = Hero(
#             output=output,
#             name=the_dict["name"],
#             profession=obj_finder(the_dict["profession"], PROFESSIONS),
#             experience=int(the_dict["experience"] or "0"),
#         )
#         hero.lives = int(the_dict["lives"] or "1")
#         hero.money = int(the_dict["money"] or "0")
#         hero.right_hand = obj_finder(the_dict["right_hand"], WEAPONS)
#         hero.left_hand = obj_finder(the_dict["left_hand"], SHIELDS)
#         hero.inventory = _create_list(the_dict["inventory"], ITEMS)
#         hero.skills = _create_list(the_dict["skills"], SKILLS)
#
#         hero.output.write(f"Героя {hero.name} завантажено", log=log)
#         return hero
#
#     except FileNotFoundError:
#         output.write(f"Помилка: Файл '{path}' не знайдено.", log=DEBUG)
#     except json.JSONDecodeError:
#         output.write(
#             f"Помилка: Файл '{path}' містить недійсний формат JSON.", log=DEBUG
#         )
