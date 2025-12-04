# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import requests

from karatel.auth.firebase import (
    firebase_change_password,
    firebase_delete_user,
    firebase_signin,
    firebase_signup,
)
from karatel.storage import firebase_manager

# from karatel.storage.sqlite_manager import (
#     delete_row_by_id,
#     delete_table,
#     insert_user,
#     select_heroes,
#     select_user,
#     sqlite_hero_and_map_loader,
#     sqlite_hero_and_map_saver,
#     update_user_data,
# )
from karatel.utils.crypt import (  # hash_pass,; is_username_valid,; validate_password,
    is_email_valid,
    is_password_valid,
)

# from karatel.utils.settings import HERO_SQL_TABLE, USERS_SQL_TABLE

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.ui.abstract import OutputSpace


class StorageManager(ABC):
    """'Відкритий простір' для збереження/завантаження користувача та героїв"""

    @abstractmethod
    def list_hero(self, output: OutputSpace, username: str) -> list:
        """Перегляд переліку героїв через 'відкритий простір'"""
        pass

    @abstractmethod
    def save_hero(
        self, hero: Hero, game_map: list | None, username: str, log: bool
    ) -> None:
        """Збереження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def load_hero(
        self, output: OutputSpace, username: str, hero_id: int, log: bool
    ) -> tuple[Hero, list]:
        """Завантаження героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def delete_hero(self, output: OutputSpace, username: str, row_id: int) -> bool:
        """Видалення героя через 'відкритий простір'"""
        pass

    @abstractmethod
    def register_user(
        self, output: OutputSpace, username: str, password: str, log: bool
    ) -> tuple[bool, str | int | None, str | None, str | None, str | None]:
        """Реєстрація користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def validate_user(
        self, output: OutputSpace, username: str, password: str, log: bool
    ) -> tuple[bool, str | int | None, str | None, str | None, str | None]:
        pass

    @abstractmethod
    def delete_user(
        self, output: OutputSpace, username: str, id_token: str, log: bool
    ) -> bool:
        """Видалення користувача через 'відкритий простір'"""
        pass

    @abstractmethod
    def update_password(
        self, output: OutputSpace, user_id: int, password: str, log: bool
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

    @staticmethod
    @abstractmethod
    def check_username(output: OutputSpace, username: str, log: bool) -> bool:
        """Перевірка валідності імені користувача"""
        pass

    @staticmethod
    def check_password(output: OutputSpace, password: str, log: bool) -> bool:
        """Перевірка валідності пароля користувача"""
        pwd = is_password_valid(password)
        if not pwd:
            output.write(
                "Пароль має складатися з мінімум 8 символів латинського алфавіту, "
                + "має містити мінімум одну велику та одну малу літеру і "
                + "обов'язково має мати мінімум одну цифру і один спеціальний символ.",
                log=log,
            )
        return pwd


class FirebaseSaver(StorageManager):
    """Робота з Firebase"""

    def __init__(self):
        pass

    def list_hero(self, output: OutputSpace, username: str) -> list:
        return firebase_manager.fetch_heroes(username)

    def save_hero(
        self, hero: Hero, game_map: list | None, username: str, log: bool
    ) -> None:
        firebase_manager.save_hero(hero=hero, game_map=game_map, uid=username)
        hero.output.write(f"Героя '{hero.name}' збережено", log=log)

    def load_hero(
        self, output: OutputSpace, username: str, hero_name: str, log: bool
    ) -> tuple[Hero, list]:
        hero, game_map = firebase_manager.load_hero(
            output=output, uid=username, hero_name=hero_name
        )
        return hero, game_map

    def delete_hero(self, output: OutputSpace, username: str, hero_name: str) -> bool:
        return firebase_manager.delete_hero(uid=username, hero_name=hero_name)

    def register_user(
        self, output: OutputSpace, username: str, password: str, log: bool
    ) -> tuple[bool, str | None, str | None, str | None, str | None]:
        try:
            result = firebase_signup(email=username, password=password)
            firebase_manager.save_email(result["localId"], result["email"])
            return (
                True,
                result["localId"],
                result["email"],
                result["idToken"],
                result["refreshToken"],
            )
        except requests.HTTPError as e:
            error = e.response.json()
            output.write("Помилка реєстрації:", error["error"]["message"], log=log)
            return False, None, None, None, None

    def validate_user(
        self, output: OutputSpace, username: str, password: str, log: bool
    ) -> tuple[bool, str | None, str | None, str | None, str | None]:
        try:
            result = firebase_signin(email=username, password=password)
            return (
                True,
                result["localId"],
                result["email"],
                result["idToken"],
                result["refreshToken"],
            )
        except requests.HTTPError as e:
            error = e.response.json()
            output.write("Помилка авторизації:", error["error"]["message"], log=log)
            return False, None, None, None, None

    def delete_user(
        self, output: OutputSpace, username: str, id_token: str, log: bool
    ) -> bool:
        try:
            firebase_manager.delete_all_heroes(uid=username)
        except Exception as e:
            output.write("Помилка видалення даних користувача:", str(e), log=log)
            return False

        try:
            firebase_delete_user(id_token=id_token)
            return True
        except requests.HTTPError as e:
            error = e.response.json()
            output.write(
                "Помилка видалення користувача:", error["error"]["message"], log=log
            )
            return False

    def update_password(
        self, output: OutputSpace, id_token: str, password: str, log: bool
    ) -> tuple[bool, str | None, str | None, str | None, str | None]:

        try:
            result = firebase_change_password(id_token=id_token, new_password=password)
            output.write("Пароль успішно змінено", log=log)
            return (
                True,
                result["localId"],
                result["email"],
                result["idToken"],
                result["refreshToken"],
            )
        except requests.HTTPError as e:
            error = e.response.json()
            output.write("Помилка зміни пароля:", error["error"]["message"], log=log)
            return False, None, None, None, None

    def update_username(self, **kwargs):
        """Неможливо змінити ім'я користувача у Firebase Auth"""
        pass

    @staticmethod
    def check_username(output: OutputSpace, username: str, log: bool) -> bool:
        uname = is_email_valid(username)
        if not uname:
            output.write(
                "Введіть коректну email-адресу у форматі: "
                + "ім’я@домен.зона (наприклад: user@example.com)",
                log=log,
            )
        return uname


# # Спосіб збереження в SQLite втратив свою актуальність
#
# class SQLiteSaver(StorageManager):
#     """Робота з SQLite"""
#
#     def __init__(self):
#         # self._path = SQLITE_PATH
#         self._hero_table = HERO_SQL_TABLE
#         self._users_table = USERS_SQL_TABLE
#
#     def _create_table_name(self, username: str) -> str:
#         return self._hero_table + "_" + username
#
#     def list_hero(self, output: OutputSpace, username: str) -> list:
#         return select_heroes(
#             output=output,
#             table_name=self._create_table_name(username),
#         )
#
#     def save_hero(
#         self, hero: Hero, game_map: list | None, username: str, log: bool
#     ) -> None:
#         sqlite_hero_and_map_saver(
#             hero=hero,
#             game_map=game_map,
#             table_name=self._create_table_name(username),
#             log=log,
#         )
#
#     def load_hero(
#         self, output: OutputSpace, username: str, hero_id: int, log: bool
#     ) -> tuple[Hero, list]:
#         return sqlite_hero_and_map_loader(
#             output=output,
#             table_name=self._create_table_name(username),
#             hero_id=hero_id,
#             log=log,
#         )
#
#     def delete_hero(self, output: OutputSpace, username: str, row_id: int) -> bool:
#         return delete_row_by_id(
#             output=output,
#             table_name=self._create_table_name(username),
#             row_id=row_id,
#         )
#
#     def register_user(
#         self, output: OutputSpace, username: str, password: str, log: bool
#     ) -> bool:
#         hashed_password = hash_pass(password)
#         return insert_user(
#             output=output,
#             username=username,
#             hashed_password=hashed_password,
#             table_name=self._users_table,
#             log=log,
#         )
#
#     def fetch_user(
#         self, output: OutputSpace, username: str, log: bool
#     ) -> tuple[int, bytes] | None:
#         return select_user(
#             output=output, username=username, table_name=self._users_table, log=log
#         )
#
#     def delete_user(self, output: OutputSpace, username: str, row_id: int) -> bool:
#         delete_table(output=output, table_name=self._create_table_name(username))
#         is_row_deleted = delete_row_by_id(
#             output=output, table_name=self._users_table, row_id=row_id
#         )
#         return is_row_deleted
#
#     def update_password(
#         self, output: OutputSpace, user_id: int, password: str, log: bool
#     ) -> bool:
#         hashed_password = hash_pass(password)
#         return update_user_data(
#             output=output,
#             user_id=user_id,
#             hashed_password=hashed_password,
#             table_name=self._users_table,
#             log=log,
#         )
#
#     def update_username(
#         self,
#         output: OutputSpace,
#         user_id: int,
#         new_username: str,
#         old_username: str,
#         log: bool,
#     ) -> bool:
#         return update_user_data(
#             output=output,
#             user_id=user_id,
#             username=new_username,
#             old_username_table=self._create_table_name(old_username),
#             new_username_table=self._create_table_name(new_username),
#             table_name=self._users_table,
#             log=log,
#         )
#
#     def validate_user(
#         self, output: OutputSpace, username: str, password: str, log: bool
#     ) -> tuple[int | None, bool]:
#         all_data = select_user(
#             output=output, username=username, table_name=self._users_table, log=False
#         )
#         if all_data is None:
#             return None, False
#         user_id, hashed_password = all_data
#         return user_id, validate_password(password, hashed_password)
#
#     @staticmethod
#     def check_username(output: OutputSpace, username: str, log: bool) -> bool:
#         uname = is_username_valid(username)
#         if not uname:
#             output.write(
#                 "Ім'я користувача має містити мінімум 2 символи, "
#                 + "може мати лише літери латинського алфавіту, "
#                 + "цифри та знак підкреслення.",
#                 log=log,
#             )
#         return uname


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
