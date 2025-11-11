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
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except FileNotFoundError:
        gsm.ui.write(f"Помилка: файл {XML_SAVES_PATH} не знайдено", log=DEBUG)
        return None
    except Exception as e:
        gsm.ui.write(f"Error loading XML: {e}", log=DEBUG)
        return None

    name: str = ""
    if root.find('name') is not None:
        name = root.find('name').text

    profession: str = ""
    if root.find('profession') is not None:
        profession = root.find('profession').text

    experience: int = 0
    if root.find('experience') is not None:
        experience = int(root.find('experience').text)

    lives: int = 0
    if root.find('lives') is not None:
        lives = int(root.find('lives').text)

    money: int = 0
    if root.find('money') is not None:
        money = int(root.find('money').text)

    hero_skills = []
    skills_root = root.find('skills')
    if skills_root is not None:
        skills = skills_root.findall('skill')
        for skill in skills:
            hero_skills.append(obj_finder(skill.text, SKILLS))

    hero_inventory = []
    inventory_root = root.find('inventory')
    if inventory_root is not None:
        inventory = inventory_root.findall('item')
        for item in inventory:
            hero_inventory.append(obj_finder(item.text, ITEMS))

    hero_left_hand = None
    if root.find('left_hand') is not None:
        left_hand = root.find('left_hand').text
        hero_left_hand = obj_finder(left_hand, SHIELDS)

    hero_right_hand = None
    if root.find('right_hand') is not None:
        right_hand = root.find('right_hand').text
        hero_right_hand = obj_finder(right_hand, WEAPONS)

    hero = Hero(
        name=name,
        profession=obj_finder(profession, PROFESSIONS),
        experience=experience,
    )

    hero.lives = lives
    hero.money = money
    hero.skills = hero_skills
    hero.inventory = hero_inventory
    hero.right_hand = hero_right_hand
    hero.left_hand = hero_left_hand

    return hero
