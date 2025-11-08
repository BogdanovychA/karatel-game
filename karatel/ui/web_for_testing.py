import streamlit as st

from karatel.core.hero import HeroFactory
from karatel.core.professions import PROFESSIONS
from karatel.logic.combat import fight
from karatel.ui.abstract import ui
from karatel.ui.web_elements import dungeon_button, hero_button, navigation, show_log
from karatel.ui.web_gui import TITLE
from karatel.utils.settings import DEBUG, MAX_LEVEL, MIN_LEVEL


def menu() -> None:
    st.title(TITLE)
    st.header("Головне меню")

    col1, col2 = st.columns([1, 3])
    with col1:
        hero_button()
        dungeon_button()
        if DEBUG:
            if st.button("Ворог", type="secondary", width=150):
                st.session_state.game_state = "enemy"
                st.rerun()
            if st.button("Швидкий бій", type="secondary", width=150):
                st.session_state.game_state = "fast"
                st.rerun()
        if st.button("Назад", type="secondary", width=150):
            st.session_state.game_state = None
            st.rerun()
    with col2:
        st.subheader(
            "Створіть собі героя та вирушайте в захопливі пригоди у підземелля. "
            + "Вбивайте ворогів, знаходьте зброю та засоби захисту. "
            + "Знайдіть вихід -- дійдіть до дверей."
        )


def enemy() -> None:
    st.title(TITLE)
    st.header("Ворог")

    if 'enemy' in st.session_state:
        if not st.session_state.enemy:
            profession = st.selectbox(
                "Професія",
                options=list(PROFESSIONS.keys()),
                format_func=lambda x: PROFESSIONS[x].name,
            )
            level = st.slider(
                "Рівень",
                MIN_LEVEL,
                MAX_LEVEL,
                MIN_LEVEL if not st.session_state.hero else st.session_state.hero.level,
            )

            if st.button("Створити ворога", type="secondary", width=150):
                st.session_state.enemy = HeroFactory.generate(
                    level=level, profession=profession, name=HeroFactory.select_name()
                )
                st.success(f"Ворога {st.session_state.enemy.name} створено!")
                st.rerun()

        else:
            st.success("Ворога створено")
            st.text(st.session_state.enemy.display.show())

            if st.button("Видалити ворога", type="primary", width=150):
                st.session_state.enemy = None
                ui.clear()
                st.rerun()
            show_log()
    navigation()


def fast() -> None:
    st.title(TITLE)
    if not st.session_state.hero:
        st.subheader("Створіть героя, щоб почати бійку")

    if 'hero' in st.session_state and st.session_state.hero:
        with st.expander("Ваш Герой:", expanded=True):
            st.text(st.session_state.hero.display.show())

        if 'enemy' in st.session_state and (
            not st.session_state.enemy or not st.session_state.enemy.alive
        ):
            st.session_state.enemy = HeroFactory.generate(
                level=st.session_state.hero.level
            )

        if 'enemy' in st.session_state and st.session_state.enemy:
            with st.expander("Ваш ворог:", expanded=True):
                st.text(st.session_state.enemy.display.show())
            if st.button("Почати бій", type="primary", width=150):
                fight(st.session_state.hero, st.session_state.enemy)
                show_log()

    navigation()
