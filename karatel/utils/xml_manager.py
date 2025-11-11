import xml.etree.ElementTree as ET

from karatel.core.game_state_manager import gsm
from karatel.core.hero import Hero
from karatel.core.items import ITEMS, SHIELDS, WEAPONS
from karatel.core.professions import PROFESSIONS
from karatel.core.skills import SKILLS
from karatel.utils.settings import DEBUG, XML_SAVES_PATH
from karatel.utils.utils import obj_finder


def xml_hero_saver(hero: Hero, path: str) -> None:
    root = ET.Element('hero')

    ET.SubElement(root, "name").text = hero.name
    ET.SubElement(root, "profession").text = hero.profession.name
    ET.SubElement(root, "experience").text = str(hero.experience)
    ET.SubElement(root, "lives").text = str(hero.lives)
    ET.SubElement(root, "money").text = str(hero.money)
    # stats_root = ET.SubElement(root, 'stats')
    # for stat_name, stat_value in hero.stats.items():
    #     ET.SubElement(stats_root, stat_name).text = str(stat_value)
    skills_root = ET.SubElement(root, 'skills')
    for index, skill in enumerate(hero.skills):
        ET.SubElement(skills_root, "skill", index=str(index)).text = str(skill.name)

    inventory_root = ET.SubElement(root, 'inventory')
    for index, item in enumerate(hero.inventory):
        ET.SubElement(inventory_root, "item", index=str(index)).text = str(item.name)

    ET.SubElement(root, "left_hand").text = hero.left_hand.name
    ET.SubElement(root, "right_hand").text = hero.right_hand.name

    tree = ET.ElementTree(root)

    with open(path, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)


def xml_hero_loader(path: str) -> Hero | None:

    def create_list(parent_tag: str, child_tag: str, base: tuple) -> list:

        the_list: list = []
        parent_root = root.find(parent_tag)
        if parent_root is not None:
            tags = parent_root.findall(child_tag)
            for tag in tags:
                the_list.append(obj_finder(tag.text, base))

        return the_list

    def find_text(text: str) -> str | None:
        element = root.find(text)
        if element is not None and element.text:
            return element.text
        else:
            return None

    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except FileNotFoundError:
        gsm.ui.write(f"Помилка: файл {XML_SAVES_PATH} не знайдено", log=DEBUG)
        return None
    except Exception as e:
        gsm.ui.write(f"Помилка завантаження XML: {e}", log=DEBUG)
        return None

    name = find_text("name")
    profession = find_text("profession")
    experience = int(find_text("experience") or "0")
    lives = int(find_text("lives") or "0")
    money = int(find_text("money") or "0")
    left_hand = obj_finder(find_text("left_hand"), SHIELDS)
    right_hand = obj_finder(find_text("right_hand"), WEAPONS)
    skills = create_list('skills', 'skill', SKILLS)
    inventory = create_list('inventory', 'item', ITEMS)

    hero = Hero(
        name=name,
        profession=obj_finder(profession, PROFESSIONS),
        experience=experience,
    )
    hero.lives = lives
    hero.money = money
    hero.skills = skills
    hero.inventory = inventory
    hero.right_hand = right_hand
    hero.left_hand = left_hand

    return hero
