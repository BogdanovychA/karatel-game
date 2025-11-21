# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from karatel.ai.openai import ChatGPT

if TYPE_CHECKING:
    pass


class AIModel(ABC):
    """'Відкритий простір' роботи ШІ"""

    @abstractmethod
    def rewrite(self, text: str) -> str:
        """Рерайт тексту"""
        pass


class OpenAI(AIModel):
    """Робота з ChatGPT"""

    def __init__(self, on: bool | None = None):
        self.model = ChatGPT()
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        prompt = (
            "Перепиши текст в художньому стилі. Залиш числа і зміст незмінними. "
            "Не згадуй дату свого навчання або обмеження знань."
        )
        return self.model.request(prompt, text)
