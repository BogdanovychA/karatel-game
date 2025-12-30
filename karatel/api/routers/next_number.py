# -*- coding: utf-8 -*-

from typing import Annotated

from fastapi import APIRouter, Path, Query

from karatel.logic.next_number import get_sequence
from karatel.utils.constants import Difficulty

LENGTH_MIN = 1
# LENGTH_DEFAULT = 6
LENGTH_MAX = 10
router = APIRouter()


@router.get("/get/{length}")
def get_game(
    length: Annotated[
        int, Path(description="Довжина послідовності", ge=LENGTH_MIN, le=LENGTH_MAX)
    ],
    difficulty: Annotated[
        Difficulty,
        Query(
            description="Рівень складності послідовності, випадкова складність або всі наявні"
        ),
    ] = Difficulty.RANDOM,
    random: Annotated[
        bool,
        Query(
            description="Одна випадкова послідовність з обраного рівня складності або всі наявні на цьому рівні"
        ),
    ] = True,
) -> tuple[tuple[int, ...], str] | tuple[tuple[tuple[int, ...], str], ...]:
    return get_sequence(length, difficulty, random)
