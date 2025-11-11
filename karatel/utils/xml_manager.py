import xml.etree.ElementTree as ET

from karatel.core.hero import Hero
from karatel.utils.settings import XML_SAVES_PATH


def xml_hero_writer(hero: Hero) -> None:
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

    with open(XML_SAVES_PATH, "wb") as file:
        tree.write(file, encoding="utf-8", xml_declaration=True)
