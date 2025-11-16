# -*- coding: utf-8 -*-
import psycopg

from karatel.storage.postgresql_config import (
    PSQL_DB,
    PSQL_HOST,
    PSQL_PASS,
    PSQL_PORT,
    PSQL_USER,
)
from karatel.utils.utils import sanitize_word


def connect():

    try:
        connection = psycopg.connect(
            dbname=PSQL_DB,
            user=PSQL_USER,
            password=PSQL_PASS,
            host=PSQL_HOST,
            port=PSQL_PORT,
        )
        print("З'єднання з PostgreSQL встановлено!")
        return connection

    except psycopg.OperationalError as e:
        print(f"Помилка при підключенні: {e}")
        raise


def table_exists(
    connection: psycopg.Connection, table_name: str, schema_name: str = 'public'
) -> bool | None:
    """Перевіряє, чи таблиця з такою назвою вже існує в PostgreSQL."""

    # cursor = None
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
                print(f"Таблиця '{table_name}' існує")
                return True
            else:
                print(f"Таблиця '{table_name}' не існує")
                return False

    except psycopg.Error as e:
        print(f"Помилка при перевірці існування таблиці: {e}")
        return None

    # finally:
    #     if cursor:
    #         cursor.close()
    #         print("Курсор закрито")


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
                cursor.execute(f"DROP TABLE {table_name}")
                print(f"Таблицю '{table_name}' успішно видалено")
                return True
    except psycopg.OperationalError as e:
        print(f"Помилка з'єднання: {e}")
        return False

    except Exception as e:
        print(f"Помилка: {e}")
        return False

    finally:
        if connection:
            connection.close()
            print("З'єднання закрито.")


def create_hero_table(connection: psycopg.Connection, table_name: str) -> None:
    """Створення таблиці для зберігання героя"""

    if table_exists(connection, table_name):
        print(f"Таблиця '{table_name}' вже існує")

    else:
        with connection.cursor() as cursor:
            sql = f"""CREATE TABLE {table_name} (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
                # data TEXT NOT NULL
            )"""
            cursor.execute(sql)
            print(f"Таблицю '{table_name}' успішно створено")
