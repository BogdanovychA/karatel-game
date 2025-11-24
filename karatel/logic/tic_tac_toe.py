# -*- coding: utf-8 -*-
from __future__ import annotations

import math
from typing import TYPE_CHECKING

from karatel.utils.constants import Emoji

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace

WIN_POSITIONS = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


def check_winner(the_board: list[str]) -> str | None:
    for combo in WIN_POSITIONS:
        a, b, c = combo
        if (
            the_board[a] == the_board[b] == the_board[c]
            and the_board[a] != Emoji.EMPTY.value
        ):
            return the_board[a]
    if Emoji.EMPTY.value not in the_board:
        return "draw"
    return None


def minimax(
    the_board: list[str],
    maximizing_player: bool,
    max_player_symbol: str,
    min_player_symbol: str,
) -> int:
    winner = check_winner(the_board)

    if winner == max_player_symbol:
        return 1
    if winner == min_player_symbol:
        return -1
    if winner == "draw":
        return 0

    if maximizing_player:
        best_score = -math.inf
        for i in range(9):
            if the_board[i] == Emoji.EMPTY.value:
                the_board[i] = max_player_symbol
                score = minimax(the_board, False, max_player_symbol, min_player_symbol)
                the_board[i] = Emoji.EMPTY.value
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if the_board[i] == Emoji.EMPTY.value:
                the_board[i] = min_player_symbol
                score = minimax(the_board, True, max_player_symbol, min_player_symbol)
                the_board[i] = Emoji.EMPTY.value
                best_score = min(best_score, score)
        return best_score


def best_move(the_board: list, max_player_symbol: str, min_player_symbol: str) -> int:
    best_score = -math.inf
    move = None

    for i in range(9):
        if the_board[i] == Emoji.EMPTY.value:
            the_board[i] = max_player_symbol
            score = minimax(the_board, False, max_player_symbol, min_player_symbol)
            the_board[i] = Emoji.EMPTY.value
            if score > best_score:
                best_score = score
                move = i

    return move


def render_board(output: OutputSpace, the_board: list) -> None:
    """Рендеринг дошки"""
    text = ""
    for i in range(0, 9, 3):
        text += f"{the_board[i]} {the_board[i + 1]} {the_board[i + 2]}\n"
    output.write(text)


START_BOARD = [Emoji.EMPTY.value] * 9
