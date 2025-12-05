# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from karatel.utils.constants import TRANSLATIONS, Sex
from karatel.utils.settings import LOG

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace


@dataclass(frozen=True)
class Profession:
    """Клас професій"""

    name: str  # Назва (чол. рід)
    name_fem: str  # Назва (жін. рід)
    description: str  # Опис (чол. рід)
    description_fem: str  # Опис (жін. рід)
    main_bonuses: tuple[str, ...]
    secondary_bonuses: tuple[str, ...]
    penalties: tuple[str, ...]


PROFESSIONS = {
    # 1. Спецпризначенець / Спецпризначенка
    "commando": Profession(
        name="Спецпризначенець",
        name_fem="Спецпризначенка",
        description="Елітний боєць, натренований діяти швидко, точно і без емоцій. "
        "Здатен витримати найважчі умови та винести побратимів на собі.",
        description_fem="Елітна бійчиня, натренована діяти швидко, точно і без емоцій. "
        "Здатна витримати найважчі умови та винести побратимів на собі.",
        main_bonuses=("Strength",),
        secondary_bonuses=("Dexterity", "Constitution"),
        penalties=("Intelligence", "Charisma"),
    ),
    # 2. Хакер / Хакерка
    "hacker": Profession(
        name="Хакер",
        name_fem="Хакерка",
        description="Майстер коду та хаосу, який зламує системи швидше, ніж ти встигаєш відкрити термінал. "
        "Віртуальна війна — його стихія.",
        description_fem="Майстриня коду та хаосу, яка зламує системи швидше, ніж ти встигаєш відкрити термінал. "
        "Віртуальна війна — її стихія.",
        main_bonuses=("Intelligence",),
        secondary_bonuses=("Dexterity", "Charisma"),
        penalties=("Strength", "Constitution"),
    ),
    # 3. Інфлюенсер / Інфлюенсерка
    "influencer": Profession(
        name="Інфлюенсер",
        name_fem="Інфлюенсерка",
        description="Володар уваги й лайків. Уміє переконати будь-кого у будь-чому, "
        "навіть якщо не дуже розуміє, про що говорить.",
        description_fem="Володарка уваги й лайків. Уміє переконати будь-кого у будь-чому, "
        "навіть якщо не дуже розуміє, про що говорить.",
        main_bonuses=("Charisma",),
        secondary_bonuses=("Dexterity", "Intelligence"),
        penalties=("Strength", "Constitution"),
    ),
    # 4. Трюкач / Трюкачка
    "stuntman": Profession(
        name="Трюкач",
        name_fem="Трюкачка",
        description="Безстрашний шукач адреналіну. Стрибає з дахів, перекочується під колесами й "
        "завжди приземляється на ноги — якщо пощастить.",
        description_fem="Безстрашна шукачка адреналіну. Стрибає з дахів, перекочується під колесами й "
        "завжди приземляється на ноги — якщо пощастить.",
        main_bonuses=("Dexterity",),
        secondary_bonuses=("Charisma",),
        penalties=("Intelligence", "Strength"),
    ),
}


def show_professions(
    output: OutputSpace,
    professions: str | list[str] | None = None,
    sex: Sex | None = Sex.M,
    log: bool = LOG,
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

        if sex.value == Sex.M.value:
            text = f"{prof.name.upper()}.\n{prof.description}\n"
        else:
            text = f"{prof.name_fem.upper()}.\n{prof.description_fem}\n"

        output.write(
            text
            + f"Основні бонуси: "
            + f"{', '.join(TRANSLATIONS.get(bonus, bonus) for bonus in prof.main_bonuses)}. "
            + f"Вторинні бонуси: "
            + f"{', '.join(TRANSLATIONS.get(bonus, bonus) for bonus in prof.secondary_bonuses)}. "
            + f"Штрафи: {', '.join(TRANSLATIONS.get(bonus, bonus) for bonus in prof.penalties)}.\n",
            log=log,
        )
