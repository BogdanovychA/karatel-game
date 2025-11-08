import streamlit as st

from karatel.core.items import Shield, Weapon
from karatel.ui.abstract import ui
from karatel.utils.utils import read_buffer


def back_button() -> None:
    if st.button("Назад", type="secondary", width=150):
        st.session_state.game_state = None
        st.rerun()


def dungeon_button() -> None:
    if st.session_state.hero:
        if st.button("Підземелля", type="secondary", width=150):
            st.session_state.game_state = "on_map"
            st.rerun()


def hero_button() -> None:
    if st.button("Герой", type="secondary", width=150):
        st.session_state.game_state = "hero"
        st.rerun()


def navigation() -> None:
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        match st.session_state.game_state:
            case "hero":
                dungeon_button()
            case "on_map" | None:
                hero_button()
    with col2:
        pass
    with col3:
        pass
    with col4:
        if st.session_state.game_state is not None:
            back_button()


def respawn() -> None:

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if not st.session_state.hero.alive:
            if st.session_state.hero.lives > 0:
                if st.button("Відродитиcя", type="secondary", width=150):
                    st.session_state.hero.leveling.set_hp()
                    st.rerun()
            else:
                st.text("Ви програли!")
    with col2:
        pass
    with col3:
        pass
    with col4:
        if st.button("Знищити героя", type="primary", width=150):
            st.session_state.hero = None
            if 'game_map' in st.session_state and st.session_state.game_map:
                st.session_state.game_map = None
            ui.clear()
            st.rerun()


def equipment() -> None:
    if st.session_state.hero.alive:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            if st.button("Екіпірувати зброю", type="secondary", width=150):
                st.session_state.hero.equipment.equip_weapon(
                    st.session_state.hero.equipment.select_item(Weapon)
                )
                st.rerun()
        with col2:
            if st.button("Екіпірувати щит", type="secondary", width=150):
                st.session_state.hero.equipment.equip_shield(
                    st.session_state.hero.equipment.select_item(Shield)
                )
                st.rerun()
        with col3:
            if st.button("Зняти зброю", type="secondary", width=150):
                st.session_state.hero.equipment.equip_weapon()
                st.rerun()
        with col4:
            if st.button("Зняти щит", type="secondary", width=150):
                st.session_state.hero.equipment.equip_shield()
                st.rerun()


def show_log(expanded: bool = False) -> None:
    with st.expander("Лог:", expanded=expanded):
        st.text(read_buffer())


def show_hero() -> None:
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
