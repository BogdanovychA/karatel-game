# -*- coding: utf-8 -*-

import openai

from karatel.ai.openai_config import OPENAI_TOKEN, OPENAI_URL


class ChatGPT:

    def __init__(self) -> None:
        self.client = openai.OpenAI(base_url=OPENAI_URL, api_key=OPENAI_TOKEN)
        self._message_list = []

    def request(self, prompt: str, message: str) -> str:
        """Відправка промпта та тексту, отримання відповіді"""
        self._message_list.clear()
        self._message_list.append({"role": "system", "content": prompt})
        self._message_list.append({"role": "user", "content": message})

        answer = self.client.chat.completions.create(
            model="gpt-4-turbo",  # gpt-4o,  gpt-4-turbo,    gpt-3.5-turbo
            messages=self._message_list,
            max_tokens=2000,
            temperature=0.9,
            n=1,  # Кількість варіантів відповідей
        )
        return answer.choices[0].message.content
