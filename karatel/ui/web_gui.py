# -*- coding: utf-8 -*-

import streamlit as st

from karatel.core.game_state_manager import GameStateManager
from karatel.core.hero import HeroFactory
from karatel.core.map_model import generate_map, render_map
from karatel.core.professions import PROFESSIONS, Profession, show_professions
from karatel.ui.abstract import BufferedOutput, XMLHeroSaver
from karatel.ui.web_constants import BUTTON_WIDTH, TITLE, GameState
from karatel.ui.web_elements import (
    equipment,
    legend,
    load_button,
    movement_controls,
    navigation,
    respawn,
    show_hero,
    show_log,
)
from karatel.utils.constants import Emoji
from karatel.utils.settings import HERO_LIVES, MAX_LEVEL, MIN_LEVEL


def init_session_state():
    """Ініціалізує всі змінні сесії"""

    defaults = {
        'hero': None,
        'enemy': None,
        'game_state': None,
        'game_map': None,
        'gsm': None,
        'first_start': True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.first_start:
        st.session_state.gsm = GameStateManager(
            output=BufferedOutput(),
            saver=XMLHeroSaver(),
            can_generate_map=False,
        )
        st.session_state.first_start = False


def check_game_state() -> None:
    """Перевіряє статус гри й направляє на відповідний екран
    (викликає відповідну функцію)"""

    match st.session_state.game_state:
        case None:
            hello()
        case GameState.HERO.value:
            hero()
        case GameState.ON_MAP.value:
            on_map()
        case _:
            st.title(f"{Emoji.X.value} Відсутній пункт меню")
            st.write(f"game_state: {st.session_state.game_state.value}")


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
    st.header(f"{Emoji.HERO.value} Герой")

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
                show_professions(
                    output=st.session_state.gsm.output, professions=profession
                )
                st.text(st.session_state.gsm.output.read_buffer())

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

            with col1:
                if st.button(
                    "Створити",
                    icon=Emoji.HERO.value,
                    type="secondary",
                    width=BUTTON_WIDTH,
                ):
                    st.session_state.hero = HeroFactory.generate(
                        output=st.session_state.gsm.output,
                        level=level,
                        profession=profession,
                        name=name,
                    )
                    st.session_state.hero.lives = HERO_LIVES
                    st.rerun()
            with col2:
                load_button()
            with col3:
                pass
            with col4:
                pass

        else:
            show_hero()
            equipment()
            show_log(expanded=True)
            respawn()
    navigation()


def on_map() -> None:
    """Карта (підземелля)"""

    st.title(TITLE)
    st.header(f"{Emoji.DUNG.value} Підземелля")

    if st.session_state.hero is None:
        st.warning("Створіть героя, щоб почати гру")
        return

    if 'hero' in st.session_state and st.session_state.hero:
        with st.expander(f"{Emoji.HERO.value} Ваш Герой:", expanded=False):
            show_hero()
            equipment()
        show_log(expanded=True)
        if 'game_map' in st.session_state:
            if not st.session_state.game_map:
                st.session_state.game_map = generate_map(st.session_state.hero)
            if st.session_state.game_map:
                with st.expander(f"{Emoji.DUNG.value} Мапа", expanded=True):
                    render_map(st.session_state.gsm.output, st.session_state.game_map)
                    st.text(st.session_state.gsm.output.read_buffer())

                    if st.session_state.hero.alive:
                        colum1, colum2 = st.columns([1, 3])
                        with colum1:
                            movement_controls()
                        with colum2:
                            legend()
                    else:
                        st.write(
                            f"{Emoji.TOMB.value} {st.session_state.hero.display.show()}"
                        )
                        respawn()
    navigation()
