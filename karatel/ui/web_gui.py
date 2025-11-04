import streamlit as st

from karatel.core.hero import HeroFactory
from karatel.core.map_model import generate_map, render_map
from karatel.core.professions import PROFESSIONS
from karatel.logic.combat import fight
from karatel.ui.abstract import ui

TITLE = "КАРАТЄЛЬ"


def check_game_state() -> None:
    match st.session_state.game_state:
        case None:
            hello()
        case "menu":
            menu()
        case "hero":
            hero()
        case "enemy":
            enemy()
        case "on_map":
            on_map()
        case "fast":
            fast()
        case _:
            st.title("Відсутній пункт меню")


def read_buffer() -> str:
    text = "\n".join(str(a) for a in ui.get_buffer())
    ui.clear()
    return text


def init_session_state():
    """Ініціалізує всі змінні сесії"""
    defaults = {'hero': None, 'enemy': None, 'game_state': None, 'game_map': None}

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def back() -> None:
    if st.button("Назад", type="secondary"):
        st.session_state.game_state = "menu"
        st.rerun()


def hello() -> None:
    # st.title(TITLE)
    st.image("./karatel/images/logo.png")
    st.header(
        "КАРАТЄЛЬ — консольна рольова гра, де ти створюєш персонажа, "
        + "обираєш професію і пробуєш вижити у тактичних боях. "
        + "Гра використовує спрощену систему D&D 5e з унікальними українськими "
        + "професіями"
    )
    if st.button("СТАРТ", type="primary"):
        st.session_state.game_state = "menu"
        st.rerun()


def menu() -> None:
    st.title(TITLE)
    st.header("Головне меню")
    if st.button("Персонаж", type="primary"):
        st.session_state.game_state = "hero"
        st.rerun()
    if st.button("Ворог", type="primary"):
        st.session_state.game_state = "enemy"
        st.rerun()
    if st.button("Підземелля", type="primary"):
        st.session_state.game_state = "on_map"
        st.rerun()
    if st.button("Швидкий бій", type="secondary"):
        st.session_state.game_state = "fast"
        st.rerun()
    if st.button("Назад", type="secondary"):
        st.session_state.game_state = None
        st.rerun()


def on_map():
    st.title(TITLE)
    st.header("Підземелля")

    if st.session_state.hero is None:
        st.subheader("Створіть персонажа, щоб почати гру")

    if 'hero' in st.session_state and st.session_state.hero:
        with st.expander("Ваш Герой:", expanded=False):
            st.text(st.session_state.hero.display.show())
        if 'game_map' in st.session_state:
            if not st.session_state.game_map:
                st.session_state.game_map = generate_map(st.session_state.hero)
            if st.session_state.game_map:
                with st.expander("Мапа", expanded=True):
                    render_map(st.session_state.game_map)
                    st.text(read_buffer())

    back()


def hero() -> None:
    st.title(TITLE)
    st.header("Персонаж")

    if st.session_state.hero is None:
        name = st.text_input("Ім'я", value="Іван")
        profession = st.selectbox(
            "Професія",
            options=list(PROFESSIONS.keys()),
            format_func=lambda x: PROFESSIONS[x].name,
        )
        level = st.slider("Рівень", 1, 20, 1)

        if st.button("Створити героя", type="secondary"):
            st.session_state.hero = HeroFactory.generate(
                level=level, profession=profession, name=name
            )
            st.success(f"Героя {name} створено!")
            st.rerun()

    else:
        st.success("Героя створено")
        st.text(st.session_state.hero.display.show())

        if st.button("Видалити героя", type="primary"):
            st.session_state.hero = None
            if st.session_state.game_map:
                st.session_state.game_map = []
            ui.clear()
            st.rerun()
    back()


def enemy() -> None:
    st.title(TITLE)
    st.header("Ворог")

    if st.session_state.enemy is None:

        profession = st.selectbox(
            "Професія",
            options=list(PROFESSIONS.keys()),
            format_func=lambda x: PROFESSIONS[x].name,
        )
        level = st.slider(
            "Рівень",
            1,
            20,
            1 if st.session_state.hero is None else st.session_state.hero.level,
        )

        if st.button("Створити ворога", type="secondary"):
            st.session_state.enemy = HeroFactory.generate(
                level=level, profession=profession, name=HeroFactory.select_name()
            )
            st.success(f"Ворога {st.session_state.enemy.name} створено!")
            st.rerun()

    else:
        st.success("Ворога створено")
        st.text(st.session_state.enemy.display.show())

        if st.button("Видалити ворога", type="primary"):
            st.session_state.enemy = None
            ui.clear()
            st.rerun()
    back()


def fast() -> None:
    st.title(TITLE)
    if st.session_state.hero is None:
        st.subheader("Створіть персонажа, щоб почати бійку")

    if 'hero' in st.session_state and st.session_state.hero is not None:
        with st.expander("Ваш Герой:", expanded=True):
            st.text(st.session_state.hero.display.show())

        if 'enemy' in st.session_state and (
            st.session_state.enemy is None or not st.session_state.enemy.alive
        ):
            st.session_state.enemy = HeroFactory.generate(
                level=st.session_state.hero.level
            )

        if 'enemy' in st.session_state and st.session_state.enemy is not None:
            with st.expander("Ваш ворог:", expanded=True):
                st.text(st.session_state.enemy.display.show())
            if st.button("Почати бій", type="primary"):
                fight(st.session_state.hero, st.session_state.enemy)
                with st.expander("Лог бою:"):
                    st.text(read_buffer())

    back()
