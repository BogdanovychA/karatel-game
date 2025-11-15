# -*- coding: utf-8 -*-
from __future__ import annotations

import math
import random
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from karatel.ui.abstract import OutputSpace

from karatel.core.items import (
    ITEMS,
    JUST_HAND,
    SHIELDS,
    UNARMED_STRIKE,
    WEAPONS,
    Item,
    Shield,
    Weapon,
    select_shield,
    select_weapon,
)
from karatel.core.professions import PROFESSIONS, Profession
from karatel.core.skills import SKILLS, Skill, SkillTiming
from karatel.utils.constants import FEMALE_NAMES, MALE_NAMES, TRANSLATIONS
from karatel.utils.settings import (
    BASE_SKILL_LEVELS,
    DEBUG,
    EXPERIENCE_FOR_LEVEL,
    LOG,
    MAX_LEVEL,
    MIN_LEVEL,
)
from karatel.utils.utils import clamp_value, get_modifier, obj_finder, sanitize_word


class Hero:
    """Клас героя"""

    def __init__(
        self,
        output: OutputSpace,
        name: str,
        profession: Profession,
        experience: int = 0,
    ) -> None:
        self.name = sanitize_word(name)
        self.profession = profession
        self._level = MIN_LEVEL
        self._experience = 0
        # Ініціалізуємо HP до будь-яких викликів
        self._hp = 1  # тимчасове значення
        self.max_hp = 1  # тимчасове значення

        self._lives = 1

        self._money = 0

        self.stats = {
            "Strength": 10,
            "Dexterity": 10,
            "Constitution": 10,
            "Intelligence": 10,
            "Charisma": 10,
        }
        # Менеджери
        self.output = output
        self.leveling = LevelSystem(self)
        self.equipment = EquipmentManager(self)
        self.display = HeroDisplay(self)
        self.skill_manager = SkillSystem(self)

        self.skills = []

        # Ініціалізація героя
        self.leveling.level_up(add_constitution=False, log=DEBUG)
        self.leveling.set_penalties()

        # "Докручування" героя до потрібного рівня
        if experience > 0:
            self.leveling.add_experience(experience, log=DEBUG)

        self.inventory = []

        self.left_hand = JUST_HAND
        self.right_hand = UNARMED_STRIKE

        self.output.write(f"Персонажа {self.name} створено", log=DEBUG)

    def __str__(self) -> str:
        """Повертає текстове представлення героя для print()."""

        if self.alive:
            return f"Ім'я: [{self.name}]. Професія: [{self.profession.name}]."
        elif self.lives > 0:
            return f"{self.name} - мертвий. Залишилося життів: {self.lives}"
        else:
            return f"{self.name} помер остаточно."

    @property
    def hp(self) -> int:
        """Повертає кількість здоров'я"""

        if self.lives > 0:
            return self._hp
        else:
            return 0

    @hp.setter
    def hp(self, value: int) -> None:
        """Сеттер здоров'я"""
        old_hp = self._hp
        self._hp = math.floor(clamp_value(value, 0, self.max_hp))
        if old_hp > 0 and self._hp == 0:  # Тільки якщо щойно помер
            self.lives -= 1

    @property
    def ac(self) -> int:
        """Розраховує та повертає клас броні"""
        return (10 + get_modifier(self.stats["Dexterity"])) + self.left_hand.ac_bonus

    @property
    def attack_modifier(self) -> int:
        """Розраховує та повертає модифікатор атаки"""
        return get_modifier(self.stats[self.right_hand.stat])

    @property
    def initiative(self) -> int:
        """Розраховує та повертає модифікатор ініціативи"""
        return get_modifier(self.stats["Dexterity"])

    @property
    def alive(self) -> bool:
        """Повертає статус чи живий герой"""
        return self.hp > 0

    @property
    def money(self) -> int:
        """Повертає кількість грошей"""
        return self._money

    @money.setter
    def money(self, value: int) -> None:
        """Сеттер грошей"""
        self._money = math.floor(clamp_value(value, 0, None))

    @property
    def experience(self) -> int:
        """Повертає досвід"""
        return self._experience

    @experience.setter
    def experience(self, value: int) -> None:
        """Сеттер досвіду"""
        self._experience = math.floor(clamp_value(value, 0, EXPERIENCE_FOR_LEVEL[-1]))

    @property
    def level(self) -> int:
        """Повертає рівень героя"""
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        """Сеттер рівня героя"""
        self._level = math.floor(clamp_value(value, 0, MAX_LEVEL))

    @property
    def lives(self) -> int:
        """Повертає кількість життів героя"""
        return self._lives

    @lives.setter
    def lives(self, value: int) -> None:
        """Сеттер життів героя"""
        self._lives = math.floor(clamp_value(value, 0, MAX_LEVEL))


class HeroDisplay:
    """Виведення інформації про героя"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def show(self) -> str:
        """Виводить повну інформацію про героя."""
        if self.hero.alive:
            text = [
                str(self.hero),
                self.lives(),
                self.hp(),
                self.level(),
                self.stats(),
                self.ac(),
                self.modifiers(),
                self.skills(),
                self.inventory(),
            ]
            total = "\n".join(str(a) for a in text)
            return total
        else:
            return str(self.hero)

    def level(self) -> str:
        """Виводить рівень та досвід."""
        return (
            f"Рівень: [{self.hero.level}]. "
            + f"Досвід: [{self.hero.experience} з "
            + f"{EXPERIENCE_FOR_LEVEL[clamp_value(self.hero.level, MIN_LEVEL, MAX_LEVEL-1)]}]."
        )

    def hp(self) -> str:
        """Виводить здоров'я героя"""
        return f"Здоров'я: [{self.hero.hp} з {self.hero.max_hp}]."

    def lives(self) -> str:
        """Виводить кількість життів героя"""
        return f"Кількість життів: [{self.hero.lives}]."

    def ac(self) -> str:
        """Виводить клас броні героя"""
        return f"Клас броні: [{self.hero.ac}]."

    def modifiers(self) -> str:
        """Виводить клас броні героя"""
        return (
            f"Модифікатори: [Ініціатива: {self.hero.initiative}, "
            f"Атака: {self.hero.attack_modifier}]."
        )

    def stats(self) -> str:
        """Виводить характеристики героя."""
        stats_list = [
            f"{TRANSLATIONS.get(stat, stat)}: {self.hero.stats[stat]}"
            for stat in self.hero.stats
        ]
        return f"Характеристики: [{', '.join(stats_list)}]."

    def skills(self) -> str:
        """Виводить навички героя."""
        if self.hero.skills is None or self.hero.skills == []:
            text = ["Навички: [відсутні]"]
        else:
            text = ["Навички: "]
            for item in self.hero.skills:
                text.append(f"* {item}")

        total = "\n".join(str(a) for a in text)
        return total

    def inventory(self) -> str:
        """Виводить екіпірування та інвентар."""
        text = [
            f"Права рука (зброя): {str(self.hero.right_hand)}\n",
            f"Ліва рука (щит): {str(self.hero.left_hand)}\n",
        ]
        if self.hero.inventory is None or self.hero.inventory == []:
            text.append("Інвентар: [пусто].\n")
        else:
            text.append("Інвентар: ")
            for item in self.hero.inventory:
                text.append(f"* {item}")
            text.append("\n")
        text.append(f"Гроші: {self.hero.money} грн.")
        total = "\n".join(str(a) for a in text)
        return total


class LevelSystem:
    """Управління рівнями та досвідом"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def set_hp(self) -> None:
        """Встановлює HP на основі Constitution."""
        self.hero.max_hp = 10 + get_modifier(self.hero.stats["Constitution"])
        self.hero._hp = self.hero.max_hp

    def level_up(self, add_constitution: bool = True, log: bool = LOG) -> None:
        """Підвищує характеристики при новому рівні."""
        for main_bonuses in self.hero.profession.main_bonuses:
            self.hero.stats[main_bonuses] += 2
        for secondary_bonuses in self.hero.profession.secondary_bonuses:
            self.hero.stats[secondary_bonuses] += 1
        if add_constitution:
            self.hero.stats["Constitution"] += 1
        self.set_hp()
        self.hero.skill_manager.can_learn_skill(log=log)

    def set_penalties(self) -> None:
        """Встановлює штрафи."""

        for penalty in self.hero.profession.penalties:
            self.hero.stats[penalty] -= 1
        self.set_hp()

    def add_experience(self, amount: int | None = None, log: bool = LOG) -> None:
        """Перевіряє чи отримав герой новий рівень."""

        if not amount:
            return
        self.hero.experience += amount
        self.hero.output.write(f"{self.hero.name} отримує {amount} досвіду", log=log)
        if self.hero.experience == EXPERIENCE_FOR_LEVEL[-1]:
            self.hero.output.write(
                f"{self.hero.name} досяг максимального досвіду: "
                + f"{EXPERIENCE_FOR_LEVEL[-1]}",
                log=log,
            )

        if self.hero.level == MAX_LEVEL:
            self.hero.output.write(
                f"{self.hero.name} досяг максимального рівня: " + f"{self.hero.level}",
                log=log,
            )
            return

        while (
            self.hero.level < MAX_LEVEL
            and self.hero.experience >= EXPERIENCE_FOR_LEVEL[self.hero.level]
        ):
            self.hero.level += 1
            self.level_up(log=log)
            self.hero.output.write(
                f"Рівень {self.hero.name} підвищено: {self.hero.level}", log=log
            )

        if self.hero.level < MAX_LEVEL:
            self.hero.output.write(
                (
                    f"У {self.hero.name} досвіду: {self.hero.experience}. "
                    f"До наступного рівня: "
                    f"{EXPERIENCE_FOR_LEVEL[self.hero.level] - self.hero.experience}."
                ),
                log=log,
            )


class SkillSystem:
    """Управління скілами"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def learn_skill(self, skill: Skill, log: bool = LOG) -> None:
        """Вивчення будь-якої навички"""

        if skill not in self.hero.skills:
            self.hero.skills.append(skill)
            self.hero.output.write(
                f"{self.hero.name} отримує навичку {skill.name}", log=log
            )
        else:
            self.hero.output.write(
                f"{self.hero.name} вже має навичку {skill.name}", log=log
            )

    def forget_skill(self, skill: Skill, log: bool = LOG) -> None:
        """Забування будь-якої навички"""

        if skill in self.hero.skills:
            self.hero.skills.remove(skill)
            self.hero.output.write(
                f"{self.hero.name} забуває навичку {skill.name}", log=log
            )
        else:
            self.hero.output.write(
                f"{self.hero.name} не має навички {skill.name}", log=log
            )

    def can_learn_skill(self, log: bool = LOG) -> None:
        """Видавання базових навичок залежно від рівня персонажа
        Використовується при "докручуванні" до потрібного рівня"""

        match self.hero.level:

            case level if level == BASE_SKILL_LEVELS[0]:
                self.learn_skill(SKILLS["self_heal_small"], log=log)
            case level if level == BASE_SKILL_LEVELS[1]:
                self.forget_skill(SKILLS["self_heal_small"], log=log)
                self.learn_skill(SKILLS["self_heal_medium"], log=log)
            case level if level == BASE_SKILL_LEVELS[2]:
                self.forget_skill(SKILLS["self_heal_medium"], log=log)
                self.learn_skill(SKILLS["self_heal_strong"], log=log)
            case level if level == BASE_SKILL_LEVELS[3]:
                self.forget_skill(SKILLS["self_heal_strong"], log=log)
                self.learn_skill(SKILLS["self_heal_ultimate"], log=log)

    def use_all_skills(self, timing: SkillTiming, log=LOG) -> None:
        """Використати всі вивчені навички, які відповідають
        їх таймінгу застосування"""

        for item in self.hero.skills:
            if timing == item.skill_timing:
                item.use(self.hero, log=log)


class EquipmentManager:
    """Управління екіпіровкою"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def equip_item(
        self,
        hand_name: str,
        item: Weapon | Shield,
        default_item: Weapon | Shield,
        log=True,
    ) -> None:
        """Допоміжна функція для екіпірування предмета.
        Для забезпечення принципів DRY"""

        current_hand = getattr(self.hero, hand_name)
        if item in self.hero.inventory:
            self.hero.inventory.remove(item)
        setattr(self.hero, hand_name, item)
        if current_hand != default_item:
            self.hero.inventory.append(current_hand)
        if item != default_item:
            self.hero.output.write(f"Екіпіруємо {item.name}", log=log)
        else:
            if current_hand != default_item:
                self.hero.output.write(f"{current_hand.name} Знято!", log=log)
            else:
                self.hero.output.write(f"В руках пусто!", log=log)

    def equip_weapon(self, weapon: Weapon | None = None, log: bool = LOG) -> None:
        """Екіпірує зброю."""

        if weapon is None:
            weapon = UNARMED_STRIKE
        if isinstance(weapon, Weapon):
            self.equip_item("right_hand", weapon, UNARMED_STRIKE, log=log)
            if weapon.two_handed:
                if self.hero.left_hand != JUST_HAND:
                    self.hero.inventory.append(self.hero.left_hand)
                    self.hero.output.write(f"{weapon.name} потребує обох рук!", log=log)
                    self.hero.output.write(
                        f"{self.hero.left_hand.name} автоматично знято", log=log
                    )
                self.hero.left_hand = JUST_HAND
        else:
            self.hero.output.write(f"{weapon.name} не є зброєю", log=log)

    def equip_shield(self, shield: Shield | None = None, log: bool = LOG) -> None:
        """Екіпірує щит."""

        if shield is None:
            shield = JUST_HAND

        if isinstance(shield, Shield):
            self.equip_item("left_hand", shield, JUST_HAND, log=log)
            if shield != JUST_HAND:
                if self.hero.right_hand.two_handed:
                    self.hero.inventory.append(self.hero.right_hand)
                    self.hero.output.write(
                        f"{self.hero.right_hand.name} потребує обох рук!", log=log
                    )
                    self.hero.output.write(
                        f"{self.hero.right_hand.name} автоматично знято", log=log
                    )
                    self.hero.right_hand = UNARMED_STRIKE
        else:
            self.hero.output.write(f"{shield.name} не є щитом", log=log)

    def add_item(self, item: Item, log: bool = LOG) -> None:
        """Додавання предметів в інвентар"""

        if isinstance(item, Item):
            if item != UNARMED_STRIKE and item != JUST_HAND:
                self.hero.inventory.append(item)
                self.hero.output.write(f"{self.hero.name} підбирає: {item}", log=log)
            else:
                self.hero.output.write(f"Не можна підібрати {item.name}", log=log)
        else:
            self.hero.output.write(f"{item} не є предметом", log=log)

    def select_item(self, item_class: Type | None = None) -> Item | None:
        """Повертає перший предмет з інвентаря, заданого типу"""
        if self.hero.inventory is not None:
            for item in self.hero.inventory:
                if isinstance(item, item_class):
                    return item
            return None
        else:
            return None


class HeroFactory:
    """Клас управління героєм"""

    @staticmethod
    def generate(
        output: OutputSpace,
        level: int | None = None,
        profession: str | None = None,
        name: str | None = None,
        right_hand: Weapon | None = None,
        left_hand: Shield | None = None,
    ) -> Hero:
        """Генерація рандомного героя, або героя з
        конкретними характеристиками"""

        if name is None:
            name = HeroFactory.select_name()
        if profession is None:
            profession = random.choice(list(PROFESSIONS.values()))
        else:
            profession = PROFESSIONS[profession]
        if level is None:
            experience = random.choice(EXPERIENCE_FOR_LEVEL)
        else:
            level = clamp_value(level, MIN_LEVEL, MAX_LEVEL)
            experience = EXPERIENCE_FOR_LEVEL[level - 1]

        hero = Hero(
            name=name,
            profession=profession,
            experience=experience,
            output=output,
        )

        if left_hand is None:
            hero.equipment.equip_shield(select_shield(hero.level), log=DEBUG)
        else:
            hero.equipment.equip_shield(left_hand, log=DEBUG)

        if right_hand is None:
            hero.equipment.equip_weapon(
                select_weapon(hero.level, hero.profession.main_bonuses[0]), log=DEBUG
            )
        else:
            hero.equipment.equip_weapon(right_hand, log=DEBUG)

        return hero

    @staticmethod
    def dict_to_hero(output: OutputSpace, the_dict: dict) -> Hero:
        """Створення героя передаючи словник.
        Використовується при завантаженнях зі збереження"""

        def _create_list(input_list: list, base: tuple) -> list:
            """Допоміжна функція для забезпечення DRY"""
            the_list = []
            for item in input_list:
                the_list.append(obj_finder(item, base))
            return the_list

        hero = Hero(
            output=output,
            name=the_dict["name"],
            profession=obj_finder(the_dict["profession"], PROFESSIONS),
            experience=int(the_dict["experience"] or "0"),
        )
        hero.lives = int(the_dict["lives"] or "1")
        hero.money = int(the_dict["money"] or "0")
        hero.right_hand = obj_finder(the_dict["right_hand"], WEAPONS)
        hero.left_hand = obj_finder(the_dict["left_hand"], SHIELDS)
        hero.inventory = _create_list(the_dict["inventory"], ITEMS)
        hero.skills = _create_list(the_dict["skills"], SKILLS)

        return hero

    @staticmethod
    def hero_to_dict(hero: Hero) -> dict:
        """Конвертація героя в словник -- для збереження"""
        the_dict: dict = {
            "name": hero.name,
            "profession": hero.profession.name,
            "experience": hero.experience,
            "lives": hero.lives,
            "money": hero.money,
            "left_hand": hero.left_hand.name,
            "right_hand": hero.right_hand.name,
            "skills": [],
            "inventory": [],
        }
        for skill in hero.skills:
            the_dict["skills"].append(skill.name)
        for item in hero.inventory:
            the_dict["inventory"].append(item.name)

        return the_dict

    @staticmethod
    def select_name(sex: str | None = None) -> str:
        """Допоміжна фун-ія для вибору імені героя при генерації"""
        if sex is None:
            return random.choice(MALE_NAMES + FEMALE_NAMES)
        elif sex == "female":
            return random.choice(FEMALE_NAMES)
        else:
            return random.choice(MALE_NAMES)
