# -*- coding: utf-8 -*-

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from karatel.storage.json_manager import json_hero_loader, json_hero_saver
from karatel.storage.sqlite_manager import (
    delete_row_by_id,
    sqlite_hero_loader,
    sqlite_hero_saver,
)
from karatel.storage.xml_manager import xml_hero_loader, xml_hero_saver
from karatel.utils.settings import HERO_SQL_TABLE, JSON_SAVES_PATH, XML_SAVES_PATH

if TYPE_CHECKING:
    from karatel.core.hero import Hero


class SaveHero(ABC):
    """'Відкритий простір' для збереження/завантаження героя"""

    @abstractmethod
    def save(self, *args, hero: Hero, **kwargs) -> None:
        """Зберігаємо героя у 'відкритий простір'"""
        pass

    @abstractmethod
    def load(self, *args, **kwargs) -> Hero:
        """Завантажуємо героя з 'відкритого простору'"""
        pass


class SQLiteHeroSaver(SaveHero):
    """Збереження в SQLite"""

    def __init__(self):
        # self._path = SQLITE_PATH
        self._hero_table = HERO_SQL_TABLE

    def save(self, *args, hero: Hero, **kwargs) -> None:
        sqlite_hero_saver(*args, hero=hero, table_name=self._hero_table, **kwargs)

    def load(self, *args, **kwargs) -> Hero:
        return sqlite_hero_loader(*args, table_name=self._hero_table, **kwargs)

    def delete(self, *args, **kwargs) -> bool:
        return delete_row_by_id(*args, table_name=self._hero_table, **kwargs)


class JSONHeroSaver(SaveHero):
    """Збереження в JSON"""

    def __init__(self):
        self._path = JSON_SAVES_PATH

    def save(self, *args, hero: Hero, **kwargs) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        json_hero_saver(*args, hero=hero, path=self._path, **kwargs)

    def load(self, *args, **kwargs) -> Hero:
        return json_hero_loader(*args, path=self._path, **kwargs)


class XMLHeroSaver(SaveHero):
    """Збереження в XML"""

    def __init__(self):
        self._path = XML_SAVES_PATH

    def save(self, *args, hero: Hero, **kwargs) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        xml_hero_saver(*args, hero=hero, path=self._path, **kwargs)

    def load(self, *args, **kwargs) -> Hero:
        return xml_hero_loader(*args, path=self._path, **kwargs)
