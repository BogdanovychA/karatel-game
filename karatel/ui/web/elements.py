# -*- coding: utf-8 -*-

import streamlit as st

from karatel.core.items import Shield, Weapon
from karatel.logic.map import move_hero
from karatel.ui.web.constants import BUTTON_WIDTH, GameState
from karatel.utils.constants import Emoji
from karatel.utils.settings import LOG


def username_input():
    if st.session_state.gsm.username is not None:
        value = st.session_state.gsm.username
    else:
        value = ""
    return st.text_input(
        "Ім'я користувача",
        icon=Emoji.MAN.value,
        value=value,
    )


def pass_input():
    return st.text_input("Пароль", icon=Emoji.KEY.value, type="password")


def logout_button() -> None:
    """Кнопка виходу з гри"""

    if st.button(
        "Вийти з гри", icon=Emoji.LOGOUT.value, type="primary", width=BUTTON_WIDTH
    ):
        st.session_state.game_state = None
        st.session_state.gsm.username = None
        st.rerun()


def dungeon_button() -> None:
    """Кнопка підземелля"""

    if st.session_state.hero:
        if st.button(
            "Підземелля", icon=Emoji.DUNG.value, type="secondary", width=BUTTON_WIDTH
        ):
            st.session_state.game_state = GameState.MAP.value
            st.rerun()


def hero_button() -> None:
    """Кнопка екрана героя"""

    if st.button("Герой", icon=Emoji.HERO.value, type="secondary", width=BUTTON_WIDTH):
        st.session_state.game_state = GameState.HERO.value
        st.rerun()


# Втратило актуальність
#
# def select_load_button() -> None:
#     match st.session_state.gsm.saver:
#         case SQLiteSaver():
#             load_hero_button()
#         # case JSONHeroSaver() | XMLHeroSaver():
#         #     load_button()
#         case _:
#             pass

# Втратило актуальність
#
# def load_button() -> None:
#     """Кнопка завантаження героя"""
#     if st.button(
#         "Завантажити", icon=Emoji.MOVE_W.value, type="secondary", width=BUTTON_WIDTH
#     ):
#         st.session_state.hero = st.session_state.gsm.saver.load_hero(
#             output=st.session_state.gsm.output, log=LOG
#         )
#         if st.session_state.game_map:
#             y, x = find_hero(st.session_state.game_map)
#             st.session_state.game_map[y][x].obj = st.session_state.hero
#         st.rerun()


def load_hero_button() -> None:
    """Кнопка екрана завантажень героя"""
    if st.button(
        "Завантажити", icon=Emoji.LOAD.value, type="secondary", width=BUTTON_WIDTH
    ):
        st.session_state.game_state = GameState.LOAD_HERO.value
        st.rerun()


def profile_button() -> None:
    """Кнопка екрана профілю користувача"""
    if st.button(
        "Профіль", icon=Emoji.PROFILE.value, type="secondary", width=BUTTON_WIDTH
    ):
        st.session_state.game_state = GameState.PROFILE.value
        st.rerun()


def save_button() -> None:
    """Кнопка збереження героя в XML-файл"""
    if st.button(
        "Зберегти", icon=Emoji.SAVE.value, type="secondary", width=BUTTON_WIDTH
    ):
        st.session_state.gsm.saver.save_hero(
            username=st.session_state.gsm.username,
            hero=st.session_state.hero,
            game_map=st.session_state.game_map,
            log=LOG,
        )
        st.rerun()


def navigation() -> None:
    """Блок кнопок навігації"""

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        match st.session_state.game_state:
            case GameState.HERO.value:
                dungeon_button()
            case (
                GameState.MAP.value
                | GameState.LOAD_HERO.value
                | GameState.PROFILE.value
                | None
            ):
                hero_button()
    with col2:
        if (
            'game_map' in st.session_state
            and st.session_state.game_map
            and st.session_state.game_state == GameState.MAP.value
            and st.session_state.gsm.can_generate_map
        ):
            if st.button(
                "Нова пригода",
                icon=Emoji.DUNG.value,
                type="primary",
                width=(BUTTON_WIDTH * 2),
            ):
                st.session_state.game_map = None
                st.session_state.gsm.can_generate_map = False
                st.rerun()
    with col3:
        pass
    with col4:
        if (
            st.session_state.gsm.username is not None
            and st.session_state.game_state != GameState.PROFILE.value
        ):
            profile_button()
        elif st.session_state.game_state == GameState.PROFILE.value:
            logout_button()


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
        if (
            st.session_state.hero.alive
            and st.session_state.gsm.can_generate_map is False
        ):
            save_button()
    with col3:
        load_hero_button()
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
                "Взяти зброю",
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
                "Взяти щит",
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
    """Створення кнопок керування 3x3"""

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

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.text(f"{Emoji.HERO.value} — ти (герой)")
    with col2:
        st.text(f"{Emoji.ENEMY.value} — ворог")
    with col3:
        st.text(f"{Emoji.EXIT.value} — вихід")
    with col4:
        st.text(f"{Emoji.BOOK.value} — досвід")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        st.text(f"{Emoji.ITEM.value} — скарб")
    with col2:
        st.text(f"{Emoji.GOLD.value} — гроші")
    with col3:
        st.text(f"{Emoji.EMPTY.value} — нічого")
    with col4:
        pass


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
