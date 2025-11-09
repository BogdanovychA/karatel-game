# -*- coding: utf-8 -*-

LOG = True

DEBUG = False

HERO_LIVES = 3

XP_MULTIPLIER = 50

BASE_SKILL_LEVELS = (1, 6, 12, 18)

MIN_LEVEL = 1

EXPERIENCE_FOR_LEVEL = (
    0,  # 1
    300,  # 2
    900,  # 3
    2700,  # 4
    6500,  # 5
    14000,  # 6
    23000,  # 7
    34000,  # 8
    48000,  # 9
    64000,  # 10
    85000,  # 11
    100000,  # 12
    120000,  # 13
    140000,  # 14
    165000,  # 15
    195000,  # 16
    225000,  # 17
    265000,  # 18
    305000,  # 19
    355000,  # 20
)

MAX_LEVEL = len(EXPERIENCE_FOR_LEVEL)
