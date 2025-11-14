# -*- coding: utf-8 -*-

import streamlit as st

from karatel.core.items import Shield, Weapon
from karatel.logic.map_logic import find_hero, move_hero
from karatel.ui.abstract import JSONHeroSaver, SQLiteHeroSaver, XMLHeroSaver
from karatel.ui.web_constants import BUTTON_WIDTH, GameState
from karatel.utils.constants import Emoji
from karatel.utils.settings import LOG


def back_button() -> None:
    """Кнопка НАЗАД"""

    if st.button("Назад", icon=Emoji.BACK.value, type="secondary", width=BUTTON_WIDTH):
        st.session_state.game_state = None
        st.rerun()


def dungeon_button() -> None:
    """Кнопка підземелля"""

    if st.session_state.hero:
        if st.button(
            "Підземелля", icon=Emoji.DUNG.value, type="secondary", width=BUTTON_WIDTH
        ):
            st.session_state.game_state = GameState.ON_MAP.value
            st.rerun()


def hero_button() -> None:
    """Кнопка екрана героя"""

    if st.button("Герой", icon=Emoji.HERO.value, type="secondary", width=BUTTON_WIDTH):
        st.session_state.game_state = GameState.HERO.value
        st.rerun()


def select_load_button() -> None:
    match st.session_state.gsm.saver:
        case SQLiteHeroSaver():
            load_hero_button()
        case JSONHeroSaver() | XMLHeroSaver():
            load_button()
        case _:
            pass


def load_button() -> None:
    """Кнопка завантаження героя"""
    if st.button(
        "Завантажити", icon=Emoji.MOVE_W.value, type="secondary", width=BUTTON_WIDTH
    ):
        st.session_state.hero = st.session_state.gsm.saver.load(
            output=st.session_state.gsm.output, log=LOG
        )
        if 'game_map' in st.session_state and st.session_state.game_map:
            y, x = find_hero(st.session_state.game_map)
            st.session_state.game_map[y][x].obj = st.session_state.hero
        st.rerun()


def load_hero_button() -> None:
    """Кнопка екрану завантажень героя"""
    if st.button(
        "Відновити", icon=Emoji.MOVE_W.value, type="secondary", width=BUTTON_WIDTH
    ):
        st.session_state.game_state = GameState.LOAD_HERO.value
        st.rerun()


def save_button() -> None:
    """Кнопка збереження героя в XML-файл"""
    if st.button(
        "Зберегти", icon=Emoji.MOVE_S.value, type="secondary", width=BUTTON_WIDTH
    ):
        st.session_state.gsm.saver.save(hero=st.session_state.hero, log=LOG)
        st.rerun()


def navigation() -> None:
    """Блок кнопок навігації"""

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        match st.session_state.game_state:
            case GameState.HERO.value:
                dungeon_button()
            case GameState.ON_MAP.value | GameState.LOAD_HERO.value | None:
                hero_button()
    with col2:
        if (
            'game_map' in st.session_state
            and st.session_state.game_map
            and st.session_state.game_state == GameState.ON_MAP.value
            and st.session_state.gsm.can_generate_map
        ):
            if st.button(
                "Нове підземелля",
                icon=Emoji.DUNG.value,
                type="primary",
                width=BUTTON_WIDTH,
            ):
                st.session_state.game_map = None
                st.session_state.gsm.can_generate_map = False
                st.rerun()
    with col3:
        pass
    with col4:
        if st.session_state.game_state is not None:
            back_button()


def respawn() -> None:
    """Блок кнопок відродження"""

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if not st.session_state.hero.alive:
            if st.session_state.hero.lives > 0:
                if st.button(
                    "Відродити",
                    icon=Emoji.RESP.value,
                    type="secondary",
                    width=BUTTON_WIDTH,
                ):
                    st.session_state.hero.leveling.set_hp()
                    st.rerun()
            else:
                st.text(f"{Emoji.X.value} Ви програли!")
    with col2:
        if st.session_state.hero.alive:
            save_button()
    with col3:
        select_load_button()
    with col4:
        if st.button(
            "Знищити", icon=Emoji.TOMB.value, type="primary", width=BUTTON_WIDTH
        ):
            st.session_state.hero = None
            st.session_state.game_state = GameState.HERO.value
            if 'game_map' in st.session_state and st.session_state.game_map:
                st.session_state.game_map = None
            st.session_state.gsm.output.clear()
            st.rerun()


def equipment() -> None:
    """Блок кнопок керування екіпіруванням"""

    if st.session_state.hero.alive:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button(
                "Екіпірувати зброю",
                icon=Emoji.WEAPON.value,
                type="secondary",
                width=BUTTON_WIDTH,
            ):
                st.session_state.hero.equipment.equip_weapon(
                    st.session_state.hero.equipment.select_item(Weapon)
                )
                st.rerun()
        with col2:
            if st.button(
                "Екіпірувати щит",
                icon=Emoji.SHIELD.value,
                type="secondary",
                width=BUTTON_WIDTH,
            ):
                st.session_state.hero.equipment.equip_shield(
                    st.session_state.hero.equipment.select_item(Shield)
                )
                st.rerun()
        with col3:
            if st.button(
                "Зняти зброю", icon=Emoji.X.value, type="secondary", width=BUTTON_WIDTH
            ):
                st.session_state.hero.equipment.equip_weapon()
                st.rerun()
        with col4:
            if st.button(
                "Зняти щит", icon=Emoji.X.value, type="secondary", width=BUTTON_WIDTH
            ):
                st.session_state.hero.equipment.equip_shield()
                st.rerun()


MOVE_BUTTONS = [
    [
        (Emoji.MOVE_Q.value, "move_q", -1, -1, "Вліво-вгору"),
        (Emoji.MOVE_W.value, "move_w", -1, 0, "Вгору"),
        (Emoji.MOVE_E.value, "move_e", -1, 1, "Вправо-вгору"),
    ],
    [
        (Emoji.MOVE_A.value, "move_a", 0, -1, "Вліво"),
        None,  # Центр
        (Emoji.MOVE_D.value, "move_d", 0, 1, "Вправо"),
    ],
    [
        (Emoji.MOVE_Z.value, "move_z", 1, -1, "Вліво-вниз"),
        (Emoji.MOVE_S.value, "move_s", 1, 0, "Вниз"),
        (Emoji.MOVE_C.value, "move_c", 1, 1, "Вправо-вниз"),
    ],
]


def movement_controls() -> None:
    """Рендерить кнопки керування 3x3"""

    st.html(f"{Emoji.CTRL.value} <b>Керування:</b>")

    for line in MOVE_BUTTONS:

        cols = st.columns(3)
        for index, value in enumerate(line):
            with cols[index]:
                if value is None:
                    pass
                else:
                    text, key, y, x, description = value
                    if st.button(label=text, key=key, help=description):
                        move_hero(
                            st.session_state.gsm,
                            y,
                            x,
                            st.session_state.game_map,
                            log=LOG,
                        )
                        st.rerun()


def legend() -> None:
    st.html(f"{Emoji.LEGEND.value} <b>Легенда:</b>")
    st.html(
        f"{Emoji.HERO.value} — ти (герой) | {Emoji.ENEMY.value} — ворог | "
        + f"{Emoji.EXIT.value} — вихід<br>{Emoji.BOOK.value} — досвід | "
        + f"{Emoji.ITEM.value} — скарб | {Emoji.GOLD.value} — гроші<br>"
        + f"{Emoji.EMPTY.value} — нічого"
    )


def show_log(expanded: bool = False) -> None:
    """Експандер з логом гри"""

    with st.expander(f"{Emoji.LOG.value} Лог подій:", expanded=expanded):
        text = st.session_state.gsm.output.read_buffer()
        if text:
            st.text(text)
        else:
            st.text(f"Подій поки не було...")


def show_hero() -> None:
    """Перегляд характеристик героя"""

    st.html(f"<b>{st.session_state.hero}</b>")
    if st.session_state.hero.alive:
        st.write(st.session_state.hero.display.level())
        col1, col2 = st.columns(2)
        with col1:
            st.write(st.session_state.hero.display.lives())
            st.write(st.session_state.hero.display.hp())
        with col2:
            st.write(st.session_state.hero.display.modifiers())
            st.write(st.session_state.hero.display.ac())
        st.write(st.session_state.hero.display.stats())
        st.write(st.session_state.hero.display.skills())
        st.write(st.session_state.hero.display.inventory())
