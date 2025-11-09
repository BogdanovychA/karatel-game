# -*- coding: utf-8 -*-

import streamlit as st

from karatel.core.game_state_manager import gsm
from karatel.core.hero import HeroFactory
from karatel.core.map_model import generate_map, render_map
from karatel.core.professions import PROFESSIONS, Profession, show_professions
from karatel.logic.map_logic import move_hero
from karatel.ui.abstract import BufferedOutput
from karatel.ui.web_constants import TITLE, GameState
from karatel.ui.web_elements import equipment, navigation, respawn, show_hero, show_log
from karatel.utils.constants import Emoji
from karatel.utils.settings import HERO_LIVES, LOG, MAX_LEVEL, MIN_LEVEL
from karatel.utils.utils import read_buffer


def init_session_state():
    """Ініціалізує всі змінні сесії"""

    defaults = {
        'hero': None,
        'enemy': None,
        'game_state': None,
        'game_map': None,
        'first_start': True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.first_start:
        gsm.ui = BufferedOutput()

    st.session_state.first_start = False


def check_game_state() -> None:
    """Перевіряє статус гри й направляє на відповідний екран
    (викликає відповідну функцію)"""

    match st.session_state.game_state:
        case None:
            hello()
        case GameState.HERO:
            hero()
        case GameState.ON_MAP:
            on_map()
        case _:
            st.title("Відсутній пункт меню")


def hello() -> None:
    """Перший екран, який бачить користувач"""

    st.image("./karatel/images/logo.png")
    st.header(
        "КАРАТЄЛЬ — рольова гра, де ти створюєш героя, "
        + "обираєш професію і намагаєшся вижити у тактичних боях. "
    )
    st.subheader(
        "Гра використовує спрощену систему D&D 5e з унікальними українськими "
        + "професіями."
    )
    st.subheader(
        "Створіть собі героя та вирушайте в захопливі пригоди у підземелля. "
        + "Вбивайте ворогів, знаходьте зброю та засоби захисту. "
        + "Знайдіть вихід -- дійдіть до дверей."
    )
    st.write("Гітхаб: https://github.com/BogdanovychA/karatel-game")
    st.write("Автор: https://www.bogdanovych.org/")

    navigation()


def hero() -> None:
    """ "Екран з гравцем (героєм)"""

    st.title(TITLE)
    st.header("Герой")

    if 'hero' in st.session_state:
        if not st.session_state.hero:
            name = st.text_input("Ім'я", value="КАРАТЄЛЬ")

            professions_plus_none = {
                None: Profession(
                    name="Оберіть професію",
                    description="",
                    main_bonuses=("",),
                    secondary_bonuses=("",),
                    penalties=("",),
                ),
                **PROFESSIONS,  # Об'єднуємо зі словником наявних професій
            }

            profession = st.selectbox(
                "Професія",
                options=list(professions_plus_none.keys()),
                format_func=lambda x: professions_plus_none[x].name,
            )
            level = st.slider("Рівень", MIN_LEVEL, MAX_LEVEL, MIN_LEVEL)

            with st.expander("Професії", expanded=True):
                show_professions(profession)
                st.text(read_buffer())

            if st.button("Створити героя", type="secondary", width=150):
                st.session_state.hero = HeroFactory.generate(
                    level=level, profession=profession, name=name
                )
                st.session_state.hero.lives = HERO_LIVES
                st.rerun()

        else:
            show_hero()
            equipment()
            show_log(expanded=True)
            respawn()
    navigation()


def on_map() -> None:
    """Карта (підземелля)"""

    st.title(TITLE)
    st.header("Підземелля")

    if st.session_state.hero is None:
        st.subheader("Створіть героя, щоб почати гру")

    if 'hero' in st.session_state and st.session_state.hero:
        with st.expander("Ваш Герой:", expanded=False):
            show_hero()
            equipment()
        show_log(expanded=True)
        if 'game_map' in st.session_state:
            if not st.session_state.game_map:
                st.session_state.game_map = generate_map(st.session_state.hero)
            if st.session_state.game_map:
                with st.expander("Мапа", expanded=True):
                    render_map(st.session_state.game_map)
                    st.text(read_buffer())

                    if st.session_state.hero.alive:
                        # Верхній ряд (3 кнопки)
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
                        with col1:
                            if st.button("↖️"):
                                move_hero(-1, -1, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col2:
                            if st.button("⬆️"):
                                move_hero(-1, 0, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col3:
                            if st.button("↗️"):
                                move_hero(-1, 1, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col4:
                            st.write(f"Легенда: {Emoji.HERO.value} -- ви")

                        # Середній ряд (3 кнопки)
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
                        with col1:
                            if st.button("⬅️"):
                                move_hero(0, -1, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col2:
                            st.text(" ")
                        with col3:
                            if st.button("➡️"):
                                move_hero(0, 1, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col4:
                            st.write(
                                f"{Emoji.ENEMY.value} -- вороги | {Emoji.ITEM.value} -- скарби |"
                                + f"{Emoji.GOLD.value} -- гроші"
                            )

                        # Нижній ряд (3 кнопки)
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
                        with col1:
                            if st.button("↙️"):
                                move_hero(1, -1, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col2:
                            if st.button("⬇️"):
                                move_hero(1, 0, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col3:
                            if st.button("↘️"):
                                move_hero(1, 1, st.session_state.game_map, log=LOG)
                                st.rerun()
                        with col4:
                            st.write(
                                f"{Emoji.BOOK.value} -- досвід | {Emoji.EMPTY.value} -- нічого | "
                                + f"{Emoji.EXIT.value} -- вихід"
                            )
                    else:
                        st.write(
                            f"{Emoji.TOMB.value} {st.session_state.hero.display.show()}"
                        )
                        respawn()
    navigation()
