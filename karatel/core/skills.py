# -*- coding: utf-8 -*-
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from karatel.utils.dice import Dice

if TYPE_CHECKING:
    from karatel.core.hero import Hero

from karatel.core.game_state_manager import gsm


class SkillTiming(Enum):
    """Enum-клас для зберігання змінних, що
    відповідають за час використання скілів"""

    PRE_BATTLE = "pre_battle"
    IN_BATTLE = "in_battle"
    POST_BATTLE = "post_battle"


def check_skill_timing(timing: SkillTiming) -> str | None:
    """Перевірка що виводити в описі скіла"""

    match timing:
        case SkillTiming.PRE_BATTLE:
            return "перед боєм"
        case SkillTiming.IN_BATTLE:
            return "в бою"
        case SkillTiming.POST_BATTLE:
            return "після бою"


class Skill:
    """Базовий клас для скілів"""

    def __init__(self, name: str, description: str, skill_timing: SkillTiming) -> None:
        self.name = name
        self.description = description
        self.skill_timing = skill_timing


class HealSelfSkill(Skill):
    """Навички самолікування"""

    def __init__(
        self,
        name: str,
        description: str,
        skill_timing: SkillTiming,
        power: int | str,
    ) -> None:
        super().__init__(name, description, skill_timing)
        self.power = power or 1

    def __str__(self) -> str:
        """Повертає текстове представлення героя для print()."""

        skill_timing = check_skill_timing(self.skill_timing)

        return (
            f"{self.name.upper()}. {self.description}. "
            + f"Сила ефекту: {self.power}. "
            + f"Застосовується: {skill_timing}."
        )

    def use(self, hero: Hero, log: bool = True) -> None:
        """Використання скіла"""

        if hero.alive and self in hero.skills:
            power = 0
            match self.power:
                case str():
                    power = Dice.roll(self.power)
                case int():
                    power = self.power
            # Обмеження максимального здоров'я реалізовано через сеттер Hero.hp
            hero.hp += power
            gsm.ui.write(
                f"{hero.name} Відновлює {power} здоров'я за допомогою {self.name}",
                log=log,
            )


def skill_finder(name: str, the_dict: dict) -> Skill | None:
    for skill in the_dict.values():
        if name == skill.name:
            return skill
    return None


# База навичок
SKILLS = {
    "self_heal_small": HealSelfSkill(
        name="Слабке самолікування",
        description="Краще так, ніж ніяк",
        power="1d6",
        skill_timing=SkillTiming.POST_BATTLE,
    ),
    "self_heal_medium": HealSelfSkill(
        name="Середнє самолікування",
        description="Трохи турботи про себе нікому не завадить",
        power="1d6+4",
        skill_timing=SkillTiming.POST_BATTLE,
    ),
    "self_heal_strong": HealSelfSkill(
        name="Сильне самолікування",
        description="Зцілення, гідне польового лікаря",
        power="1d15",
        skill_timing=SkillTiming.POST_BATTLE,
    ),
    "self_heal_ultimate": HealSelfSkill(
        name="Надпотужне самолікування",
        description="Повертаєшся з того світу, ніби з відпустки",
        power="1d15+5",
        skill_timing=SkillTiming.POST_BATTLE,
    ),
}
