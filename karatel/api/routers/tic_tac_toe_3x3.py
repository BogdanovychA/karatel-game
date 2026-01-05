# -*- coding: utf-8 -*-
from unittest import case

from fastapi import APIRouter

import karatel.logic.tic_tac_toe_3x3 as ttt
from karatel.api.schemas import TTTGameBoard, TTTGameResult, TTTResultEnum
from karatel.utils.constants import Emoji

router = APIRouter()


@router.post("/check", response_model=TTTGameResult)
def check_winner(board: TTTGameBoard):

    board_list = board.cells
    board_list = list(Emoji.EMPTY.value if cell == " " else cell for cell in board_list)

    result = ttt.check_winner(board_list)

    if result is None:
        return TTTGameResult(result=TTTResultEnum.NONE)

    match result:
        case TTTResultEnum.WIN_X.value:
            return TTTGameResult(result=TTTResultEnum.WIN_X)
        case TTTResultEnum.WIN_0.value:
            return TTTGameResult(result=TTTResultEnum.WIN_0)
        case ttt.TTT.DRAW.value:
            return TTTGameResult(result=TTTResultEnum.DRAW)
