from itertools import combinations

import pytest

from karatel.core.hero import HeroFactory
from karatel.core.professions import PROFESSIONS
from karatel.logic.combat import fight
from karatel.ui.abstract import NoneOutput
from karatel.utils.settings import MAX_LEVEL, MIN_LEVEL

output = NoneOutput()

num_tests = 1000
min_ratio = 0.45
max_ratio = 0.55


@pytest.mark.parametrize("level", list(range(MIN_LEVEL, MAX_LEVEL + 1)))
@pytest.mark.parametrize(
    "prof1, prof2", list(combinations(list(PROFESSIONS.keys()), 2))
)
def test_hero_combats(level, prof1, prof2):
    wins1 = 0
    wins2 = 0

    for _ in range(num_tests):
        hero1 = HeroFactory.generate(output, level=level, profession=prof1)
        hero2 = HeroFactory.generate(output, level=level, profession=prof2)
        fight(hero1, hero2)

        if hero1.alive and not hero2.alive:
            wins1 += 1
        elif hero2.alive and not hero1.alive:
            wins2 += 1

    total = wins1 + wins2
    assert total == num_tests

    ratio = wins1 / total
    assert min_ratio <= ratio <= max_ratio
