# -*- coding: utf-8 -*-

import pickle

import streamlit as st

from karatel.core.game_state_manager import GameStateManager
from karatel.core.hero import HeroFactory
from karatel.core.map_model import generate_map, render_map
from karatel.core.professions import PROFESSIONS, Profession, show_professions
from karatel.logic.map_logic import find_hero, output_setter
from karatel.storage.abstract import SQLiteSaver
from karatel.ui.abstract import BufferedOutput
from karatel.ui.web_constants import BUTTON_WIDTH, TITLE, GameState
from karatel.ui.web_elements import (
    equipment,
    legend,
    load_hero_button,
    movement_controls,
    navigation,
    pass_input,
    respawn,
    show_hero,
    show_log,
    username_input,
)
from karatel.utils.constants import Emoji
from karatel.utils.crypt import (
    hash_pass,
    is_password_valid,
    is_username_valid,
    validate_password,
)
from karatel.utils.settings import HERO_LIVES, LOG, MAX_LEVEL, MIN_LEVEL


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
            saver=SQLiteSaver(),
            username=None,
            can_generate_map=False,
            sex="Чоловік",
        )
        st.session_state.first_start = False


def check_game_state() -> None:
    """Перевіряє статус гри й направляє на відповідний екран
    (викликає відповідну функцію)"""

    if (
        st.session_state.gsm.username is not None
        and st.session_state.game_state is not None
    ):
        match st.session_state.game_state:
            case GameState.HERO.value:
                hero()
            case GameState.MAP.value:
                game_map()
            case GameState.LOAD_HERO.value:
                load_hero()
            case GameState.PROFILE.value:
                profile()
            case _:
                st.title(f"{Emoji.X.value} Відсутній пункт меню")
                st.write(f"game_state: {st.session_state.game_state}")
    else:
        authenticate_user()


def check_username_and_password(username: str, password: str) -> bool:
    uname = check_username(username)
    pwd = check_password(password)
    if not uname or not pwd:
        st.rerun()
    return uname and pwd


def check_username(username: str) -> bool:
    uname = is_username_valid(username)
    if not uname:
        st.session_state.gsm.output.write(
            "Ім'я користувача має містити мінімум 2 символи, "
            + "може мати лише літери латинського алфавіту, "
            + "цифри та знак підкреслення."
        )
    return uname


def check_password(password: str) -> bool:
    pwd = is_password_valid(password)
    if not pwd:
        st.session_state.gsm.output.write(
            "Пароль має складатися з мінімум 8 символів латинського алфавіту, "
            + "має містити мінімум одну велику та одну малу літеру і "
            + "обов'язково має мати мінімум одну цифру і один спеціальний символ."
        )
    return pwd


def authenticate_user():

    def _start() -> None:
        st.session_state.gsm.username = username
        st.session_state.game_state = GameState.HERO.value

    st.image("./karatel/images/logo.png", width=500)
    st.subheader(
        "КАРАТЄЛЬ — рольова гра, де ти створюєш героя, "
        + "обираєш професію і намагаєшся вижити у тактичних боях. "
    )
    st.write(
        "Гра використовує спрощену систему D&D 5e з унікальними українськими "
        + "професіями."
    )
    st.write(
        "Створіть собі героя та вирушайте в захопливі пригоди у підземелля. "
        + "Вбивайте ворогів, знаходьте зброю та засоби захисту. "
        + "Знайдіть вихід -- дійдіть до дверей."
    )
    st.write("Гітхаб: https://github.com/BogdanovychA/karatel-game")
    st.write("Автор: https://www.bogdanovych.org/")

    st.subheader(f"Створіть користувача або авторизуйтеся")

    col1, col2 = st.columns(2)
    with col1:
        username = username_input()
        password = pass_input()
    with col2:
        st.text(st.session_state.gsm.output.read_buffer())

    colum1, colum2 = st.columns(2)

    with colum1:
        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "Вхід",
                icon=Emoji.LOGIN.value,
                type="secondary",
                width=BUTTON_WIDTH,
            ):
                if check_username_and_password(username, password):
                    all_data = st.session_state.gsm.saver.select_user(
                        output=st.session_state.gsm.output, username=username, log=LOG
                    )
                    if all_data:
                        user_id, hashed_password = all_data
                        if validate_password(password, hashed_password):
                            _start()
                        else:
                            st.session_state.gsm.output.write("Пароль не коректний")
                st.rerun()

        with col2:
            if st.button(
                "Реєстрація",
                icon=Emoji.REG.value,
                type="secondary",
                width=BUTTON_WIDTH,
            ):
                if check_username_and_password(username, password):
                    if st.session_state.gsm.saver.register_user(
                        output=st.session_state.gsm.output,
                        username=username,
                        hashed_password=hash_pass(password),
                        log=LOG,
                    ):
                        _start()
                    st.rerun()

    with colum2:
        pass


def profile() -> None:
    """ "Екран з гравцем (героєм)"""
    st.title(TITLE)
    st.header(
        f"{Emoji.PROFILE.value} Профіль користувача '{st.session_state.gsm.username}'"
    )

    col1, col2 = st.columns(2)
    with col1:
        username = username_input()
        password = pass_input()
    with col2:
        st.text(st.session_state.gsm.output.read_buffer())

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button(
            "Змінити логін",
            icon=Emoji.LOGIN.value,
            type="secondary",
            width=BUTTON_WIDTH,
        ):
            if password:
                if check_username_and_password(username, password):
                    all_data = st.session_state.gsm.saver.select_user(
                        output=st.session_state.gsm.output,
                        username=st.session_state.gsm.username,
                        log=LOG,
                    )
                    if all_data:
                        user_id, hashed_password = all_data
                        if validate_password(password, hashed_password):
                            if st.session_state.gsm.saver.update_username(
                                output=st.session_state.gsm.output,
                                user_id=user_id,
                                old_username=st.session_state.gsm.username,
                                new_username=username,
                                log=LOG,
                            ):
                                st.session_state.gsm.username = username
                        else:
                            st.session_state.gsm.output.write("Пароль не коректний")

            else:
                st.session_state.gsm.output.write(
                    "Для зміни імені користувача введіть діючий пароль", log=LOG
                )
            st.rerun()
    with col2:
        if st.button(
            "Змінити пароль",
            icon=Emoji.KEY.value,
            type="secondary",
            width=BUTTON_WIDTH,
        ):
            if check_password(password):
                all_data = st.session_state.gsm.saver.select_user(
                    output=st.session_state.gsm.output,
                    username=st.session_state.gsm.username,
                    log=LOG,
                )
                if all_data:
                    user_id, hashed_password = all_data
                    st.session_state.gsm.saver.update_password(
                        output=st.session_state.gsm.output,
                        user_id=user_id,
                        hashed_password=hash_pass(password),
                        log=LOG,
                    )
            st.rerun()
    with col3:
        pass
    with col4:
        if st.button(
            "Видалити користувача",
            icon=Emoji.TRASH.value,
            type="primary",
            width=BUTTON_WIDTH,
        ):
            if password:
                all_data = st.session_state.gsm.saver.select_user(
                    output=st.session_state.gsm.output, username=username, log=LOG
                )
                if all_data:
                    user_id, hashed_password = all_data
                    if validate_password(password, hashed_password):
                        if st.session_state.gsm.saver.delete_user(
                            output=st.session_state.gsm.output,
                            username=st.session_state.gsm.username,
                            row_id=user_id,
                        ):
                            st.session_state.gsm.username = None
                            st.session_state.game_state = None
                    else:
                        st.session_state.gsm.output.write("Пароль не коректний")
            else:
                st.session_state.gsm.output.write(
                    "Для видалення користувача введіть діючий пароль", log=LOG
                )
            st.rerun()

    navigation()


def hero() -> None:
    """ "Екран з гравцем (героєм)"""

    st.title(TITLE)
    st.header(f"{Emoji.HERO.value} Герой")

    if 'hero' in st.session_state:
        if not st.session_state.hero:

            st.session_state.gsm.sex = st.radio(
                "Оберіть стать",
                key="sex_radio",
                options=["Чоловік", "Жінка"],
            )

            if st.session_state.gsm.sex == "Жінка":
                name_text = "КАРАТЄЛЬКА"
            else:
                name_text = "КАРАТЄЛЬ"

            name = st.text_input("Ім'я", icon=Emoji.HERO.value, value=name_text)

            if st.session_state.gsm.sex == "Жінка":
                man = False
            else:
                man = True

            professions_plus_none = {
                None: Profession(
                    name="Оберіть професію",
                    name_fem="",
                    description="",
                    description_fem="",
                    main_bonuses=("",),
                    secondary_bonuses=("",),
                    penalties=("",),
                ),
                **PROFESSIONS,  # Об'єднуємо зі словником наявних професій
            }

            profession = st.selectbox(
                "Професія",
                options=list(professions_plus_none.keys()),
                format_func=lambda x: professions_plus_none[x].name
                + " / "
                + professions_plus_none[x].name_fem,
            )
            level = st.slider("Рівень", MIN_LEVEL, MAX_LEVEL, MIN_LEVEL)

            with st.expander("Професії", expanded=True):
                show_professions(
                    output=st.session_state.gsm.output, professions=profession, man=man
                )
                st.text(st.session_state.gsm.output.read_buffer())

            col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

            with col1:
                if st.button(
                    "Створити",
                    icon=Emoji.PLUS.value,
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
                load_hero_button()
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


def game_map() -> None:
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
    all_saved_heroes = st.session_state.gsm.saver.list_hero(
        output=st.session_state.gsm.output, username=st.session_state.gsm.username
    )

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
                icon=Emoji.LOAD.value,
                type="secondary",
                width=BUTTON_WIDTH,
                key=f"respawn{hero_id}",
            ):
                # Відновлюємо героя та мапу
                st.session_state.hero, st.session_state.game_map = (
                    st.session_state.gsm.saver.load_hero(
                        username=st.session_state.gsm.username,
                        output=st.session_state.gsm.output,
                        hero_id=hero_id,
                        log=LOG,
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
                icon=Emoji.TRASH.value,
                type="primary",
                width=BUTTON_WIDTH,
                key=f"del{hero_id}",
            ):
                st.session_state.gsm.saver.delete_hero(
                    output=st.session_state.gsm.output,
                    username=st.session_state.gsm.username,
                    row_id=hero_id,
                )
                st.rerun()

    st.write()
    navigation()
