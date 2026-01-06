# -*- coding: utf-8 -*-

from enum import Enum
from typing import Annotated, Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

import karatel.logic.tic_tac_toe_3x3 as ttt
from karatel.utils.constants import Emoji

Board = Annotated[
    list[Literal["none", "X", "O"]],
    Field(..., min_length=9, max_length=9, description="Дошка з 9 елементів"),
]

Move = Annotated[int, Field(ge=0, le=8, description="Індекс ходу (0-8)")]


class GameSymbol(str, Enum):
    """Варіанти повернення результату гри в хрестики-нолики"""

    X = "X"
    O = "O"
    DRAW = "draw"
    NONE = "none"


class GameResult(BaseModel):
    """Для повернення результату гри в хрестики-нолики"""

    result: GameSymbol


class MoveRequest(BaseModel):
    """Дошка та символ гравця, який максимізує.
    Мінімізатор визначається автоматично"""

    board: Board
    max_player_symbol: Literal["X", "O"]


router = APIRouter()


def normalise_board(board_list: list[str]) -> list[str]:
    """Приведення дошки у формат, прийнятний для функції в іншому модулі"""
    return [
        Emoji.EMPTY.value if cell == GameSymbol.NONE.value else cell
        for cell in board_list
    ]


@router.post("/check", response_model=GameResult)
def check_winner(board: Board) -> GameResult:
    """Перевірка чи є переможець"""

    board_list = normalise_board(board)

    result = ttt.check_winner(board_list)

    if result is None:
        return GameResult(result=GameSymbol.NONE)

    return GameResult(result=GameSymbol(result))


@router.post("/move", response_model=Move)
def best_move(request_data: MoveRequest) -> int:
    """Визначення найкращого ходу для гравця"""

    board_list = normalise_board(request_data.board)

    min_player_symbol = (
        GameSymbol.O.value
        if request_data.max_player_symbol == GameSymbol.X.value
        else GameSymbol.X.value
    )

    move = ttt.best_move(board_list, request_data.max_player_symbol, min_player_symbol)

    return move
