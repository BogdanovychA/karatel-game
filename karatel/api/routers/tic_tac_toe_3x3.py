# -*- coding: utf-8 -*-

from enum import Enum
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field, model_validator

import karatel.logic.tic_tac_toe_3x3 as ttt
from karatel.utils.constants import Emoji


class GameBoard(BaseModel):
    """Схема дошки для хрестиків-ноликів"""

    cells: list[Literal[" ", "X", "0"]] = Field(..., min_length=9, max_length=9)


class ResultEnum(str, Enum):
    """Символи для повернення результату гри в хрестики-нолики"""

    WIN_X = "X"
    WIN_0 = "0"
    DRAW = "draw"
    NONE = "none"


class GameResult(BaseModel):
    """Для повернення результату гри в хрестики-нолики"""

    result: ResultEnum


PlayerSymbol = Literal["X", "0"]


class MoveRequest(BaseModel):
    board: GameBoard
    max_player_symbol: PlayerSymbol
    min_player_symbol: PlayerSymbol

    @model_validator(mode='after')
    def check_symbols_are_different(self):
        if self.max_player_symbol == self.min_player_symbol:
            raise ValueError(
                "max_player_symbol and min_player_symbol must be different"
            )
        return self


class MoveResponse(BaseModel):
    move: int


router = APIRouter()


def normalise_board(board_list: list[str]) -> list[str]:
    return [Emoji.EMPTY.value if cell == " " else cell for cell in board_list]


@router.post("/check", response_model=GameResult)
def check_winner(board: GameBoard):

    board_list = board.cells
    board_list = normalise_board(board_list)

    result = ttt.check_winner(board_list)

    if result is None:
        return GameResult(result=ResultEnum.NONE)

    return GameResult(result=ResultEnum(result))


@router.post("/move")
def best_move(request_data: MoveRequest):

    board_list = request_data.board.cells
    board_list = normalise_board(board_list)

    result = ttt.best_move(
        board_list, request_data.max_player_symbol, request_data.min_player_symbol
    )

    return MoveResponse(move=result)
