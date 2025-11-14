# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import sqlite3
from typing import TYPE_CHECKING

from karatel.core.hero import HeroFactory
from karatel.utils.settings import DEBUG, HERO_SQL_TABLE, LOG, SQLITE_PATH
from karatel.utils.utils import sanitize_word

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.ui.abstract import OutputSpace


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


def delete_table(output: OutputSpace, table_name: str) -> bool:
    """Видалення таблиці по назві"""

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


def create_hero_table(
    output: OutputSpace, conn: sqlite3.Connection, table_name: str
) -> None:
    """Створення таблиці для зберігання героя"""

    if table_exists(output, conn, table_name):
        output.write(f"Таблиця '{table_name}' вже існує", log=DEBUG)
    else:
        cursor = conn.cursor()
        try:
            sql = f"""CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                data TEXT NOT NULL
            )"""
            cursor.execute(sql)
        finally:
            cursor.close()
        output.write(f"Таблицю '{table_name}' успішно створено", log=DEBUG)


def select_heroes(
    output: OutputSpace,
    table_name: str,
    hero_name: str | None = None,
    hero_id: int | None = None,
    conn: sqlite3.Connection | None = None,
) -> list:
    """
    Універсальна функція вибірки.
    Якщо hero_name надано, шукає героя за іменем.
    Якщо hero_name = None, повертає список усіх героїв.
    """

    if not conn:
        table_name = sanitize_word(table_name)
        if not table_name:
            return []

    sql_where = ""

    if hero_name is not None:
        sql_where = " WHERE name = ?"
    elif hero_id is not None:
        sql_where = " WHERE id = ?"

    sql = f"SELECT id, name, data FROM {table_name}{sql_where} ORDER BY id"

    def _select():
        """Допоміжна функція для забезпечення DRY"""

        cursor = connection.cursor()
        try:
            if hero_name is not None:
                cursor.execute(sql, (hero_name,))
            elif hero_id is not None:
                cursor.execute(sql, (hero_id,))
            else:
                cursor.execute(sql)
            return cursor.fetchall()
        finally:
            cursor.close()

    try:
        if not conn:
            with sqlite3.connect(SQLITE_PATH) as connection:
                if not table_exists(output, connection, table_name):
                    return []
                return _select()
        else:
            connection = conn
            if not table_exists(output, connection, table_name):
                return []
            return _select()

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: '{e}'", log=DEBUG)
        return []


def insert_hero(hero: Hero, table_name: str) -> None:
    """Вставка героя в БД -- новий запис або перезапис"""

    table_name = sanitize_word(table_name)
    if not table_name:
        return

    json_data = json.dumps(HeroFactory.hero_to_dict(hero), ensure_ascii=False)
    insert = False

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            old_data = select_heroes(hero.output, table_name, hero.name, connection)
            if not old_data:
                insert = True

            create_hero_table(hero.output, connection, table_name)

            cursor = connection.cursor()
            try:
                if insert:
                    cursor.execute(
                        f"INSERT INTO {table_name} (name, data) VALUES (?, ?)",
                        (hero.name, json_data),
                    )
                    hero_id = cursor.lastrowid
                    hero.output.write(
                        f"Герой '{hero.name}' збережений з ID: {hero_id}", log=DEBUG
                    )
                else:
                    # cursor.execute(
                    #     f"UPDATE {table_name} SET data = ? WHERE name = ?",
                    #     (json_data, hero.name),
                    # )
                    cursor.execute(
                        f"""UPDATE {table_name}
                        SET data = ? 
                        WHERE id = (
                            SELECT MIN(id) 
                            FROM {table_name} 
                            WHERE name = ?
                        );
                        """,
                        (json_data, hero.name),
                    )
                    hero.output.write(
                        f"Герой '{hero.name}' оновлений. ID: {old_data[0][0]}",
                        log=DEBUG,
                    )
            finally:
                cursor.close()

    except sqlite3.Error as e:
        hero.output.write(f"Помилка SQLite: {e}", log=DEBUG)


def sqlite_hero_saver(hero: Hero, log: bool = LOG) -> None:
    """Збереження героя"""

    insert_hero(hero, HERO_SQL_TABLE)
    hero.output.write(
        f"Героя {hero.name} збережено.",
        log=log,
    )


def sqlite_hero_loader_by_id(
    output: OutputSpace,
    hero_id: int,
    log: bool = LOG,
) -> Hero:

    sql_data = select_heroes(output, HERO_SQL_TABLE, hero_id=hero_id)
    json_data = sql_data[0][2]
    data = json.loads(json_data)

    output.write(
        f"Героя {data["name"]} завантажено.",
        log=log,
    )
    return HeroFactory.dict_to_hero(output, data)


def sqlite_hero_loader_by_name(
    output: OutputSpace,
    hero_name: str,
    log: bool = LOG,
) -> Hero:
    """Завантаження героя"""

    # Робимо вибірку по імені героя. Якщо декілька -- беремо перший запис
    # З нех беремо третю комірку, саме там дані в форматі JSON
    sql_data = select_heroes(output, HERO_SQL_TABLE, hero_name=hero_name)
    json_data = sql_data[0][2]
    data = json.loads(json_data)

    output.write(
        f"Героя {data["name"]} завантажено.",
        log=log,
    )
    return HeroFactory.dict_to_hero(output, data)
