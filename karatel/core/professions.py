# -*- coding: utf-8 -*-
from dataclasses import dataclass

from karatel.ui.abstract import ui
from karatel.utils.settings import LOG
from karatel.utils.translate import TRANSLATIONS


@dataclass
class Profession:
    """Клас професій"""

    name: str
    description: str
    main_bonuses: tuple[str, ...]
    secondary_bonuses: tuple[str, ...]
    penalties: tuple[str, ...]


# 1. Спецпризначенець

PROFESSIONS = {
    "commando": Profession(
        name="Спецпризначенець",
        description="Елітний боєць, натренований діяти швидко, точно і без емоцій. "
        "Здатен витримати найважчі умови та винести побратимів на собі.",
        main_bonuses=("Strength",),
        secondary_bonuses=("Dexterity", "Constitution"),
        penalties=("Intelligence", "Charisma"),
    ),
    # 2. Хакер
    "hacker": Profession(
        name="Хакер",
        description="Майстер коду та хаосу, який зламує системи швидше, ніж ти встигаєш відкрити термінал. "
        "Віртуальна війна — його стихія.",
        main_bonuses=("Intelligence",),
        secondary_bonuses=("Dexterity", "Charisma"),
        penalties=("Strength", "Constitution"),
    ),
    # 3. Інфлюенсер
    "influencer": Profession(
        name="Інфлюенсер",
        description="Володар уваги й лайків. Уміє переконати будь-кого у будь-чому, "
        "навіть якщо не дуже розуміє, про що говорить.",
        main_bonuses=("Charisma",),
        secondary_bonuses=("Dexterity", "Intelligence"),
        penalties=("Strength", "Constitution"),
    ),
    # 4. Трюкач
    "stuntman": Profession(
        name="Трюкач",
        description="Безстрашний шукач адреналіну. Стрибає з дахів, перекочується під колесами й "
        "завжди приземляється на ноги — якщо пощастить.",
        main_bonuses=("Dexterity",),
        secondary_bonuses=("Charisma",),
        penalties=("Intelligence", "Strength"),
    ),
}


def show_professions(
    professions: str | list[str] | None = None, log: bool = LOG
) -> None:
    """Виводить одну або кілька професій. Якщо аргумент відсутній — виводить всі."""

    # Якщо передано одну професію як рядок — обертаємо у список
    if isinstance(professions, str):
        professions = [professions]

    # Якщо None — беремо всі ключі словника
    elif professions is None:
        professions = PROFESSIONS.keys()

    for profession in professions:
        prof = PROFESSIONS[profession]
        ui.write(
            f"{prof.name.upper()}.\n{prof.description}\n"
            + f"Основні бонуси: "
            + f"{', '.join(TRANSLATIONS.get(bonus, bonus) for bonus in prof.main_bonuses)}. "
            + f"Вторинні бонуси: "
            + f"{', '.join(TRANSLATIONS.get(bonus, bonus) for bonus in prof.secondary_bonuses)}. "
            + f"Штрафи: {', '.join(TRANSLATIONS.get(bonus, bonus) for bonus in prof.penalties)}.\n",
            log=log,
        )
