# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from karatel.utils.settings import XML_SAVES_PATH
from karatel.utils.xml_manager import xml_hero_loader, xml_hero_saver


class SaveHero(ABC):
    """'Відкритий простір' для збереження героя"""

    @abstractmethod
    def save(self, *args, **kwargs) -> None:
        """Зберігаємо героя у 'відкритий простір'"""
        pass

    @abstractmethod
    def load(
        self,
        *args,
        **kwargs,
    ):
        """Завантажуємо героя з 'відкритого простору'"""
        pass


class XMLSaver(SaveHero):
    """Збереження в XML"""

    def __init__(self):
        self._path = XML_SAVES_PATH

    def save(self, *args, **kwargs) -> None:
        xml_hero_saver(*args, path=self._path, **kwargs)

    def load(
        self,
        *args,
        **kwargs,
    ):
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
