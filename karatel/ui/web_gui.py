# -*- coding: utf-8 -*-

import pickle

import streamlit as st

from karatel.core.game_state_manager import GameStateManager
from karatel.core.hero import HeroFactory
from karatel.core.map_model import generate_map, render_map
from karatel.core.professions import PROFESSIONS, Profession, show_professions
from karatel.logic.map_logic import find_hero, output_setter
from karatel.storage.abstract import SQLiteHeroSaver
from karatel.storage.sqlite_manager import select_heroes
from karatel.ui.abstract import BufferedOutput
from karatel.ui.web_constants import BUTTON_WIDTH, TITLE, GameState
from karatel.ui.web_elements import (
    equipment,
    legend,
    movement_controls,
    navigation,
    respawn,
    select_load_button,
    show_hero,
    show_log,
)
from karatel.utils.constants import Emoji
from karatel.utils.settings import HERO_LIVES, HERO_SQL_TABLE, LOG, MAX_LEVEL, MIN_LEVEL


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
            # saver=XMLHeroSaver(),
            # saver=JSONHeroSaver(),
            saver=SQLiteHeroSaver(),
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
        case GameState.LOAD_HERO.value:
            load_hero()
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
                select_load_button()
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


def load_hero() -> None:
    st.title(TITLE)
    st.header(f"{Emoji.LOG.value} Список збережених {Emoji.HERO.value} Героїв")
    all_saved_heroes = select_heroes(st.session_state.gsm.output, HERO_SQL_TABLE)

    col1, col2, col3, col4, col5 = st.columns([1, 7, 2, 4, 4])
    with col1:
        st.html("<b>ID</b>")
    with col2:
        st.html("<b>Ім'я</b>")
    with col3:
        st.html("<b>Мапа</b>")
    with col4:
        pass
    with col5:
        pass

    for saved_hero in all_saved_heroes:
        hero_id, hero_name, pickled_hero, pickled_map = saved_hero
        col1, col2, col3, col4, col5 = st.columns([1, 7, 2, 4, 4])
        with col1:
            st.text(hero_id)
        with col2:
            st.text(hero_name)
        with col3:
            if pickle.loads(pickled_map) is not None:
                st.text(Emoji.CHECK.value)
            else:
                st.text(Emoji.X.value)
        with col4:
            if st.button(
                "Відновити",
                icon=Emoji.HERO.value,
                type="secondary",
                width=BUTTON_WIDTH,
                key=f"respawn{hero_id}",
            ):
                # Відновлюємо героя та мапу
                st.session_state.hero, st.session_state.game_map = (
                    st.session_state.gsm.saver.load(
                        output=st.session_state.gsm.output, hero_id=hero_id, log=LOG
                    )
                )
                # Встановлюємо відновленому герою output поточної сесії
                st.session_state.hero.output = st.session_state.gsm.output
                if st.session_state.game_map:
                    y, x = find_hero(st.session_state.game_map)
                    # Встановлюємо екземпляр новоствореного героя на мапу
                    st.session_state.game_map[y][x].obj = st.session_state.hero
                    # Встановлюємо всім об'єктам на мапі поточний output
                    output_setter(
                        st.session_state.game_map, st.session_state.gsm.output
                    )
                st.session_state.game_state = GameState.HERO.value
                st.rerun()
        with col5:
            if st.button(
                "Видалити",
                icon=Emoji.TOMB.value,
                type="primary",
                width=BUTTON_WIDTH,
                key=f"del{hero_id}",
            ):
                st.session_state.gsm.saver.delete(
                    output=st.session_state.gsm.output,
                    row_id=hero_id,
                )
                st.rerun()

    st.write()
    navigation()
