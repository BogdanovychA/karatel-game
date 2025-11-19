# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from karatel.storage.sqlite_manager import (
    delete_row_by_id,
    delete_table,
    insert_user,
    select_heroes,
    select_user,
    sqlite_hero_and_map_loader,
    sqlite_hero_and_map_saver,
)
from karatel.utils.settings import HERO_SQL_TABLE, USERS_SQL_TABLE

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.ui.abstract import OutputSpace


class SQLSaver(ABC):
    """'Відкритий простір' для збереження/завантаження користувача та героїв"""

    @abstractmethod
    def list_hero(self, *args, **kwargs) -> list:
        """Перегляд переліку героїв через 'відкритий простір'"""
        pass

    @abstractmethod
    def save_hero(self, *args, hero: Hero, **kwargs) -> None:
        """Збереження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def load_hero(self, *args, **kwargs) -> Hero:
        """Завантаження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def delete_hero(self, *args, **kwargs) -> bool:
        """Видалення героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def register_user(self, *args, **kwargs) -> bool:
        """Реєстрація користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def select_user(self, *args, **kwargs) -> tuple[int, bytes] | None:
        """Авторизація користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def delete_user(self, *args, **kwargs) -> bool:
        """Авторизація користувача через 'відкритий простір'"""
        pass


class SQLiteSaver(SQLSaver):
    """Робота з SQLite"""

    def __init__(self):
        # self._path = SQLITE_PATH
        self._hero_table = HERO_SQL_TABLE
        self._users_table = USERS_SQL_TABLE

    def _create_table_name(self, username: str) -> str:
        return self._hero_table + "_" + username

    def list_hero(self, *args, username: str, **kwargs) -> list:
        return select_heroes(
            *args, table_name=self._create_table_name(username), **kwargs
        )

    def save_hero(self, *args, username: str, **kwargs) -> None:
        sqlite_hero_and_map_saver(
            *args, table_name=self._create_table_name(username), **kwargs
        )

    def load_hero(self, *args, username: str, **kwargs) -> Hero:
        return sqlite_hero_and_map_loader(
            *args, table_name=self._create_table_name(username), **kwargs
        )

    def delete_hero(self, *args, username: str, **kwargs) -> bool:
        return delete_row_by_id(
            *args, table_name=self._create_table_name(username), **kwargs
        )

    def register_user(self, *args, **kwargs) -> bool:
        return insert_user(*args, table_name=self._users_table, **kwargs)

    def select_user(self, *args, **kwargs) -> tuple[int, bytes] | None:
        return select_user(*args, table_name=self._users_table, **kwargs)

    def delete_user(self, output: OutputSpace, username: str, row_id: int) -> bool:
        table_deleted = delete_table(
            output=output, table_name=self._create_table_name(username)
        )
        row_deleted = delete_row_by_id(
            output=output, table_name=self._users_table, row_id=row_id
        )
        return table_deleted and row_deleted


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
