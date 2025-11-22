# -*- coding: utf-8 -*-

import asyncio
from abc import ABC, abstractmethod

from karatel.ai.anthropic import Claude
from karatel.ai.google import Gemini
from karatel.ai.openai import ChatGPT


class AIModel(ABC):
    """'Відкритий простір' роботи ШІ"""

    BASE_REWRITE_PROMPT = (
        "Перепиши текст в художньому стилі всесвіту Dungeons & Dragons, "
        "але в сучасному сеттінгу. "
        "Залиш числа, імена і інший зміст незмінними. "
    )

    def __init__(self):
        self.rewrite_prompt_openai = (
            self.BASE_REWRITE_PROMPT
            + "Не згадуй дату свого навчання або обмеження знань."
        )
        self.rewrite_prompt_model_anthropic = self.BASE_REWRITE_PROMPT
        self.rewrite_prompt_google = (
            self.BASE_REWRITE_PROMPT
            + "Видай лише один варіант рерайту і без супровідного тексту."
        )

    @abstractmethod
    def rewrite(self, text: str) -> str:
        """Рерайт тексту"""
        pass


class OpenAI(AIModel):
    """Робота з ChatGPT"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model = ChatGPT()
        self.name = "ChatGPT"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        return self.model.request(self.rewrite_prompt_openai, text)


class Google(AIModel):
    """Робота з Gemini"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model = Gemini()
        self.name = "Gemini"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        return self.model.request(self.rewrite_prompt_google, text)


class Anthropic(AIModel):
    """Робота з Claude"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model = Claude()
        self.name = "Claude"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI

    def rewrite(self, text: str) -> str:
        return self.model.request(self.rewrite_prompt_model_anthropic, text)


class MasterAI(AIModel):
    """Асинхронна робота з API AIs"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model_openai = ChatGPT()
        self.model_anthropic = Claude()
        self.model_google = Gemini()
        self.name = "MasterAI"  # Використовується в зовнішній логіці
        self.on = (
            on or False
        )  # Використовується в зовнішній логіці -- чи застосовувати AI
        # Створюємо та зберігаємо loop
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def rewrite(self, text: str) -> str:
        async def _main() -> str:
            task_openai = self.model_openai.request_async(
                self.rewrite_prompt_openai, text
            )
            task_google = self.model_google.request_async(
                self.rewrite_prompt_google, text
            )
            task_claude = self.model_anthropic.request_async(
                self.rewrite_prompt_model_anthropic, text
            )

            openai, google, anthropic = await asyncio.gather(
                task_openai, task_google, task_claude
            )

            return f"OpenAI:\n{openai}\n\nGoogle:\n{google}\n\nAnthropic:\n{anthropic}"

        return self.loop.run_until_complete(_main())

    def close(self):
        """Примусово закрити луп"""
        if hasattr(self, 'loop') and self.loop and not self.loop.is_closed():
            self.loop.close()

    def __del__(self):
        """Автоматичне закриття лупу при видаленні об'єкта"""
        try:
            self.close()
        except Exception:
            pass
