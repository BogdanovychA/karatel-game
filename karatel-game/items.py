# -*- coding: utf-8 -*-
from settings import MAX_LEVEL, MIN_LEVEL
from translations import TRANSLATIONS
from utils import clamp_value


class Item:
    """Базовий клас для предметів"""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description


class Weapon(Item):
    """Предмет - зброя"""

    def __init__(
        self,
        name: str,
        description: str,
        damage: str,
        stat: str,
        two_handed: bool = False,
    ) -> None:
        super().__init__(name, description)
        self.damage = damage  # наприклад, "1d6"
        self.stat = stat  # "Strength", "Dexterity" тощо
        self.two_handed = two_handed

    def __str__(self) -> str:
        """Повертає текстове представлення героя для print()."""
        two_handed = "Двуручний" if self.two_handed else "Одноручний"

        return (
            f"{self.name.upper()}. {self.description}. "
            + f"Атака: {self.damage}. {two_handed}. Бонус: "
            + f"{TRANSLATIONS.get(self.stat, self.stat)}."
        )


class Shield(Item):
    """Предмет - щит"""

    def __init__(self, name: str, description: str, ac_bonus: int) -> None:
        super().__init__(name, description)
        self.ac_bonus = ac_bonus

    def __str__(self) -> str:
        """Повертає текстове представлення героя для print()."""
        return (
            f"{self.name.upper()}. {self.description}. "
            + f"Бонус захисту: {self.ac_bonus}."
        )


STRENGTH_WEAPONS = (
    Weapon(
        "Кулак",
        "Просто кулак — слабенько, але завжди під рукою",
        "1d3",
        "Strength",
        False,
    ),
    Weapon(
        "Дубинка",
        "Тверда дерев'яна палка — больовий фактор більше, ніж краса",
        "1d4",
        "Strength",
        False,
    ),
    Weapon(
        "Металева труба",
        "Іржава, але важка — додає ваги кожному удару",
        "1d6",
        "Strength",
        False,
    ),
    Weapon(
        "Бита з металевим обертанням",
        "Класика в екшн-фільмах: боляче і драматично",
        "1d8",
        "Strength",
        False,
    ),
    Weapon(
        "Старий лопата-головач",
        "Копати — не гра, а бити — теж не гра",
        "1d8+1",
        "Strength",
        False,
    ),
    Weapon(
        "Гантеля 10 кг",
        "Фітнес-зброя: робиш вигляд, що тренуєшся — і ламаєш опонента",
        "1d10",
        "Strength",
        False,
    ),
    Weapon(
        "Молоток", "Для серйозних ремонтних конфліктів", "1d10+1", "Strength", False
    ),
    Weapon(
        "Мачете", "Гостре, важке — робить свою роботу швидко", "2d6", "Strength", False
    ),
    Weapon(
        "Кувалда 'Батя'",
        "Коли треба повідомити всьому району про свій настрій",
        "2d6+2",
        "Strength",
        True,
    ),
    Weapon(
        "Перфоратор-таран",
        "Двуручний інструмент руйнування — серйозний шкодер",
        "2d6+4",
        "Strength",
        True,
    ),
)

DEXTERITY_WEAPONS = (
    Weapon(
        "Різак для коробок",
        "Маленький, гострий — для точних проблем",
        "1d3",
        "Dexterity",
        False,
    ),
    Weapon(
        "Кишеньковий ніж", "Швидко дістаєш — швидко б’єш", "1d4", "Dexterity", False
    ),
    Weapon("Ключ-важіль", "Інструмент, що служить як зброя", "1d6", "Dexterity", False),
    Weapon(
        "Тактичний ніж", "Офіційний інструмент хитрих рішень", "1d8", "Dexterity", False
    ),
    Weapon(
        "Кобура-кістяк", "Працює краще, коли ти спритний", "1d8+1", "Dexterity", False
    ),
    Weapon(
        "Пістолет тренувальний",
        "Легкий, точний — але не для всіх рук",
        "1d10",
        "Dexterity",
        False,
    ),
    Weapon(
        "Пістолет з глушником", "Тиха й акуратна робота", "1d10+1", "Dexterity", False
    ),
    Weapon(
        "Пістолет + прискорювач",
        "Для тих, хто натискає швидше за думку",
        "2d6",
        "Dexterity",
        False,
    ),
    Weapon(
        "Штурмова пістолетна система",
        "Компактна, але смертоносна у правильних руках",
        "2d6+2",
        "Dexterity",
        True,
    ),
    Weapon(
        "Двухручний арбалет 'Спец'",
        "Хоч і важкий, але вимагає спритності для снаряду",
        "2d6+4",
        "Dexterity",
        True,
    ),
)

INTELLIGENCE_WEAPONS = (
    Weapon(
        "Паяльник",
        "Гострий, гарячий — для точних, болючих дотиків",
        "1d3",
        "Intelligence",
        False,
    ),
    Weapon("Кабель", "Короткий, але з планом дій", "1d4", "Intelligence", False),
    Weapon(
        "Ноутбук",
        "Коли аргументи закінчилися — кидаємо ноут",
        "1d6",
        "Intelligence",
        False,
    ),
    Weapon(
        "Планшет 'Відповідь'",
        "Працює краще у руках хитруна",
        "1d8",
        "Intelligence",
        False,
    ),
    Weapon(
        "Хакерський ключ",
        "Прицільний інструмент для творчої рукопашки",
        "1d8+1",
        "Intelligence",
        False,
    ),
    Weapon("Газовий багнет", "Комбо науки й механіки", "1d10", "Intelligence", False),
    Weapon(
        "Батарейка-ударник",
        "Електронний бонус до болю",
        "1d10+1",
        "Intelligence",
        False,
    ),
    Weapon(
        "Ноутбук з SSD",
        "Коли старий ноут не хоче миритись із життям",
        "2d6",
        "Intelligence",
        False,
    ),
    Weapon(
        "Стаціонарний сервер",
        "Великий і важкий — потрібно знати алгоритм кидка",
        "2d6+2",
        "Intelligence",
        True,
    ),
    Weapon(
        "Модульна електропила",
        "Двуручна і хитра — поєднує інженерний геній і руйнування",
        "2d6+4",
        "Intelligence",
        True,
    ),
)

CHARISMA_WEAPONS = (
    Weapon(
        "Газета 'Смішний заголовок'",
        "Пару слів — і люди дивляться в інший бік",
        "1d3",
        "Charisma",
        False,
    ),
    Weapon(
        "Пляшка ігристого вина",
        "Стильно й ефектно — б’є красиво",
        "1d4",
        "Charisma",
        False,
    ),
    Weapon("Селфі-палка", "Б’є і знімає контент одночасно", "1d6", "Charisma", False),
    Weapon(
        "Мікрофон-караоке",
        "Твій голос як зброя — комусь не пощастить",
        "1d8",
        "Charisma",
        False,
    ),
    Weapon(
        "Брендована парасоля",
        "Виглядає солідно і б'є ще солідніше",
        "1d8+1",
        "Charisma",
        False,
    ),
    Weapon(
        "Фаєр-шоу", "Ефектний виступ з косметичною шкодою", "1d10", "Charisma", False
    ),
    Weapon(
        "Скандальна плашка",
        "Найкраще працює у публічних місцях",
        "1d10+1",
        "Charisma",
        False,
    ),
    Weapon(
        "Мегафон 'Голос народу'", "Говориш — всі відступають", "2d6", "Charisma", False
    ),
    Weapon(
        "Шоу-мікрофон з димом",
        "Ефектно й боляче, якщо влучити",
        "2d6+2",
        "Charisma",
        True,
    ),
    Weapon(
        "Мікрофон-акустичний монстр",
        "Інструмент переконання — або руйнування сцени",
        "2d6+4",
        "Charisma",
        True,
    ),
)

SHIELDS = (
    Shield("Рука", "Просто рука — не вміє блокувати, але хоч щось", 0),
    Shield("Папка для документів", "Крихітний бар’єр між тобою і реальністю", 1),
    Shield("Кришка від каструлі", "Народна класика самооборони на кухні", 2),
    Shield("Сковорідка", "Твердий аргумент у будь-якій суперечці", 3),
    Shield(
        "Металевий піднос", "Кафешна броня, відбиває навіть агресивних офіціантів", 4
    ),
    Shield("Рюкзак туриста", "Не лише для речей, але й для порятунку обличчя", 5),
    Shield("Тактичний щит поліції", "Солідний і ефективний, як сам закон", 6),
    Shield("Дверцята від авто", "Імпровізована броня для тих, хто діє швидко", 7),
    Shield(
        "Сервісна кришка від банкомата",
        "Несподівано міцна річ, як і банківські комісії",
        8,
    ),
    Shield("Сталеві двері під’їзду", "Коли ти — останній бастіон цивілізації", 9),
)


def match_level(level: int = 1) -> int:
    """Підбирає предмет під рівень персонажа в залежності
    від позиції предмета в списку"""

    level = clamp_value(level, MIN_LEVEL, MAX_LEVEL)
    return (level - 1) // 2


def select_weapon(level: int = 1, stat: str = "Strength") -> Weapon:
    """Підбирає зброю залежно від бонусної характеристики зброї
    та бонусного модифікатора персонажа"""

    weapons = None
    match stat:
        case "Charisma":
            weapons = CHARISMA_WEAPONS
        case "Intelligence":
            weapons = INTELLIGENCE_WEAPONS
        case "Dexterity":
            weapons = DEXTERITY_WEAPONS
        case _:
            weapons = STRENGTH_WEAPONS
    index = match_level(level)
    return weapons[index]


def select_shield(level: int = 1) -> Shield:
    """Аналогічно зі зброєю - вибирає відповідний
    щит зі списку наявних щитів. Метчінг лише по рівню героя"""

    index = match_level(level)
    return SHIELDS[index]


# Створюємо дефолтну зброю
UNARMED_STRIKE = STRENGTH_WEAPONS[0]
# Створюємо дефолтний щит
JUST_HAND = SHIELDS[0]
