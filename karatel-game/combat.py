# -*- coding: utf-8 -*-
from dice import Dice
from hero import Hero
from settings import LOG, XP_MULTIPLIER
from skills import SkillTiming
from utils import log_print


def attack(attacker: Hero, defender: Hero) -> bool:
    """Атака одного героя на іншого. Повертає True якщо захисник загинув."""

    def apply_damage(att: Hero, defn: Hero, damg: int) -> None:
        """Допоміжна функція для забезпечення принципів DRY"""
        log_print(
            f"{att.name} наносить {damg} шкоди за "
            + f"допомогою {att.right_hand.name}",
            log=LOG,
        )
        defn.hp -= damg
        log_print(
            f"У {defn.name} лишається {defn.hp} з " + f"{defn.max_hp} здоров'я",
            end="\n\n",
            log=LOG,
        )

    attack_chance = Dice.roll("1d20")

    if attack_chance == 20:
        log_print(
            f"Шанс атаки: {attack_chance}. Критичний успіх! "
            f"{attacker.name} наносить подвійну шкоду!",
            end="\n\n",
            log=LOG,
        )
        attack_value = Dice.roll(attacker.right_hand.damage)
        attack_value += Dice.roll(attacker.right_hand.damage)
        apply_damage(attacker, defender, attack_value)
        return not defender.alive
    elif attack_chance == 1:
        log_print(
            f"Шанс атаки: {attack_chance}. Критичний провал! "
            + f"{attacker.name} Промахується!",
            end="\n\n",
            log=LOG,
        )
        return False
    elif (attack_chance + attacker.attack_modifier) >= defender.ac:
        log_print(
            f"Шанс атаки: {attack_chance} плюс модифікатор "
            + f"{attacker.attack_modifier}, це >= {defender.ac}",
            log=LOG,
        )
        attack_value = Dice.roll(attacker.right_hand.damage)
        apply_damage(attacker, defender, attack_value)
        return not defender.alive
    else:
        log_print(
            f"Шанс атаки: {attack_chance} плюс модифікатор "
            + f"{attacker.attack_modifier}, це < {defender.ac}",
            log=LOG,
        )
        log_print(f"{attacker.name} промахується", end="\n\n", log=LOG)
        return False


def fight(hero_a: Hero, hero_b: Hero) -> None:
    """Бій між двома героями до смерті одного з них."""

    def after_fight_actions(comb_x: Hero, comb_y: Hero) -> None:
        """Дії, які виконуються після бою"""
        log_print(
            f"{comb_x.name} — переміг, {comb_y.name} — загинув!", end="\n\n", log=LOG
        )
        comb_x.skill_manager.use_all_skills(SkillTiming.POST_BATTLE, log=LOG)
        xp_reward = comb_y.level * XP_MULTIPLIER
        comb_x.leveling.add_experience(xp_reward, log=LOG)

    if hero_a.alive and hero_b.alive:
        comb_a, comb_b = roll_initiative(hero_a, hero_b)
        log_print(
            f"Починається бій між {comb_a.name} та {comb_b.name}. "
            + f"{comb_a.name} ходить першим.",
            end="\n\n",
            log=LOG,
        )
        while comb_a.hp > 0 and comb_b.hp > 0:
            if attack(comb_a, comb_b):
                after_fight_actions(comb_a, comb_b)
                break
            if attack(comb_b, comb_a):
                after_fight_actions(comb_b, comb_a)
                break
    else:
        log_print("Мертві не воюють!", end="\n\n", log=LOG)
        log_print(hero_a, log=LOG)
        log_print(hero_b, log=LOG)


def roll_initiative(comb_a: Hero, comb_b: Hero) -> tuple[Hero, Hero]:
    """Визначає порядок ходів. Повертає пару (перший, другий)."""
    log_print(f"Готуємося до бою між {comb_a.name} та {comb_b.name}", log=LOG)

    init_a = Dice.roll("1d20")
    total_a = init_a + comb_a.initiative
    log_print(
        f"Ініціатива {comb_a.name}: {init_a} + "
        + f"модифікатор {comb_a.initiative} = {total_a}",
        log=LOG,
    )

    init_b = Dice.roll("1d20")
    total_b = init_b + comb_b.initiative
    log_print(
        f"Ініціатива {comb_b.name}: {init_b} + "
        + f"модифікатор {comb_b.initiative} = {total_b}",
        end="\n\n",
        log=LOG,
    )

    if total_a > total_b:
        return comb_a, comb_b
    elif total_a < total_b:
        return comb_b, comb_a
    else:
        log_print("Нічия в ініціативі, кидаємо ще раз...", end="\n\n", log=LOG)
        return roll_initiative(comb_a, comb_b)
