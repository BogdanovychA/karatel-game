import streamlit as st
from combat import fight
from hero import Hero, HeroFactory
from professions import PROFESSIONS
from ui import ui

TITLE = "Karatel Game"


def read_buffer() -> str:
    text = "\n".join(str(a) for a in ui.get_buffer())
    ui.clear()
    return text


def init_session_state():
    """Ініціалізує всі змінні сесії"""
    defaults = {
        'hero': None,
        'enemy': None,
        'game_state': None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def back() -> None:
    if st.button("Назад", type="secondary"):
        st.session_state.game_state = "menu"
        st.rerun()


def hello() -> None:
    st.title(TITLE)
    st.header(
        "Karatel Game — консольна рольова гра, де ти створюєш персонажа, "
        + "обираєш професію і пробуєш вижити у тактичних боях. "
        + "Гра використовує спрощену систему D&D 5e з унікальними українськими "
        + "професіями"
    )
    if st.button("Старт", type="primary"):
        st.session_state.game_state = "menu"
        st.rerun()


def menu() -> None:
    st.title(TITLE)
    st.header("Головне меню")
    if st.button("Персонаж", type="primary"):
        st.session_state.game_state = "hero"
        st.rerun()
    if st.button("Швидкий бій", type="secondary"):
        st.session_state.game_state = "fast"
        st.rerun()
    if st.button("Назад", type="secondary"):
        st.session_state.game_state = None
        st.rerun()


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
            # Створюємо героя та зберігаємо в session_state
            st.session_state.hero = HeroFactory.generate(
                level=level, profession=profession, name=name
            )
            st.success(f"Героя {name} створено!")
            st.rerun()

    else:
        st.success("Героя створено")
        st.text(st.session_state.hero.display.show())

        if st.button("Видалити героя", type="secondary"):
            st.session_state.hero = None
            ui.clear()
            st.rerun()
    back()


def fast() -> None:
    st.title(TITLE)
    if st.session_state.hero is None:
        st.header("Створіть персонажа, щоб почати бійку")

    if 'hero' in st.session_state and st.session_state.hero is not None:
        if (
            'enemy' in st.session_state
            and st.session_state.enemy is None
            or not st.session_state.enemy.alive
        ):
            st.session_state.enemy = HeroFactory.generate(
                level=st.session_state.hero.level
            )

        if 'enemy' in st.session_state and st.session_state.enemy is not None:
            st.header("Ваш ворог:")
            st.text(st.session_state.enemy.display.show())
            fight(st.session_state.hero, st.session_state.enemy)
            st.header("Лог бою:")
            st.text(read_buffer())

    back()
