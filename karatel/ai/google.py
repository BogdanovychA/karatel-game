# -*- coding: utf-8 -*-

from google import genai
from google.genai import types

from karatel.ai.config import GOOGLE_TOKEN


class Gemini:

    def __init__(self) -> None:
        self.client = genai.Client(api_key=GOOGLE_TOKEN)

    def request(self, prompt: str, message: str) -> str | None:
        """Відправка промпта та тексту, отримання відповіді"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",  # gemini-2.5-flash, gemini-2.5-pro
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                temperature=0.9,
                # max_output_tokens=3000,
            ),
            contents=message,
        )

        return response.text.strip()
