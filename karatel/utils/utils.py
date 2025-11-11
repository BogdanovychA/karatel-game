# -*- coding: utf-8 -*-

from karatel.core.game_state_manager import gsm
from karatel.ui.abstract import OutputSpace


def get_modifier(stat_value: int) -> int:
    """Для типових DnD-розрахунків бонусів"""

    return (stat_value - 10) // 2


def clamp_value(
    value: int | float, min_value: int | float | None, max_value: int | float | None
) -> int | float:
    """Обмеження значення між min та max.
    Якщо щось обмежувати не треба -- передаємо None"""

    if min_value is not None:
        value = max(value, min_value)
    if max_value is not None:
        value = min(value, max_value)
    return value


def log_print(*args, output: OutputSpace | None = None, log=True, **kwargs):
    """Для запису у 'відкритий простір'. Зараз не використовується"""

    if log:
        out = output if output is not None else gsm.ui
        out.write(*args, **kwargs)


def read_buffer() -> str:
    """Читання буфера"""
    text = "\n".join(str(a) for a in gsm.ui.buffer)
    gsm.ui.clear()
    return text


def obj_finder(name: str, data_container: dict | tuple | list) -> object | None:

    if isinstance(data_container, dict):
        iterable = data_container.values()
    elif isinstance(data_container, (tuple, list)):
        iterable = data_container
    else:
        return None

    for obj in iterable:
        if getattr(obj, "name", None) == name:
            return obj
    return None
