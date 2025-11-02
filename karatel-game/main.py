# -*- coding: utf-8 -*-

from combat import fight
from hero import Hero, HeroFactory
from professions import PROFESSIONS
from skills import SKILLS, SkillTiming
from ui import ui

# hero_a = Hero()
hero_a = HeroFactory.generate(5)
hero_a.skill_manager.learn_skill(SKILLS["self_heal_strong"])
hero_a.skill_manager.learn_skill(SKILLS["self_heal_small"])
print(hero_a.display.show())

# hero_a = HeroFactory.create()
# hero_a.skill_manager.forget_skill(SKILLS["self_heal_small"])
# hero_a.display.show()
# hero_a.hp=1
# hero_a.display.show()
#
# for _ in range (10):
#     hero_a.skill_manager.use_all_skills(SkillTiming.POST_BATTLE)
#
# hero_a.display.show()

# hero_a.hp = 1

# hero_a.display.show()

# hero_a.skill_manager.use_all_skills(SkillTiming.POST_BATTLE)

# hero_b = HeroFactory.generate(5)
# hero_b.skill_manager.forget_skill(SKILLS["self_heal_small"])
# hero_b.display.show()
#
# fight(hero_a, hero_b)
# fight(hero_a, hero_b)

# hero_a.display.show()
# hero_b.display.show()

# print(ui.get_buffer())
