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

    hero_dict = HeroFactory.hero_to_dict(hero)

    json_map = json.dumps(
        map_to_dict(game_map) if game_map is not None else None, ensure_ascii=False
    )

    data = {
        "hero": hero_dict,
        "map": json_map,
    }

    DB.document(uid).collection(SAVES_COLLECTION).document(hero.name).set(data)


def load_hero(
    output: OutputSpace, uid: str, hero_name: str
) -> tuple[Hero | None, list | None]:

    doc_ref = DB.document(uid).collection(SAVES_COLLECTION).document(hero_name)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()

        hero_dict = data["hero"]
        hero = HeroFactory.dict_to_hero(output, hero_dict)

        json_map = data["map"]
        map_dict = json.loads(json_map)

        game_map = (
            dict_to_map(output=output, the_list=map_dict)
            if map_dict is not None
            else None
        )

        return hero, game_map

    else:
        return None, None


def delete_hero(uid: str, hero_name: str) -> bool:
    doc_ref = DB.document(uid).collection(SAVES_COLLECTION).document(hero_name)
    doc_ref.delete()
    return True
