# -*- coding: utf-8 -*-

import asyncio
from abc import ABC, abstractmethod

from karatel.ai.anthropic import Claude
from karatel.ai.constants import AIName
from karatel.ai.google import Gemini
from karatel.ai.openai import ChatGPT


class AIModel(ABC):
    """'Відкритий простір' роботи ШІ"""

    BASE_REWRITE_PROMPT = (
        "Перепиши текст в художньому стилі всесвіту Dungeons & Dragons, "
        + "але в сучасному сеттінгу. Залиш числа, імена і інший зміст незмінними. "
        + "Не видавай супровідний текст."
    )

    def __init__(self):
        self.rewrite_prompt_openai = (
            self.BASE_REWRITE_PROMPT
            + "Не згадуй дату свого навчання або обмеження знань."
        )
        self.rewrite_prompt_google = (
            self.BASE_REWRITE_PROMPT
            + "Видай лише один варіант рерайту. "
            + "Не використовуй знаки пунктуації для розмітки тексту."
        )
        self.rewrite_prompt_model_anthropic = (
            self.BASE_REWRITE_PROMPT
            + "Не використовуй знаки пунктуації для розмітки тексту."
            + "Не роби забагато пропусків між строками. Компонуй речення у абзаци."
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
        self.name = AIName.OPENAI.value  # Використовується в зовнішній логіці

    def rewrite(self, text: str) -> str:
        return asyncio.run(self.model.request(self.rewrite_prompt_openai, text))


class Google(AIModel):
    """Робота з Gemini"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model = Gemini()
        self.name = AIName.GOOGLE.value  # Використовується в зовнішній логіці

        # Створюємо та зберігаємо loop -- реалізовано такий варіант
        # а не з asyncio.run() через помилки при роботі з Gemini
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def rewrite(self, text: str) -> str:
        return self.loop.run_until_complete(
            self.model.request(self.rewrite_prompt_google, text)
        )

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


class Anthropic(AIModel):
    """Робота з Claude"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model = Claude()
        self.name = AIName.ANTHROPIC.value  # Використовується в зовнішній логіці

    def rewrite(self, text: str) -> str:
        return asyncio.run(
            self.model.request(self.rewrite_prompt_model_anthropic, text)
        )


class MasterAI(AIModel):
    """Асинхронна робота з API ШІ"""

    def __init__(self, on: bool | None = None):
        super().__init__()
        self.model_openai = ChatGPT()
        self.model_anthropic = Claude()
        self.model_google = Gemini()
        self.name = AIName.MASTERAI.value  # Використовується в зовнішній логіці

        # Створюємо та зберігаємо loop -- реалізовано такий варіант
        # а не з asyncio.run() через помилки при роботі з Gemini
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def rewrite(self, text: str) -> str:
        async def _main() -> str:
            task_openai = self.model_openai.request(self.rewrite_prompt_openai, text)
            task_google = self.model_google.request(self.rewrite_prompt_google, text)
            task_claude = self.model_anthropic.request(
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


if __name__ == "__main__":
    master = MasterAI()
    try:
        result = master.rewrite("Привіт, гравець в цю чудову гру!")
        print(result)
    finally:
        master.close()
