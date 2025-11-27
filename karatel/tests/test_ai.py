# -*- coding: utf-8 -*-

from karatel.ai.abstract import Google, OpenAI
from karatel.ai.google import Gemini

# ai=Gemini()

# print(ai.request(
#     "Зроби рерайт тексту",


ai = Google()
# ai = OpenAI()
text = ai.rewrite("Сонце світить прямо в очі")

print(text)
