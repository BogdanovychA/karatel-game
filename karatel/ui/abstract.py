# -*- coding: utf-8 -*-

from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from karatel.utils.json_manager import json_hero_loader, json_hero_saver
from karatel.utils.settings import JSON_SAVES_PATH, XML_SAVES_PATH
from karatel.utils.xml_manager import xml_hero_loader, xml_hero_saver

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


class OutputSpace(ABC):
    """'Відкритий простір' для виводу інформації"""

    @abstractmethod
    def write(self, *args, **kwargs) -> None:
        """Виводимо текст у 'відкритий простір'"""
        pass


class ConsoleOutput(OutputSpace):
    """Вивід в консоль"""

    def write(self, *args, log=True, **kwargs) -> None:
        """Вивід в консоль"""
        if log:
            text = " ".join(str(a) for a in args)
            # time.sleep(0.5)
            print(text, **kwargs)


class BufferedOutput(OutputSpace):
    """Вивід у буфер (для тестів або GUI)"""

    def __init__(self):
        self._buffer: list[str] = []

    def write(self, *args, log=True, **kwargs) -> None:
        """Запис в буфер"""
        if log:
            text = " ".join(str(a) for a in args)
            self._buffer.append(text)

    @property
    def buffer(self) -> list[str]:
        """Отримати весь буфер"""
        return self._buffer

    def clear(self) -> None:
        """Очистити буфер"""
        self._buffer.clear()

    def read_buffer(self) -> str:
        """Читання буфера"""
        text = "\n".join(str(a) for a in self.buffer)
        self.clear()
        return text
