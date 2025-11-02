# -*- coding: utf-8 -*-

from .ui import OutputSpace, ui


def get_modifier(stat_value: int) -> int:
    """Для типових DnD-розрахунків бонусів"""
    return (stat_value - 10) // 2


def clamp_value(value, min_value, max_value):
    """Обмеження значення між min та max"""
    return min(max(value, min_value), max_value)


def log_print(*args, output: OutputSpace | None = None, log=True, **kwargs):
    if log:
        out = output if output is not None else ui
        out.write(*args, **kwargs)
