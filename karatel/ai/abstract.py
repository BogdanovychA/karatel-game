# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from karatel.ai.anthropic import Claude
from karatel.ai.google import Gemini
from karatel.ai.openai import ChatGPT


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
        self.name = "ChatGPT"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        prompt = (
            "Перепиши текст в художньому стилі всесвіту Dungeons & Dragons, "
            "але в сучасному сеттінгу. "
            "Залиш числа, імена і інший зміст незмінними. "
            "Не згадуй дату свого навчання або обмеження знань."
        )
        return self.model.request(prompt, text)


class Google(AIModel):
    """Робота з Gemini"""

    def __init__(self, on: bool | None = None):
        self.model = Gemini()
        self.name = "Gemini"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        prompt = (
            "Перепиши текст в художньому стилі всесвіту Dungeons & Dragons, "
            "але в сучасному сеттінгу. "
            "Залиш числа, імена і інший зміст незмінними. "
            "Видай лише один варіант рерайту і без супровідного тексту."
        )
        return self.model.request(prompt, text)


class Anthropic(AIModel):
    """Робота з Claude"""

    def __init__(self, on: bool | None = None):
        self.model = Claude()
        self.name = "Claude"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        prompt = (
            "Перепиши текст в художньому стилі всесвіту Dungeons & Dragons, "
            "але в сучасному сеттінгу. "
            "Залиш числа, імена і інший зміст незмінними. "
        )
        return self.model.request(prompt, text)
