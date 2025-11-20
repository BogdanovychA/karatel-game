# -*- coding: utf-8 -*-

from karatel.core.hero import Hero
from karatel.core.skills import SkillTiming
from karatel.utils.dice import Dice
from karatel.utils.settings import LOG, XP_MULTIPLIER


def attack(attacker: Hero, defender: Hero) -> bool:
    """Атака одного героя на іншого. Повертає True якщо захисник загинув."""

    def _apply_damage(att: Hero, defn: Hero, damg: int) -> None:
        """Допоміжна функція для забезпечення принципів DRY"""
        att.output.write(
            f"{att.name} наносить {damg} шкоди за "
            + f"допомогою '{att.right_hand.name}'",
            log=LOG,
        )
        defn.hp -= damg
        att.output.write(
            f"У {defn.name} лишається {defn.hp} з " + f"{defn.max_hp} здоров'я",
            end="\n\n",
            log=LOG,
        )

    attack_chance = Dice.roll(output=attacker.output, dice_string="1d20")

    if attack_chance == 20:
        attacker.output.write(
            f"Ходить {attacker.name}. Шанс атаки: {attack_chance}. Критичний успіх! "
            f"{attacker.name} наносить подвійну шкоду!",
            end="\n\n",
            log=LOG,
        )
        attack_value = Dice.roll(
            output=attacker.output, dice_string=attacker.right_hand.damage
        )
        attack_value += Dice.roll(
            output=attacker.output, dice_string=attacker.right_hand.damage
        )
        _apply_damage(attacker, defender, attack_value)
        return not defender.alive
    elif attack_chance == 1:
        attacker.output.write(
            f"Ходить {attacker.name}. Шанс атаки: {attack_chance}. Критичний провал! "
            + f"{attacker.name} промахується!",
            end="\n\n",
            log=LOG,
        )
        return False
    elif (attack_chance + attacker.attack_modifier) >= defender.ac:
        attacker.output.write(
            f"Ходить {attacker.name}. Шанс атаки: {attack_chance}, модифікатор "
            + f"{attacker.attack_modifier:+d}, це >= {defender.ac}",
            log=LOG,
        )
        attack_value = Dice.roll(
            output=attacker.output, dice_string=attacker.right_hand.damage
        )
        _apply_damage(attacker, defender, attack_value)
        return not defender.alive
    else:
        attacker.output.write(
            f"Ходить {attacker.name}. Шанс атаки: {attack_chance}, модифікатор "
            + f"{attacker.attack_modifier:+d}, це < {defender.ac}",
            log=LOG,
        )
        attacker.output.write(f"{attacker.name} промахується", end="\n\n", log=LOG)
        return False


def fight(hero_a: Hero, hero_b: Hero) -> None:
    """Бій між двома героями до смерті одного з них."""

    def after_fight_actions(comb_x: Hero, comb_y: Hero) -> None:
        """Дії, які виконуються після бою"""
        comb_x.output.write(
            f"{comb_x.name} — перемагає, {comb_y.name} — гине!", end="\n\n", log=LOG
        )
        comb_x.skill_manager.use_all_skills(SkillTiming.POST_BATTLE, log=LOG)
        xp_reward = comb_y.level * XP_MULTIPLIER
        comb_x.leveling.add_experience(xp_reward, log=LOG)

    if hero_a.alive and hero_b.alive:
        comb_a, comb_b = roll_initiative(hero_a, hero_b)
        comb_a.output.write(
            f"Починається бій між {comb_a.name} та {comb_b.name}. "
            + f"{comb_a.name} отримує право першого ходу.",
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
        hero_a.output.write("Мертві не воюють!", end="\n\n", log=LOG)
        hero_a.output.write(hero_a, log=LOG)
        hero_b.output.write(hero_b, log=LOG)


def roll_initiative(comb_a: Hero, comb_b: Hero) -> tuple[Hero, Hero]:
    """Визначає порядок ходів. Повертає пару (перший, другий)."""
    comb_a.output.write(f"Готуємося до бою між {comb_a.name} та {comb_b.name}", log=LOG)

    init_a = Dice.roll(output=comb_a.output, dice_string="1d20")
    total_a = init_a + comb_a.initiative
    comb_a.output.write(
        f"Ініціатива {comb_a.name}: {init_a}, "
        + f"модифікатор {comb_a.initiative:+d} = {total_a}",
        log=LOG,
    )

    init_b = Dice.roll(output=comb_b.output, dice_string="1d20")
    total_b = init_b + comb_b.initiative
    comb_b.output.write(
        f"Ініціатива {comb_b.name}: {init_b}, "
        + f"модифікатор {comb_b.initiative:+d} = {total_b}",
        end="\n\n",
        log=LOG,
    )

    if total_a > total_b:
        return comb_a, comb_b
    elif total_a < total_b:
        return comb_b, comb_a
    else:
        comb_a.output.write(
            "Нічия в ініціативі, визначаємо ще раз...", end="\n\n", log=LOG
        )
        return roll_initiative(comb_a, comb_b)
