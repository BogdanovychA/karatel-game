# -*- coding: utf-8 -*-

from fastapi import APIRouter

import karatel.logic.tic_tac_toe_3x3 as ttt
from karatel.api.schemas import (
    TTTGameBoard,
    TTTGameResult,
    TTTMoveRequest,
    TTTMoveResponse,
    TTTResultEnum,
)
from karatel.utils.constants import Emoji

router = APIRouter()


def normalise_board(board_list: list[str]) -> list[str]:
    return [Emoji.EMPTY.value if cell == " " else cell for cell in board_list]


@router.post("/check", response_model=TTTGameResult)
def check_winner(board: TTTGameBoard):

    board_list = board.cells
    board_list = normalise_board(board_list)

    result = ttt.check_winner(board_list)

    if result is None:
        return TTTGameResult(result=TTTResultEnum.NONE)

    return TTTGameResult(result=TTTResultEnum(result))


@router.post("/move")
def best_move(request_data: TTTMoveRequest):

    board_list = request_data.board.cells
    board_list = normalise_board(board_list)

    result = ttt.best_move(
        board_list, request_data.max_player_symbol, request_data.min_player_symbol
    )

    return TTTMoveResponse(move=result)
