# -*- coding: utf-8 -*-

from google import genai
from google.genai import types

from karatel.ai.config import GOOGLE_API_VERSION, GOOGLE_TOKEN, GOOGLE_URL


class Gemini:

    def __init__(self) -> None:
        self.options = types.HttpOptions(
            base_url=GOOGLE_URL, api_version=GOOGLE_API_VERSION
        )
        self.client = genai.Client(api_key=GOOGLE_TOKEN, http_options=self.options)

    async def request(self, prompt: str, message: str) -> str | None:
        """Відправка промпта та тексту, отримання відповіді (асинхронно)"""

        response = await self.client.aio.models.generate_content(
            model="gemini-2.5-flash",  # gemini-2.5-flash, gemini-2.5-pro
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                temperature=0.9,
                # max_output_tokens=3000,
            ),
            contents=message,
        )

        return response.text.strip()

    ## Синхронний варіант втратив актуальність
    # def request(self, prompt: str, message: str) -> str | None:
    #     """Відправка промпта та тексту, отримання відповіді"""
    #
    #     response = self.client.models.generate_content(
    #         model="gemini-2.5-flash",  # gemini-2.5-flash, gemini-2.5-pro
    #         config=types.GenerateContentConfig(
    #             system_instruction=prompt,
    #             temperature=0.9,
    #             # max_output_tokens=3000,
    #         ),
    #         contents=message,
    #     )
    #
    #     return response.text.strip()
