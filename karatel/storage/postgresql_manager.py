# -*- coding: utf-8 -*-
from __future__ import annotations

import pickle
from typing import TYPE_CHECKING

import psycopg
from psycopg.sql import SQL, Identifier

from karatel.storage.postgresql_config import (
    PSQL_DB,
    PSQL_HOST,
    PSQL_PASS,
    PSQL_PORT,
    PSQL_USER,
)
from karatel.utils.settings import DEBUG
from karatel.utils.utils import sanitize_word

if TYPE_CHECKING:
    from karatel.core.hero import Hero


def connect():

    try:
        connection = psycopg.connect(
            dbname=PSQL_DB,
            user=PSQL_USER,
            password=PSQL_PASS,
            host=PSQL_HOST,
            port=PSQL_PORT,
        )
        if DEBUG:
            print("З'єднання з PostgreSQL встановлено!")
        return connection

    except psycopg.OperationalError as e:
        if DEBUG:
            print(f"Помилка при підключенні: {e}")
        raise


def table_exists(
    connection: psycopg.Connection, table_name: str, schema_name: str = 'public'
) -> bool | None:
    """Перевіряє, чи таблиця з такою назвою вже існує в PostgreSQL."""

    try:
        with connection.cursor() as cursor:
            sql_query = """
            SELECT EXISTS (
                SELECT 1 
                FROM pg_tables 
                WHERE schemaname = %s AND tablename = %s
            );
            """
            cursor.execute(sql_query, (schema_name, table_name))
            exists = cursor.fetchone()[0]

            if exists:
                if DEBUG:
                    print(f"Таблиця '{table_name}' існує")
                return True
            else:
                if DEBUG:
                    print(f"Таблиця '{table_name}' не існує")
                return False

    except psycopg.Error as e:
        if DEBUG:
            print(f"Помилка при перевірці існування таблиці: {e}")
        return None


def delete_table(table_name: str) -> bool:
    """Видалення таблиці по назві"""

    table_name = sanitize_word(table_name)
    if not table_name:
        return False

    connection = None
    try:
        connection = connect()
        with connection:
            if not table_exists(connection, table_name):
                return False

            with connection.cursor() as cursor:

                sql_template = SQL("DROP TABLE {}")
                sql_query = sql_template.format(Identifier(table_name))

                cursor.execute(sql_query)
                if DEBUG:
                    print(f"Таблицю '{table_name}' успішно видалено")
                return True

    except psycopg.OperationalError as e:
        if DEBUG:
            print(f"Помилка з'єднання: {e}")
        return False

    except psycopg.Error as e:
        if DEBUG:
            print(f"Помилка при видаленні таблиці: {e}")
        return False

    finally:
        if connection:
            connection.close()
            if DEBUG:
                print("З'єднання закрито.")


def create_hero_table(connection: psycopg.Connection, table_name: str) -> None:
    """Створення таблиці для зберігання героя"""

    if table_exists(connection, table_name):
        print(f"Таблиця '{table_name}' вже існує")

    else:
        try:
            with connection.cursor() as cursor:
                sql_template = SQL(
                    """CREATE TABLE {} (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    hero BYTEA NOT NULL,
                    map BYTEA NOT NULL
                    )"""
                )
                sql_query = sql_template.format(Identifier(table_name))

                cursor.execute(sql_query)
                if DEBUG:
                    print(f"Таблицю '{table_name}' успішно створено")

        except psycopg.Error as e:
            if DEBUG:
                print(f"Помилка при створенні таблиці: {e}")


def select_heroes(
    table_name: str,
    hero_name: str | None = None,
    hero_id: int | None = None,
    conn: psycopg.Connection | None = None,
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

    sql_where = SQL("")

    if hero_name is not None:
        sql_where = SQL(" WHERE name = %s")
    elif hero_id is not None:
        sql_where = SQL(" WHERE id = %s")

    sql_query = SQL(" ").join(
        [
            SQL("SELECT * FROM {}").format(Identifier(table_name)),
            sql_where,
            SQL("ORDER BY id"),
        ]
    )

    def _select():
        """Допоміжна функція для забезпечення DRY"""

        with connection.cursor() as cursor:
            if hero_name is not None:
                cursor.execute(sql_query, (hero_name,))
            elif hero_id is not None:
                cursor.execute(sql_query, (hero_id,))
            else:
                cursor.execute(sql_query)
            return cursor.fetchall()

    try:
        if not conn:
            connection = None
            try:
                connection = connect()
                with connection:
                    if not table_exists(connection, table_name):
                        return []
                    return _select()
            except psycopg.OperationalError as e:
                if DEBUG:
                    print(f"Помилка підключення до БД: {e}")
                raise

            finally:
                if connection:
                    connection.close()
                    if DEBUG:
                        print("З'єднання закрито.")

        else:
            connection = conn
            if not table_exists(connection, table_name):
                return []
            return _select()

    except psycopg.Error as e:
        if DEBUG:
            print(f"Помилка при виборці героїв: {e}")
        return []


def insert_hero_and_map(hero: Hero, game_map: list | None, table_name: str) -> None:
    """Вставка героя в БД -- новий запис або перезапис"""

    table_name = sanitize_word(table_name)
    if not table_name:
        return

    pickled_hero = pickle.dumps(hero)
    pickled_map = pickle.dumps(game_map)

    insert = False

    connection = None

    try:
        connection = connect()
        with connection:

            old_data = select_heroes(table_name, hero_name=hero.name, conn=connection)
            if not old_data:
                insert = True

            create_hero_table(connection, table_name)

            with connection.cursor() as cursor:
                if insert:

                    sql_template = SQL(
                        "INSERT INTO {} (name, hero, map) VALUES (%s, %s, %s) RETURNING id;"
                    )
                    sql_query = sql_template.format(Identifier(table_name))

                    cursor.execute(sql_query, (hero.name, pickled_hero, pickled_map))

                    hero_id = cursor.fetchone()[0]
                    if DEBUG:
                        print(f"Герой '{hero.name}' збережений з ID: {hero_id}")
                else:
                    sql_template = SQL(
                        """UPDATE {}
                        SET hero = %s,
                            map = %s 
                        WHERE id = (
                            SELECT MIN(id) 
                            FROM {} 
                            WHERE name = %s
                        );
                        """
                    )
                    sql_query = sql_template.format(
                        Identifier(table_name), Identifier(table_name)
                    )

                    cursor.execute(sql_query, (pickled_hero, pickled_map, hero.name))

                    if DEBUG:
                        print(f"Герой '{hero.name}' оновлений. ID: {old_data[0][0]}")

    except psycopg.Error as e:
        if DEBUG:
            print(f"Помилка при додаванні даних в БД: {e}")

    finally:
        if connection:
            connection.close()
            if DEBUG:
                print("З'єднання закрито.")


def delete_row_by_id(table_name: str, row_id: int) -> bool:
    """Видалення запису по ID"""

    table_name = sanitize_word(table_name)
    if not table_name:
        return False

    connection = None
    try:
        connection = connect()
        with connection:
            if not table_exists(connection, table_name):
                return False

            with connection.cursor() as cursor:

                sql_template = SQL("DELETE FROM {} WHERE id = %s;")
                sql_query = sql_template.format(Identifier(table_name))

                cursor.execute(sql_query, (row_id,))

                if cursor.rowcount == 0:
                    if DEBUG:
                        print(
                            f"Запис з №{row_id} не знайдено у таблиці '{table_name}'."
                        )
                    return False
            if DEBUG:
                print(f"Запис з №{row_id} успішно видалено з таблиці '{table_name}'")
            return True

    except psycopg.OperationalError as e:
        if DEBUG:
            print(f"Помилка підключення до БД: {e}")
        return False

    except psycopg.Error as e:
        if DEBUG:
            print(f"Помилка при додаванні даних в БД: {e}")
        return False

    finally:
        if connection:
            connection.close()
            if DEBUG:
                print("З'єднання закрито.")
