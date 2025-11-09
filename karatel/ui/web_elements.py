# -*- coding: utf-8 -*-

import streamlit as st

from karatel.core.game_state_manager import gsm
from karatel.core.items import Shield, Weapon
from karatel.ui.web_constants import BUTTON_WIDTH, GameState
from karatel.utils.constants import Emoji
from karatel.utils.utils import read_buffer


def back_button() -> None:
    """Кнопка НАЗАД"""

    if st.button(f"{Emoji.BACK.value} Назад", type="secondary", width=BUTTON_WIDTH):
        st.session_state.game_state = None
        st.rerun()


def dungeon_button() -> None:
    """Кнопка підземелля"""

    if st.session_state.hero:
        if st.button(
            f"{Emoji.DUNG.value} Підземелля", type="secondary", width=BUTTON_WIDTH
        ):
            st.session_state.game_state = GameState.ON_MAP.value
            st.rerun()


def hero_button() -> None:
    """Кнопка екрана героя"""

    if st.button(f"{Emoji.HERO.value} Герой", type="secondary", width=BUTTON_WIDTH):
        st.session_state.game_state = GameState.HERO.value
        st.rerun()


def navigation() -> None:
    """Блок кнопок навігації"""

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        match st.session_state.game_state:
            case GameState.HERO.value:
                dungeon_button()
            case GameState.ON_MAP.value | None:
                hero_button()
    with col2:
        if (
            'game_map' in st.session_state
            and st.session_state.game_map
            and st.session_state.game_state == GameState.ON_MAP.value
            and gsm.can_generate_map
        ):
            if st.button(
                f"{Emoji.DUNG.value} Нове підземелля",
                type="primary",
                width=BUTTON_WIDTH,
            ):
                st.session_state.game_map = None
                gsm.can_generate_map = False
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
                    f"{Emoji.RESP.value} Відродити",
                    type="secondary",
                    width=BUTTON_WIDTH,
                ):
                    st.session_state.hero.leveling.set_hp()
                    st.rerun()
            else:
                st.text(f"{Emoji.X.value} Ви програли!")
    with col2:
        pass
    with col3:
        pass
    with col4:
        if st.button(
            f"{Emoji.X.value} Знищити героя", type="primary", width=BUTTON_WIDTH
        ):
            st.session_state.hero = None
            if 'game_map' in st.session_state and st.session_state.game_map:
                st.session_state.game_map = None
            gsm.ui.clear()
            st.rerun()


def equipment() -> None:
    """Блок кнопок керування екіпіруванням"""

    if st.session_state.hero.alive:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button(
                f"{Emoji.WEAPON.value} Екіпірувати зброю",
                type="secondary",
                width=BUTTON_WIDTH,
            ):
                st.session_state.hero.equipment.equip_weapon(
                    st.session_state.hero.equipment.select_item(Weapon)
                )
                st.rerun()
        with col2:
            if st.button(
                f"{Emoji.SHIELD.value} Екіпірувати щит",
                type="secondary",
                width=BUTTON_WIDTH,
            ):
                st.session_state.hero.equipment.equip_shield(
                    st.session_state.hero.equipment.select_item(Shield)
                )
                st.rerun()
        with col3:
            if st.button(
                f"{Emoji.X.value} Зняти зброю", type="secondary", width=BUTTON_WIDTH
            ):
                st.session_state.hero.equipment.equip_weapon()
                st.rerun()
        with col4:
            if st.button(
                f"{Emoji.X.value} Зняти щит", type="secondary", width=BUTTON_WIDTH
            ):
                st.session_state.hero.equipment.equip_shield()
                st.rerun()


def show_log(expanded: bool = False) -> None:
    """Експандер з логом гри"""

    with st.expander(f"{Emoji.LOG.value} Лог подій:", expanded=expanded):
        text = read_buffer()
        if text:
            st.text(text)
        else:
            st.text(f"Подій поки не було {Emoji.X.value}")


def show_hero() -> None:
    """Перегляд характеристик героя"""

    st.text(st.session_state.hero)
    if st.session_state.hero.alive:
        st.write(st.session_state.hero.display.lives())
        st.write(st.session_state.hero.display.hp())
        st.write(st.session_state.hero.display.level())
        st.write(st.session_state.hero.display.stats())
        st.write(st.session_state.hero.display.ac())
        st.write(st.session_state.hero.display.modifiers())
        st.write(st.session_state.hero.display.skills())
        st.write(st.session_state.hero.display.inventory())
