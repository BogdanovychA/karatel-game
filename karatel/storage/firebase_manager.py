# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import firebase_admin
from firebase_admin import credentials, firestore

from karatel.core.hero import HeroFactory
from karatel.core.map import dict_to_map, map_to_dict

if TYPE_CHECKING:
    from karatel.core.hero import Hero
    from karatel.ui.abstract import OutputSpace

cred = credentials.Certificate("./karatel/storage/karatel-game-firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

MAIN_COLLECTION = "karatel_database"
SAVES_COLLECTION = "saves"

DB = db.collection(MAIN_COLLECTION)


def save_hero(hero: Hero, game_map: list | None, uid: str) -> None:
    """Збереження героя та мапи у Firebase Firestore"""

    json_hero = json.dumps(HeroFactory.hero_to_dict(hero))
    json_map = json.dumps(
        map_to_dict(game_map) if game_map is not None else None, ensure_ascii=False
    )

    data = {
        "hero": json_hero,
        "map": json_map,
    }

    DB.document(uid).collection(SAVES_COLLECTION).document(hero.name).set(data)


def select_hero(uid: str, hero_name: str) -> tuple[str | None, str | None]:
    """Вибірка героя та мапи з Firebase Firestore
    повернення в форматі JSON рядків"""

    doc_ref = DB.document(uid).collection(SAVES_COLLECTION).document(hero_name)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()

        json_hero = data["hero"]
        json_map = data["map"]

        return json_hero, json_map

    else:
        return None, None


def load_hero(
    output: OutputSpace, uid: str, hero_name: str
) -> tuple[Hero | None, list | None]:
    """Завантаження героя та мапи з Firebase Firestore"""

    json_hero, json_map = select_hero(uid, hero_name)

    if json_hero is None:
        return None, None

    hero_dict = json.loads(json_hero)
    hero = HeroFactory.dict_to_hero(output, hero_dict)

    map_dict = json.loads(json_map)
    game_map = (
        dict_to_map(output=output, the_list=map_dict) if map_dict is not None else None
    )

    return hero, game_map


def delete_hero(uid: str, hero_name: str) -> bool:
    """Видалення героя з Firebase Firestore"""
    doc_ref = DB.document(uid).collection(SAVES_COLLECTION).document(hero_name)
    doc_ref.delete()
    return True
