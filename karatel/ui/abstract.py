# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod


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
