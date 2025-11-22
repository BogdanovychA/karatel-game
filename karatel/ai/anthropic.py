# -*- coding: utf-8 -*-

import anthropic

from karatel.ai.config import ANTHROPIC_TOKEN


class Claude:

    def __init__(self) -> None:
        self.client = anthropic.Anthropic(api_key=ANTHROPIC_TOKEN)
        self.aclient = anthropic.AsyncAnthropic(api_key=ANTHROPIC_TOKEN)

    def request(self, prompt: str, message: str) -> str:
        """Відправка промпта та тексту, отримання відповіді"""

        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            # claude-sonnet-4-5-20250929, claude-opus-4-20250812,
            # claude-haiku-4-5-20251001, claude-sonnet-4-20250514
            max_tokens=3000,
            system=prompt,
            messages=[{"role": "user", "content": message}],
        )

        return response.content[0].text.strip()

    async def request_async(self, prompt: str, message: str) -> str:
        """Відправка промпта та тексту, отримання відповіді"""

        response = await self.aclient.messages.create(
            model="claude-haiku-4-5-20251001",
            # claude-sonnet-4-5-20250929, claude-opus-4-20250812,
            # claude-haiku-4-5-20251001, claude-sonnet-4-20250514
            max_tokens=3000,
            system=prompt,
            messages=[{"role": "user", "content": message}],
        )

        return response.content[0].text.strip()
