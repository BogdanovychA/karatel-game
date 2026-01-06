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


START_BOARD = [Emoji.EMPTY.value] * 16

WIN_POSITIONS = [
    # Горизонтальні лінії
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 10, 11],
    [12, 13, 14, 15],
    # Вертикальні лінії
    [0, 4, 8, 12],
    [1, 5, 9, 13],
    [2, 6, 10, 14],
    [3, 7, 11, 15],
    # Діагоналі
    [0, 5, 10, 15],
    [3, 6, 9, 12],
]


def check_winner(board: list[str]) -> str | None:
    """Перевірка переможця"""

    for combo in WIN_POSITIONS:
        a, b, c, d = combo
        if (
            board[a] == board[b] == board[c] == board[d]
            and board[a] != Emoji.EMPTY.value
        ):
            return board[a]
    if Emoji.EMPTY.value not in board:
        return TTT.DRAW.value
    return None


def evaluate_position(board: list[str], max_player: str, min_player: str) -> int:
    """Евристична оцінка позиції"""
    score = 0

    for combo in WIN_POSITIONS:
        max_count = sum(1 for i in combo if board[i] == max_player)
        min_count = sum(1 for i in combo if board[i] == min_player)
        empty_count = sum(1 for i in combo if board[i] == Emoji.EMPTY.value)

        # Якщо лінія не заблокована
        if max_count > 0 and min_count == 0:
            score += max_count**2  # 1, 4, 9, 16
        elif min_count > 0 and max_count == 0:
            score -= min_count**2

    return score


def minimax(
    board: list[str],
    depth: int,
    max_depth: int,
    is_max_turn: bool,
    max_player_symbol: str,
    min_player_symbol: str,
    alpha: float = -math.inf,
    beta: float = math.inf,
) -> int:
    """Побудова дерева ходів"""

    if depth >= max_depth:
        return evaluate_position(board, max_player_symbol, min_player_symbol)

    winner = check_winner(board)

    if winner == max_player_symbol:
        return 100 - depth
    if winner == min_player_symbol:
        return depth - 100
    if winner == TTT.DRAW.value:
        return 0

    if is_max_turn:
        best_score = -math.inf
        for i in range(16):
            if board[i] == Emoji.EMPTY.value:
                board[i] = max_player_symbol
                score = minimax(
                    board,
                    depth + 1,
                    max_depth,
                    False,
                    max_player_symbol,
                    min_player_symbol,
                    alpha,
                    beta,
                )
                board[i] = Emoji.EMPTY.value
                best_score = max(best_score, score)

                alpha = max(alpha, score)
                if beta <= alpha:
                    break

        return best_score
    else:
        best_score = math.inf
        for i in range(16):
            if board[i] == Emoji.EMPTY.value:
                board[i] = min_player_symbol
                score = minimax(
                    board,
                    depth + 1,
                    max_depth,
                    True,
                    max_player_symbol,
                    min_player_symbol,
                    alpha,
                    beta,
                )
                board[i] = Emoji.EMPTY.value
                best_score = min(best_score, score)

                beta = min(beta, score)
                if beta <= alpha:
                    break

        return best_score


def best_move(board: list, max_player_symbol: str, min_player_symbol: str) -> int:
    """Вибір кращого ходу"""
    best_score = -math.inf
    move = None
    alpha = -math.inf
    beta = math.inf

    filled = sum(1 for cell in board if cell != Emoji.EMPTY.value)
    if filled < 4:
        # Початок гри - обмежуємо глибину
        actual_depth = 4
    elif filled < 8:
        actual_depth = 6
    else:
        # Кінець гри - повний перебір
        actual_depth = 16

    for i in range(16):
        if board[i] == Emoji.EMPTY.value:
            board[i] = max_player_symbol
            score = minimax(
                board,
                0,
                actual_depth,
                False,
                max_player_symbol,
                min_player_symbol,
                alpha,
                beta,
            )
            board[i] = Emoji.EMPTY.value
            if score > best_score:
                best_score = score
                move = i

            alpha = max(alpha, score)

    if move is None:
        raise ValueError("Немає доступних ходів на дошці")

    return move


def render_board(output: OutputSpace, board: list) -> None:
    """Рендеринг дошки"""
    text = ""
    for i in range(0, 16, 4):
        text += f"{board[i]} {board[i + 1]} {board[i + 2]} {board[i + 3]}\n"
    output.write(text)


# import time
#
# board = START_BOARD.copy()
#
# start = time.time()
# move = best_move(board, "X", "O")
# elapsed = time.time() - start
#
# print(f"Найкращий хід: {move}")
# print(f"Час обчислення: {elapsed:.4f}s")
