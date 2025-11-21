# -*- coding: utf-8 -*-

import openai

from karatel.ai.config import OPENAI_TOKEN, OPENAI_URL


class ChatGPT:

    def __init__(self) -> None:
        self.client = openai.OpenAI(base_url=OPENAI_URL, api_key=OPENAI_TOKEN)

    def request(self, prompt: str, message: str) -> str:
        """Відправка промпта та тексту, отримання відповіді"""
        message_list = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": message},
        ]
        answer = self.client.chat.completions.create(
            model="gpt-4-turbo",  # gpt-4o,  gpt-4-turbo,    gpt-3.5-turbo
            messages=message_list,
            max_tokens=2000,
            temperature=0.9,
            n=1,  # Кількість варіантів відповідей
        )
        return answer.choices[0].message.content.strip()
