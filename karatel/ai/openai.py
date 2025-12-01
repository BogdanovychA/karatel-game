# -*- coding: utf-8 -*-

import openai

from karatel.ai.config import OPENAI_TOKEN, OPENAI_URL


class ChatGPT:

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:

        key = api_key or OPENAI_TOKEN
        url = base_url or OPENAI_URL

        self.client = openai.AsyncOpenAI(base_url=url, api_key=key)

    async def request(self, prompt: str, message: str, model: str | None = None) -> str:
        """Відправка промпта та тексту, отримання відповіді (асинхронно)"""

        mod = model or "gpt-4-turbo"  # gpt-4-turbo, gpt-4o, gpt-4-turbo, gpt-3.5-turbo

        message_list = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message},
        ]
        response = await self.client.chat.completions.create(
            model=mod,
            messages=message_list,
            max_tokens=2000,
            temperature=0.9,
            n=1,
        )
        return response.choices[0].message.content.strip()

    ## Синхронний варіант втратив актуальність
    # def request(self, prompt: str, message: str) -> str:
    #     """Відправка промпта та тексту, отримання відповіді"""
    #     message_list = [
    #         {"role": "system", "content": prompt},
    #         {"role": "user", "content": message},
    #     ]
    #     response = self.client.chat.completions.create(
    #         model="gpt-4-turbo",  # gpt-4o,  gpt-4-turbo,    gpt-3.5-turbo
    #         messages=message_list,
    #         max_tokens=2000,
    #         temperature=0.9,
    #         n=1,  # Кількість варіантів відповідей
    #     )
    #     return response.choices[0].message.content.strip()
