# -*- coding: utf-8 -*-
from __future__ import annotations

import pickle
import sqlite3
from typing import TYPE_CHECKING

from karatel.utils.settings import DEBUG, LOG, SQLITE_PATH
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


def select_heroes(
    output: OutputSpace,
    table_name: str,
    hero_name: str | None = None,
    hero_id: int | None = None,
    conn: sqlite3.Connection | None = None,
) -> list:
    """
    Універсальна функція вибірки.
    Якщо hero_name | hero_id надано, шукає героя за іменем | id.
    Якщо hero_name and hero_id = None, повертає список усіх героїв.
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

    sql = f"SELECT * FROM {table_name}{sql_where} ORDER BY id"

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


# def insert_hero(hero: Hero, table_name: str) -> None:
#     """Вставка героя в БД -- новий запис або перезапис"""
#
#     table_name = sanitize_word(table_name)
#     if not table_name:
#         return
#
#     json_data = json.dumps(HeroFactory.hero_to_dict(hero), ensure_ascii=False)
#     insert = False
#
#     try:
#         with sqlite3.connect(SQLITE_PATH) as connection:
#
#             old_data = select_heroes(
#                 hero.output, table_name, hero_name=hero.name, conn=connection
#             )
#             if not old_data:
#                 insert = True
#
#             create_hero_table(hero.output, connection, table_name)
#
#             cursor = connection.cursor()
#             try:
#                 if insert:
#                     cursor.execute(
#                         f"INSERT INTO {table_name} (name, data) VALUES (?, ?)",
#                         (hero.name, json_data),
#                     )
#                     hero_id = cursor.lastrowid
#                     hero.output.write(
#                         f"Герой '{hero.name}' збережений з ID: {hero_id}", log=DEBUG
#                     )
#                 else:
#                     cursor.execute(
#                         f"""UPDATE {table_name}
#                         SET data = ?
#                         WHERE id = (
#                             SELECT MIN(id)
#                             FROM {table_name}
#                             WHERE name = ?
#                         );
#                         """,
#                         (json_data, hero.name),
#                     )
#                     hero.output.write(
#                         f"Герой '{hero.name}' оновлений. ID: {old_data[0][0]}",
#                         log=DEBUG,
#                     )
#             finally:
#                 cursor.close()
#
#     except sqlite3.Error as e:
#         hero.output.write(f"Помилка SQLite: {e}", log=DEBUG)


def delete_row_by_id(output: OutputSpace, table_name: str, row_id: int) -> bool:
    """Видалення запису по ID"""

    table_name = sanitize_word(table_name)
    if not table_name:
        return False

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            if not table_exists(output, connection, table_name):
                return False

            cursor = connection.cursor()
            try:
                cursor.execute(f"DELETE FROM {table_name} WHERE id = ?;", (row_id,))
                if cursor.rowcount == 0:
                    output.write(
                        f"Запис з №{row_id} не знайдено у таблиці '{table_name}'.",
                        log=DEBUG,
                    )
                    return False
            finally:
                cursor.close()
            output.write(
                f"Запис з №{row_id} успішно видалено з таблиці '{table_name}'",
                log=DEBUG,
            )
            return True

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: '{e}'", log=DEBUG)
        return False


def create_hero_and_map_table(
    output: OutputSpace, conn: sqlite3.Connection, table_name: str
) -> None:
    """Створення таблиці для зберігання героя та мапи"""

    if table_exists(output, conn, table_name):
        output.write(f"Таблиця '{table_name}' вже існує", log=DEBUG)
    else:
        cursor = conn.cursor()
        try:
            sql = f"""CREATE TABLE {table_name} (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        hero BLOB NOT NULL,
        map BLOB NOT NULL
            )"""
            cursor.execute(sql)
        finally:
            cursor.close()
        output.write(f"Таблицю '{table_name}' успішно створено", log=DEBUG)


def insert_hero_and_map(hero: Hero, game_map: list | None, table_name: str) -> None:
    """Вставка героя в БД -- новий запис або перезапис"""

    table_name = sanitize_word(table_name)
    if not table_name:
        return

    pickled_hero = pickle.dumps(hero)
    pickled_map = pickle.dumps(game_map)

    insert = False

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            old_data = select_heroes(
                hero.output, table_name, hero_name=hero.name, conn=connection
            )
            if not old_data:
                insert = True

            create_hero_and_map_table(hero.output, connection, table_name)

            cursor = connection.cursor()
            try:
                if insert:
                    cursor.execute(
                        f"INSERT INTO {table_name} (name, hero, map) VALUES (?, ?, ?)",
                        (hero.name, pickled_hero, pickled_map),
                    )
                    hero_id = cursor.lastrowid
                    hero.output.write(
                        f"Герой '{hero.name}' збережений з ID: {hero_id}", log=DEBUG
                    )
                else:
                    cursor.execute(
                        f"""UPDATE {table_name}
                        SET hero = ?,
                            map = ? 
                        WHERE id = (
                            SELECT MIN(id) 
                            FROM {table_name} 
                            WHERE name = ?
                        );
                        """,
                        (pickled_hero, pickled_map, hero.name),
                    )
                    hero.output.write(
                        f"Герой '{hero.name}' оновлений. ID: {old_data[0][0]}",
                        log=DEBUG,
                    )
            finally:
                cursor.close()

    except sqlite3.Error as e:
        hero.output.write(f"Помилка SQLite: {e}", log=DEBUG)


def sqlite_hero_and_map_loader(
    output: OutputSpace,
    table_name: str,
    hero_id: int,
    log: bool = LOG,
):
    """Завантаження героя"""

    sql_data = select_heroes(output, table_name, hero_id=hero_id)

    hero = pickle.loads(sql_data[0][2])
    the_map = pickle.loads(sql_data[0][3])

    output.write(
        f"Героя {hero.name} завантажено.",
        log=log,
    )
    return hero, the_map


def sqlite_hero_and_map_saver(
    hero: Hero, game_map: list, table_name, log: bool = LOG
) -> None:
    """Збереження героя"""

    insert_hero_and_map(hero, game_map, table_name)
    hero.output.write(
        f"Героя {hero.name} збережено.",
        log=log,
    )


def insert_user(
    output: OutputSpace,
    username: str,
    hashed_password: bytes,
    table_name: str,
    log: bool = LOG,
) -> bool:

    def _create_users_table() -> None:
        """Створення таблиці для користувачів"""
        cur = connection.cursor()
        try:
            sql = f"""CREATE TABLE IF NOT EXISTS {table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                hashed_password BLOB NOT NULL
            )"""
            cur.execute(sql)
        finally:
            cur.close()

    table_name = sanitize_word(table_name)

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:

            _create_users_table()

            cursor = connection.cursor()
            try:
                cursor.execute(
                    f"INSERT INTO {table_name} (username, hashed_password) VALUES (?, ?)",
                    (username, hashed_password),
                )
                if DEBUG:
                    output.write(
                        f"Користувача '{username}' збережено. ID: {cursor.lastrowid}",
                        log=DEBUG,
                    )
                return True
            finally:
                cursor.close()

    except sqlite3.IntegrityError:
        output.write(
            f"Користувач з іменем '{username}' вже існує. Виберіть інше ім'я.", log=log
        )
        return False

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite: {e}", log=DEBUG)
        return False


def select_user(
    output: OutputSpace, username: str, table_name: str, log=LOG
) -> tuple[int, bytes] | None:

    table_name = sanitize_word(table_name)

    try:
        with sqlite3.connect(SQLITE_PATH) as connection:
            cursor = connection.cursor()
            try:
                sql = f"SELECT id, hashed_password FROM {table_name} WHERE username = ?"
                cursor.execute(sql, (username,))
                result = cursor.fetchone()
                if result is None:
                    output.write(f"Користувач {username} не знайдений", log=log)
                return result
            finally:
                cursor.close()

    except sqlite3.Error as e:
        output.write(f"Помилка SQLite під час пошуку користувача: {e}", log=DEBUG)
        return None
