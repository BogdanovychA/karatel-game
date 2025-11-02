# -*- coding: utf-8 -*-

import streamlit as st
from combat import fight
from hero import Hero, HeroFactory
from professions import PROFESSIONS
from ui import ui


def init_session_state():
    """Ініціалізує всі змінні сесії"""
    defaults = {
        'hero': None,
        'enemy': None,
        # 'fight_logs': [],
        # 'battle_count': 0,
        # 'game_started': False
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# Викликаємо один раз на початку
init_session_state()

# ============= UI =============
st.title("⚔️ Karatel Game")

if st.session_state.hero is None:
    st.header("Створіть персонажа, щоб почати бійку")

# Sidebar для створення героя
with st.sidebar:
    st.header("Управління героєм")

    if st.session_state.hero is None:
        # Форма створення героя
        name = st.text_input("Ім'я", value="Іван")
        profession = st.selectbox(
            "Професія",
            options=list(PROFESSIONS.keys()),
            format_func=lambda x: PROFESSIONS[x].name,
        )
        level = st.slider("Рівень", 1, 20, 1)

        if st.button("Створити героя", type="primary"):
            # Створюємо героя та зберігаємо в session_state
            st.session_state.hero = HeroFactory.generate(
                level=level, profession=profession, name=name
            )
            st.success(f"Героя {name} створено!")
            st.rerun()  # Перезапускаємо для оновлення UI

    else:
        # Герой вже створений
        hero = st.session_state.hero
        st.success(f"{hero}")
        st.text(st.session_state.hero.display.show())

        if st.button("Видалити героя", type="secondary"):
            st.session_state.hero = None
            st.session_state.enemy = None
            # st.session_state.fight_logs = []
            ui.clear()
            st.rerun()


if 'hero' in st.session_state and st.session_state.hero is not None:
    if st.session_state.enemy is None:
        st.session_state.enemy = HeroFactory.generate(level=st.session_state.hero.level)
    st.header("Ваш ворог:")
    st.text(st.session_state.enemy.display.show())


if (
    'hero' in st.session_state
    and st.session_state.hero is not None
    and 'enemy' in st.session_state
    and st.session_state.enemy is not None
):
    fight(st.session_state.hero, st.session_state.enemy)
    st.header("Лог бою:")
    # st.session_state.fight_logs = ui.get_buffer()

    for item in ui.get_buffer():
        st.text(item)
