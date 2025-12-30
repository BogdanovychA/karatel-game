# -*- coding: utf-8 -*-

import time

from google import genai
from google.genai import types

from karatel.ai.config import GOOGLE_TOKEN  # , GOOGLE_URL, GOOGLE_API_VERSION,

IMAGE_MODEL = "gemini-2.5-flash-image"
VIDEO_MODEL = "veo-3.0-fast-generate-001"

# Налаштування безпеки
#
# types.HarmCategory.HARM_CATEGORY_HARASSMENT           Домагання
# types.HarmCategory.HARM_CATEGORY_HATE_SPEECH          Мова ненависті
# types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT    Сексуальний контент
# types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT    Небезпечний контент
#
# .BLOCK_LOW_AND_ABOVE      Найсуворіший
# .BLOCK_MEDIUM_AND_ABOVE   Середній
# .BLOCK_ONLY_HIGH          Тільки високий ризик
# .BLOCK_NONE               Вимкнено фільтри
#
safety_settings = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_NONE,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
        threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    ),
]


class Gemini:

    def __init__(self) -> None:
        self.client = genai.Client(api_key=GOOGLE_TOKEN)
        # self.options = types.HttpOptions(
        #     base_url=GOOGLE_URL, api_version=GOOGLE_API_VERSION
        # )
        # self.client = genai.Client(api_key=GOOGLE_TOKEN, http_options=self.options)
        self.PATH = "./karatel/temp/"

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

    def create_image(self, prompt: str) -> bytes:
        config = types.GenerateContentConfig(safety_settings=safety_settings)
        response = self.client.models.generate_content(
            model=IMAGE_MODEL, contents=prompt, config=config
        )

        if not response.candidates:
            raise RuntimeError("Gemini не зміг створити зображення.")

        candidates = response.candidates[0]

        if candidates.finish_reason and candidates.finish_reason.name == "IMAGE_SAFETY":
            raise RuntimeError("Відхилено фільтрами безпеки.")

        if not candidates.content or not candidates.content.parts:
            raise RuntimeError("Відповідь Gemini не містить зображення.")

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return part.inline_data.data

        raise RuntimeError("Відповідь від ШІ не містить зображення.")

    def create_video(self, prompt: str):
        config = types.GenerateVideosConfig(aspect_ratio="16:9", number_of_videos=1)
        operation = self.client.models.generate_videos(
            model=VIDEO_MODEL, prompt=prompt, config=config
        )

        timeout = 300  # 5 хвилин
        start_time = time.time()

        # Чекаємо завершення генерації
        while not operation.done:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Очікування генерації відео перевищило {timeout} секунд."
                )
            time.sleep(5)
            operation = self.client.operations.get(operation)

        if not getattr(operation, "response", None):
            raise RuntimeError("Відео не згенеровано: порожня відповідь від моделі.")

        if not getattr(operation.response, "generated_videos", None):
            raise RuntimeError("Відео не згенеровано: список порожній.")

        video = operation.response.generated_videos[0]

        # Проміжний результат. Треба допрацювати логіку збереження відео

        return video


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
