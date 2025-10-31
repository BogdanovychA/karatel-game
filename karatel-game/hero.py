# -*- coding: utf-8 -*-
import random

from items import (
    JUST_HAND,
    UNARMED_STRIKE,
    Item,
    Shield,
    Weapon,
    select_shield,
    select_weapon,
)
from professions import PROFESSIONS, Profession, show_professions
from settings import (
    BASE_SKILL_LEVELS,
    DEBUG,
    EXPERIENCE_FOR_LEVEL,
    FEMALE_NAMES,
    LOG,
    MALE_NAMES,
    MAX_LEVEL,
    MIN_LEVEL,
)
from skills import SKILLS, Skill, SkillTiming
from translations import TRANSLATIONS
from utils import clamp_value, get_modifier, log_print


class Hero:
    def __init__(
        self,
        name: str | None = None,
        profession: Profession | None = None,
        experience: int = 0,
        skills: list[Skill] | None = None,
        right_hand: Weapon | None = None,
        left_hand: Shield | None = None,
        inventory: list[Item] | None = None,
        money: int = 0,
    ) -> None:
        self.name = name or HeroFactory.select_name()

        log_print(f"Персонажа {self.name} створено", end="\n\n", log=DEBUG)

        self.profession = profession or PROFESSIONS["commando"]

        self.level = MIN_LEVEL
        self.experience = 0
        # Ініціалізуємо HP до будь-яких викликів
        self._hp = 0
        self.max_hp = 0

        self.stats = {
            "Strength": 10,
            "Dexterity": 10,
            "Constitution": 10,
            "Intelligence": 10,
            "Charisma": 10,
        }
        # Менеджери
        self.leveling = LevelSystem(self)
        self.equipment = EquipmentManager(self)
        self.display = HeroDisplay(self)
        self.skill_manager = SkillSystem(self)

        self.skills = skills or []

        # Ініціалізація героя
        self.leveling.level_up(add_const=False, log=DEBUG)
        self.leveling.set_penalties()

        # "Докручування" героя до потрібного рівня
        if experience > 0:
            self.leveling.add_experience(experience, log=DEBUG)

        self.inventory = inventory or []

        self.left_hand = JUST_HAND
        self.right_hand = UNARMED_STRIKE

        if left_hand is None:
            self.equipment.equip_shield(select_shield(self.level), log=DEBUG)
        else:
            self.equipment.equip_shield(left_hand, log=DEBUG)

        if right_hand is None:
            self.equipment.equip_weapon(
                select_weapon(self.level, self.profession.main_bonuses[0]), log=DEBUG
            )
        else:
            self.equipment.equip_weapon(right_hand, log=DEBUG)

        self.money: int = money

    def __str__(self) -> str:
        """Повертає текстове представлення героя для print()."""
        return (
            (f"Ім'я: [{self.name}]. " + f"Професія: [{self.profession.name}]")
            if self.alive
            else f"{self.name} - мертвий"
        )

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = clamp_value(value, 0, self.max_hp)

    @property
    def ac(self) -> int:
        return (10 + get_modifier(self.stats["Dexterity"])) + self.left_hand.ac_bonus

    @property
    def attack_modifier(self) -> int:
        return get_modifier(self.stats[self.right_hand.stat])

    @property
    def initiative(self) -> int:
        return get_modifier(self.stats["Dexterity"])

    @property
    def alive(self) -> bool:
        return True if self.hp > 0 else False


class HeroDisplay:
    """Виведення інформації про героя"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def show(self) -> None:
        """Виводить повну інформацію про героя."""
        if self.hero.alive:
            log_print(self.hero, end="\n", log=LOG)
            self.level()
            self.stats()
            self.skills()
            self.inventory()
        else:
            log_print(f"{self.hero.name} - мертвий\n\n", log=LOG)

    def level(self) -> None:
        """Виводить рівень та досвід."""
        log_print(
            f"Рівень: [{self.hero.level}]. " + f"Досвід: [{self.hero.experience}]",
            log=LOG,
        )

    def stats(self) -> None:
        """Виводить характеристики героя."""
        stats_list = [
            f"{TRANSLATIONS.get(stat, stat)}: {self.hero.stats[stat]}"
            for stat in self.hero.stats
        ]
        log_print(f"Характеристики: [{', '.join(stats_list)}]", log=LOG)
        log_print(
            f"Здоров'я: [{self.hero.hp} з {self.hero.max_hp}]. "
            + f"Клас броні: [{self.hero.ac}]. "
            + f"Модифікатор ініціативи: [{self.hero.initiative}]. "
            + f"Модифікатор атаки: [{self.hero.attack_modifier}].",
            log=LOG,
        )

    def skills(self) -> None:
        """Виводить навички героя."""

        if self.hero.skills is None or self.hero.skills == []:
            log_print("Навички: [відсутні]", log=LOG)
        else:
            log_print("Навички: ", log=LOG)
            for item in self.hero.skills:
                log_print(f"* {item}", log=LOG)

    def inventory(self) -> None:
        """Виводить екіпірування та інвентар."""

        log_print("Права рука: ", end="", log=LOG)
        log_print(self.hero.right_hand, log=LOG)
        log_print("Ліва рука: ", end="", log=LOG)
        log_print(self.hero.left_hand, log=LOG)

        if self.hero.inventory is None or self.hero.inventory == []:
            log_print("Інвентар: [пусто]", log=LOG)
        else:
            log_print("Інвентар: ", log=LOG)
            for item in self.hero.inventory:
                log_print(f"* {item}", log=LOG)

        log_print(f"Гроші: {self.hero.money} грн", end="\n\n", log=LOG)


class LevelSystem:
    """Управління рівнями та досвідом"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def set_hp(self) -> None:
        """Встановлює HP на основі Constitution."""
        self.hero.max_hp = 10 + get_modifier(self.hero.stats["Constitution"])
        self.hero._hp = self.hero.max_hp

    def level_up(self, add_const: bool = True, log: bool = True) -> None:
        """Підвищує характеристики при новому рівні."""
        for main_bonuses in self.hero.profession.main_bonuses:
            self.hero.stats[main_bonuses] += 2
        for secondary_bonuses in self.hero.profession.secondary_bonuses:
            self.hero.stats[secondary_bonuses] += 1
        if add_const:
            self.hero.stats["Constitution"] += 1
        self.set_hp()
        self.hero.skill_manager.can_learn_skill(log=log)

    def set_penalties(self) -> None:
        """Встановлює штрафи."""

        for penalty in self.hero.profession.penalties:
            self.hero.stats[penalty] -= 1
        self.set_hp()

    def add_experience(self, amount: int | None = None, log: bool = True) -> None:
        """Перевіряє чи герой отримав новий рівень."""

        if self.hero.level >= MAX_LEVEL:
            self.hero.level = MAX_LEVEL
            log_print(
                f"{self.hero.name} отримав максимальний рівень: "
                + f"{self.hero.level}",
                log=log,
            )
            return

        if amount is not None:
            self.hero.experience += amount
            if self.hero.experience < EXPERIENCE_FOR_LEVEL[-1]:
                log_print(f"{self.hero.name} отримує {amount} досвіду\n", log=log)
            else:
                self.hero.experience = EXPERIENCE_FOR_LEVEL[-1]
                log_print(
                    f"{self.hero.name} Досяг максимального рівня досвіду: "
                    + f"{EXPERIENCE_FOR_LEVEL[-1]}\n",
                    log=log,
                )

        while (
            self.hero.level < MAX_LEVEL
            and self.hero.experience >= EXPERIENCE_FOR_LEVEL[self.hero.level]
        ):
            self.hero.level += 1
            self.level_up(log=log)
            log_print(f"Рівень {self.hero.name} підвищено: {self.hero.level}", log=log)

        if self.hero.level < MAX_LEVEL:
            log_print(
                (
                    f"У {self.hero.name} досвіду: {self.hero.experience}. "
                    f"До наступного рівня: "
                    f"{EXPERIENCE_FOR_LEVEL[self.hero.level] - self.hero.experience}.\n"
                ),
                log=log,
            )


class SkillSystem:
    """Управління скілами"""

    def __init__(self, hero: Hero) -> None:
        self.hero = hero

    def learn_skill(self, skill: Skill, log: bool = True) -> None:
        """Вивчення будь-якої навички"""

        if skill not in self.hero.skills:
            self.hero.skills.append(skill)
            log_print(f"{self.hero.name} отримує навичку {skill.name}\n", log=log)
        else:
            log_print(f"{self.hero.name} вже має навичку {skill.name}\n", log=log)

    def forget_skill(self, skill: Skill, log: bool = True) -> None:
        """Забування будь-якої навички"""

        if skill in self.hero.skills:
            self.hero.skills.remove(skill)
            log_print(f"{self.hero.name} забуває навичку {skill.name}\n", log=log)
        else:
            log_print(f"{self.hero.name} не має навички {skill.name}\n", log=log)

    def can_learn_skill(self, log: bool = True) -> None:
        """Видавання базових навичок в залежності від рівня персонажа
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

    def use_all_skills(self, timing: SkillTiming, log=True) -> None:
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
        if current_hand != default_item:
            self.hero.inventory.append(current_hand)
        if item in self.hero.inventory:
            self.hero.inventory.remove(item)
        setattr(self.hero, hand_name, item)
        log_print(f"Екіпіруємо {item.name}\n", log=log)

    def equip_weapon(self, weapon: Weapon | None = None, log: bool = True) -> None:
        """Екіпірує зброю."""

        if weapon is None:
            weapon = UNARMED_STRIKE

        if isinstance(weapon, Weapon):
            self.equip_item("right_hand", weapon, UNARMED_STRIKE, log=log)
            if weapon.two_handed:
                if self.hero.left_hand != JUST_HAND:
                    self.hero.inventory.append(self.hero.left_hand)
                    log_print(f"{weapon.name} потребує обох рук!", log=log)
                    log_print(
                        f"{self.hero.left_hand.name} автоматично знято",
                        end="\n\n",
                        log=log,
                    )
                self.hero.left_hand = JUST_HAND
        else:
            log_print(f"{weapon.name} не є зброєю", log=log)

    def equip_shield(self, shield: Shield | None = None, log: bool = True) -> None:
        """Екіпірує щит."""

        if shield is None:
            shield = JUST_HAND

        if isinstance(shield, Shield):
            self.equip_item("left_hand", shield, JUST_HAND, log=log)
            if self.hero.right_hand.two_handed:
                self.hero.inventory.append(self.hero.right_hand)
                log_print(f"{self.hero.right_hand.name} потребує обох рук!", log=log)
                log_print(
                    f"{self.hero.right_hand.name} автоматично знято",
                    end="\n\n",
                    log=log,
                )
                self.hero.right_hand = UNARMED_STRIKE
        else:
            log_print(f"{shield.name} не є щитом", log=log)


class HeroFactory:
    """Клас управління героєм"""

    @staticmethod
    def create(log=LOG) -> Hero:
        """Для створення героя гравцем"""
        name = input("Введіть ім'я вашого персонажа: ")
        professions = list(PROFESSIONS.keys())
        menu = {}
        while True:
            log_print("Обери одну з професій:", log=LOG)
            for i in range(len(PROFESSIONS)):
                log_print(i + 1, "-", PROFESSIONS[professions[i]].name, log=LOG)
                menu[str(i + 1)] = professions[i]
            log_print("L - Переглянути опис професій", log=LOG)
            choice = input("Зроби свій вибір: ").upper()
            if choice == "L" or choice == "Д":
                show_professions()
            elif choice in menu:
                profession = PROFESSIONS[menu[choice]]
                break
            else:
                log_print("\nЗробіть правильний вибір!", log=LOG)
        log_print(
            f"Створюємо персонажа з ім'ям {name} та " f"професією {profession.name}",
            log=LOG,
        )
        return Hero(name, profession)

    @staticmethod
    def generate(level: int | None = None, name: str | None = None) -> Hero:
        """Генерація рандомного героя"""
        if name is None:
            name = HeroFactory.select_name()
        profession = random.choice(list(PROFESSIONS.values()))
        if level is None:
            experience = random.choice(EXPERIENCE_FOR_LEVEL)
        else:
            level = clamp_value(level, MIN_LEVEL, MAX_LEVEL)
            experience = EXPERIENCE_FOR_LEVEL[level - 1]
        return Hero(name, profession, experience)

    @staticmethod
    def select_name(sex: str | None = None) -> str:
        """Допоміжна фун-ія для вибору імені героя при генерації"""
        if sex is None:
            return random.choice(MALE_NAMES + FEMALE_NAMES)
        elif sex == "female":
            return random.choice(FEMALE_NAMES)
        else:
            return random.choice(MALE_NAMES)
