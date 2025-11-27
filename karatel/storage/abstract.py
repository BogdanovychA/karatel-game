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
    update_user_data,
)
from karatel.utils.settings import HERO_SQL_TABLE, USERS_SQL_TABLE

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.ui.abstract import OutputSpace


class SQLSaver(ABC):
    """'Відкритий простір' для збереження/завантаження користувача та героїв"""

    @abstractmethod
    def list_hero(self, output: OutputSpace, username: str) -> list:
        """Перегляд переліку героїв через 'відкритий простір'"""
        pass

    @abstractmethod
    def save_hero(self, hero: Hero, game_map: list, username: str, log: bool) -> None:
        """Збереження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def load_hero(
        self, output: OutputSpace, username: str, hero_id: int, log: bool
    ) -> Hero:
        """Завантаження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def delete_hero(self, output: OutputSpace, username: str, row_id: int) -> bool:
        """Видалення героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def register_user(
        self, output: OutputSpace, username: str, hashed_password: bytes, log: bool
    ) -> bool:
        """Реєстрація користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def fetch_user(
        self, output: OutputSpace, username: str, log: bool
    ) -> tuple[int, bytes] | None:
        """Вибірка інформації про користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def delete_user(self, output: OutputSpace, username: str, row_id: int) -> bool:
        """Видалення користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def update_password(
        self, output: OutputSpace, user_id: int, hashed_password: bytes, log: bool
    ) -> bool:
        """Оновлення пароля користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def update_username(
        self,
        output: OutputSpace,
        user_id: int,
        new_username: str,
        old_username: str,
        log: bool,
    ) -> bool:
        """Оновлення імені користувача через 'відкритий простір'"""
        pass


class SQLiteSaver(SQLSaver):
    """Робота з SQLite"""

    def __init__(self):
        # self._path = SQLITE_PATH
        self._hero_table = HERO_SQL_TABLE
        self._users_table = USERS_SQL_TABLE

    def _create_table_name(self, username: str) -> str:
        return self._hero_table + "_" + username

    def list_hero(self, output: OutputSpace, username: str) -> list:
        return select_heroes(
            output=output,
            table_name=self._create_table_name(username),
        )

    def save_hero(self, hero: Hero, game_map: list, username: str, log: bool) -> None:
        sqlite_hero_and_map_saver(
            hero=hero,
            game_map=game_map,
            table_name=self._create_table_name(username),
            log=log,
        )

    def load_hero(
        self, output: OutputSpace, username: str, hero_id: int, log: bool
    ) -> Hero:
        return sqlite_hero_and_map_loader(
            output=output,
            table_name=self._create_table_name(username),
            hero_id=hero_id,
            log=log,
        )

    def delete_hero(self, output: OutputSpace, username: str, row_id: int) -> bool:
        return delete_row_by_id(
            output=output,
            table_name=self._create_table_name(username),
            row_id=row_id,
        )

    def register_user(
        self, output: OutputSpace, username: str, hashed_password: bytes, log: bool
    ) -> bool:
        return insert_user(
            output=output,
            username=username,
            hashed_password=hashed_password,
            table_name=self._users_table,
            log=log,
        )

    def fetch_user(
        self, output: OutputSpace, username: str, log: bool
    ) -> tuple[int, bytes] | None:
        return select_user(
            output=output, username=username, table_name=self._users_table, log=log
        )

    def delete_user(self, output: OutputSpace, username: str, row_id: int) -> bool:
        delete_table(output=output, table_name=self._create_table_name(username))
        is_row_deleted = delete_row_by_id(
            output=output, table_name=self._users_table, row_id=row_id
        )
        return is_row_deleted

    def update_password(
        self, output: OutputSpace, user_id: int, hashed_password: bytes, log: bool
    ) -> bool:
        return update_user_data(
            output=output,
            user_id=user_id,
            hashed_password=hashed_password,
            table_name=self._users_table,
            log=log,
        )

    def update_username(
        self,
        output: OutputSpace,
        user_id: int,
        new_username: str,
        old_username: str,
        log: bool,
    ) -> bool:
        return update_user_data(
            output=output,
            user_id=user_id,
            username=new_username,
            old_username_table=self._create_table_name(old_username),
            new_username_table=self._create_table_name(new_username),
            table_name=self._users_table,
            log=log,
        )


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
