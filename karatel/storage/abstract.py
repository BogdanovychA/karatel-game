# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from karatel.storage.sqlite_manager import (
    delete_row_by_id,
    insert_user,
    select_heroes,
    select_user,
    sqlite_hero_and_map_loader,
    sqlite_hero_and_map_saver,
)
from karatel.utils.settings import HERO_SQL_TABLE, USERS_SQL_TABLE

if TYPE_CHECKING:
    from karatel.core.hero import Hero


class SQLSaver(ABC):
    """'Відкритий простір' для збереження/завантаження користувача та героїв"""

    @abstractmethod
    def list_hero(self, *args, **kwargs) -> list:
        """Перегляд переліку героїв через 'відкритий простір'"""
        pass

    @abstractmethod
    def save(self, *args, hero: Hero, **kwargs) -> None:
        """Збереження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def load(self, *args, **kwargs) -> Hero:
        """Завантаження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def delete(self, *args, **kwargs) -> bool:
        """Видалення героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def register(self, *args, **kwargs) -> bool:
        """Реєстрація користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def login(self, *args, **kwargs) -> tuple[int, bytes] | None:
        """Авторизація користувача через 'відкритий простір'"""
        pass


class SQLiteSaver(SQLSaver):
    """Робота з SQLite"""

    def __init__(self):
        # self._path = SQLITE_PATH
        self._hero_table = HERO_SQL_TABLE
        self._users_table = USERS_SQL_TABLE

    def list_hero(self, *args, username: str, **kwargs) -> list:
        table_name = username + "_" + self._hero_table
        return select_heroes(*args, table_name=table_name, **kwargs)

    def save(self, *args, username: str, **kwargs) -> None:
        table_name = username + "_" + self._hero_table
        sqlite_hero_and_map_saver(*args, table_name=table_name, **kwargs)

    def load(self, *args, username: str, **kwargs) -> Hero:
        table_name = username + "_" + self._hero_table
        return sqlite_hero_and_map_loader(*args, table_name=table_name, **kwargs)

    def delete(self, *args, username: str, **kwargs) -> bool:
        table_name = username + "_" + self._hero_table
        return delete_row_by_id(*args, table_name=table_name, **kwargs)

    def register(self, *args, **kwargs) -> bool:
        return insert_user(*args, table_name=self._users_table, **kwargs)

    def login(self, *args, **kwargs) -> tuple[int, bytes] | None:
        return select_user(*args, table_name=self._users_table, **kwargs)


#
# Спосіб збереження в файл втратив свою актуальність
#
# class FileSaver(ABC):
#     """'Відкритий простір' для збереження/завантаження користувача та героїв"""
#
#     @abstractmethod
#     def save(self, *args, hero: Hero, **kwargs) -> None:
#         """Зберігаємо героя у 'відкритий простір'"""
#         pass
#
#     @abstractmethod
#     def load(self, *args, **kwargs) -> Hero:
#         """Завантажуємо героя з 'відкритого простору'"""
#         pass
#
# class JSONSaver(FileSaver):
#     """Збереження в JSON"""
#
#     def __init__(self):
#         self._path = JSON_SAVES_PATH
#
#     def save(self, *args, hero: Hero, **kwargs) -> None:
#         os.makedirs(os.path.dirname(self._path), exist_ok=True)
#         json_hero_saver(*args, hero=hero, path=self._path, **kwargs)
#
#     def load(self, *args, **kwargs) -> Hero:
#         return json_hero_loader(*args, path=self._path, **kwargs)
#
#
# class XMLSaver(FileSaver):
#     """Збереження в XML"""
#
#     def __init__(self):
#         self._path = XML_SAVES_PATH
#
#     def save(self, *args, hero: Hero, **kwargs) -> None:
#         os.makedirs(os.path.dirname(self._path), exist_ok=True)
#         xml_hero_saver(*args, hero=hero, path=self._path, **kwargs)
#
#     def load(self, *args, **kwargs) -> Hero:
#         return xml_hero_loader(*args, path=self._path, **kwargs)
