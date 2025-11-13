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
from karatel.utils.utils import hero_to_dict, obj_finder, sanitize_word

# from karatel.utils.constants import FORBIDDEN_SQL_CHARS


if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace

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


def check_word(output: OutputSpace, word: str) -> bool:
    if not word or word is True:
        output.write(f"'{word}' не може бути пустим, None, False або True", log=DEBUG)
        return False
    for char in word:
        if char in FORBIDDEN_SQL_CHARS:
            output.write(
                f"Неможливо виконати: '{word}' містить заборонені символи", log=DEBUG
            )
            return False
    return True


def table_exists(
    output: OutputSpace, conn: sqlite3.Connection, table_name: str
) -> bool | None:
    """Перевіряє, чи таблиця з такою назвою вже існує."""

    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        if cursor.fetchone() is not None:
            output.write(f"Таблиця '{table_name}' існує", log=DEBUG)
            return True
        else:
            output.write(f"Таблиця '{table_name}' не існує", log=DEBUG)
            return False
    finally:
        cursor.close()


def create_hero_table(
    output: OutputSpace, conn: sqlite3.Connection, table_name: str
) -> None:

    sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                data TEXT NOT NULL
            )"""

    if table_exists(output, conn, table_name):
        output.write(f"Таблиця '{table_name}' вже існує", log=DEBUG)
    else:
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        finally:
            cursor.close()
        output.write(f"Таблицю '{table_name}' успішно створено", log=DEBUG)


def insert_hero(hero: Hero, table_name: str) -> int | None:

    table_name = sanitize_word(table_name)
    if not table_name:
        return None

    data = hero_to_dict(hero)
    json_data = json.dumps(data, ensure_ascii=False)

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            create_hero_table(hero.output, connection, table_name)

            cursor = connection.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO {table_name} (name, data) VALUES (?, ?)",
                    (hero.name, json_data),
                )
                hero_id = cursor.lastrowid
            finally:
                cursor.close()

            hero.output.write(
                f"Герой '{hero.name}' збережений з ID: {hero_id}", log=DEBUG
            )

        return hero_id

    except sqlite3.Error as e:
        hero.output.write(f"Помилка SQLite: {e}", log=DEBUG)
        return None


def delete_table(output: OutputSpace, table_name: str) -> bool:

    table_name = sanitize_word(table_name)
    if not table_name:
        return False

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            if not table_exists(output, connection, table_name):
                return False

            cursor = connection.cursor()
            try:
                cursor.execute(f"DROP TABLE {table_name}")
            finally:
                cursor.close()
            output.write(f"Таблицю '{table_name}' успішно видалено", log=DEBUG)
            return True

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: '{e}'", log=DEBUG)
        return False


def select_all_heroes(output: OutputSpace, table_name: str) -> list | bool:

    table_name = sanitize_word(table_name)
    if not table_name:
        return False

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            if not table_exists(output, connection, table_name):
                return False

            cursor = connection.cursor()
            try:
                # cursor.execute(f"SELECT id, name FROM {table_name} ORDER BY id DESC")
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY id")
                all_heroes = cursor.fetchall()
            finally:
                cursor.close()

            return all_heroes

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: '{e}'", log=DEBUG)
        return False


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
