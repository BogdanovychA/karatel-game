# -*- coding: utf-8 -*-
from __future__ import annotations

import math
from enum import Enum
from typing import TYPE_CHECKING

from karatel.utils.constants import Emoji

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace


class TTT(Enum):
    """Enum-клас для службових значень"""

    DRAW = "Нічия"


START_BOARD = [Emoji.EMPTY.value] * 9

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


def check_winner(board: list[str]) -> str | None:
    """Перевірка переможця"""

    for combo in WIN_POSITIONS:
        a, b, c = combo
        if board[a] == board[b] == board[c] and board[a] != Emoji.EMPTY.value:
            return board[a]
    if Emoji.EMPTY.value not in board:
        return TTT.DRAW.value
    return None


def minimax(
    board: list[str],
    is_max_turn: bool,
    max_player_symbol: str,
    min_player_symbol: str,
) -> int:
    """Побудова дерева ходів"""

    winner = check_winner(board)

    if winner == max_player_symbol:
        return 1
    if winner == min_player_symbol:
        return -1
    if winner == TTT.DRAW.value:
        return 0

    if is_max_turn:
        best_score = -math.inf
        for i in range(9):
            if board[i] == Emoji.EMPTY.value:
                board[i] = max_player_symbol
                score = minimax(board, False, max_player_symbol, min_player_symbol)
                board[i] = Emoji.EMPTY.value
                best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for i in range(9):
            if board[i] == Emoji.EMPTY.value:
                board[i] = min_player_symbol
                score = minimax(board, True, max_player_symbol, min_player_symbol)
                board[i] = Emoji.EMPTY.value
                best_score = min(best_score, score)
        return best_score


def best_move(
    board: list, max_player_symbol: str, min_player_symbol: str
) -> int | None:
    """Вибір кращого ходу"""
    best_score = -math.inf
    move = None

    for i in range(9):
        if board[i] == Emoji.EMPTY.value:
            board[i] = max_player_symbol
            score = minimax(board, False, max_player_symbol, min_player_symbol)
            board[i] = Emoji.EMPTY.value
            if score > best_score:
                best_score = score
                move = i

    if move is None:
        raise ValueError("Немає доступних ходів на дошці")

    return move


def render_board(output: OutputSpace, board: list) -> None:
    """Рендеринг дошки"""
    text = ""
    for i in range(0, 9, 3):
        text += f"{board[i]} {board[i + 1]} {board[i + 2]}\n"
    output.write(text)


# def set_cell(board: list, cell: str, position: int) -> list[str]:
#     if position in range(len(board)) and board[position] == Emoji.EMPTY.value:
#         board[position] = cell
#     return board
