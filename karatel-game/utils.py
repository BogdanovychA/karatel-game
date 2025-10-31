# -*- coding: utf-8 -*-
import time


def get_modifier(stat_value: int) -> int:
    """Для типових DnD-розрахунків бонусів"""
    return (stat_value - 10) // 2


def clamp_value(value, min_value, max_value):
    """Обмеження значення між min та max"""
    return min(max(value, min_value), max_value)


def log_print(*args, log=True, **kwargs):
    """Для виводу тексту в залежності від log"""
    if log:
        time.sleep(1)
        print(*args, **kwargs)
