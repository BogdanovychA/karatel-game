# -*- coding: utf-8 -*-

import openai

from karatel.ai.openai_config import OPENAI_TOKEN, OPENAI_URL

SYSTEM_PROMPT = (
    "Перепиши текст в художньому стилі. Залиш числа і зміст незмінними. "
    "Не згадуй дату свого навчання або обмеження знань."
)


class ChatGPT:

    def __init__(self):
        self.client = openai.OpenAI(base_url=OPENAI_URL, api_key=OPENAI_TOKEN)
        self._prompt = SYSTEM_PROMPT
        self._message_list = []

    def request(self, message: str) -> str:
        self._message_list.clear()
        self._message_list.append({"role": "system", "content": self._prompt})
        self._message_list.append({"role": "user", "content": message})

        answer = self.client.chat.completions.create(
            model="gpt-4o",  # gpt-4o,  gpt-4-turbo,    gpt-3.5-turbo
            messages=self._message_list,
            max_tokens=1000,
            temperature=0.9,
            n=1,
        )
        return answer.choices[0].message.content


chatgpt = ChatGPT()
