# -*- coding: utf-8 -*-

import pickle

import streamlit as st

from karatel.ai.abstract import Anthropic, Google, MasterAI, OpenAI
from karatel.ai.constants import AIName
from karatel.core.hero import HeroFactory
from karatel.core.map import generate_map, render_map
from karatel.core.professions import PROFESSIONS, Profession, show_professions
from karatel.logic.map import find_hero, output_setter
from karatel.ui.web.constants import BUTTON_WIDTH, TITLE, GameState
from karatel.ui.web.elements import (
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
from karatel.ui.web.logic import check_password, check_username_and_password
from karatel.utils.constants import Emoji, Sex
from karatel.utils.crypt import hash_pass, validate_password
from karatel.utils.settings import DEBUG, HERO_LIVES, LOG, MAX_LEVEL, MIN_LEVEL


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


def authenticate_user():

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

    with st.form(key='login_registration_form'):

        col1, col2 = st.columns(2)
        with col1:
            username = username_input()
            password = pass_input()

            colum1, colum2 = st.columns(2)
            with colum1:
                submitted_login = st.form_submit_button(
                    "Вхід",
                    icon=Emoji.LOGIN.value,
                    type="secondary",
                    width=BUTTON_WIDTH,
                )
            with colum2:
                submitted_registration = st.form_submit_button(
                    "Реєстрація",
                    icon=Emoji.REG.value,
                    type="secondary",
                    width=BUTTON_WIDTH,
                )

        with col2:
            st.text(st.session_state.gsm.output.read_buffer())

    def _start_logic() -> None:
        st.session_state.gsm.username = username
        st.session_state.game_state = GameState.HERO.value

    # Логіка роботи кнопок
    if submitted_login:
        if check_username_and_password(username, password):
            all_data = st.session_state.gsm.saver.select_user(
                output=st.session_state.gsm.output, username=username, log=LOG
            )
            if all_data:
                user_id, hashed_password = all_data
                if validate_password(password, hashed_password):
                    _start_logic()
                else:
                    st.session_state.gsm.output.write("Пароль не коректний")
        st.rerun()
    elif submitted_registration:
        if check_username_and_password(username, password):
            if st.session_state.gsm.saver.register_user(
                output=st.session_state.gsm.output,
                username=username,
                hashed_password=hash_pass(password),
                log=LOG,
            ):
                _start_logic()
            st.rerun()


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
        change_login = st.button(
            "Змінити логін",
            icon=Emoji.LOGIN.value,
            type="secondary",
            width=BUTTON_WIDTH,
        )

    with col2:
        change_password = st.button(
            "Змінити пароль",
            icon=Emoji.KEY.value,
            type="secondary",
            width=BUTTON_WIDTH,
        )

    with col3:

        if 'ai' in st.session_state and st.session_state.ai:
            AI_CLASSES = {
                AIName.OPENAI.value: OpenAI,
                AIName.GOOGLE.value: Google,
                AIName.ANTHROPIC.value: Anthropic,
                AIName.MASTERAI.value: MasterAI,
            }

            ai_options = list(AI_CLASSES.keys())

            current_name = st.session_state.ai.name
            default_index = (
                ai_options.index(current_name) if current_name in ai_options else 0
            )

            ai_model = st.selectbox(
                f"Модель ШІ",
                key="ai_model_radio",
                index=default_index,
                options=ai_options,
            )

            if ai_model != st.session_state.ai.name:
                # Закриваємо старий loop перед створенням нового
                if hasattr(st.session_state.ai, 'close'):
                    try:
                        st.session_state.ai.close()
                    except Exception as e:
                        st.session_state.gsm.output(
                            f"Помилка при закритті попередньої моделі: {e}", log=DEBUG
                        )

                AIClass = AI_CLASSES[ai_model]
                st.session_state.ai = AIClass()
        else:
            pass

    with col4:
        delete_user = st.button(
            "Видалити користувача",
            icon=Emoji.TRASH.value,
            type="primary",
            width=BUTTON_WIDTH,
        )

    navigation()

    # Логіка роботи кнопок
    if change_login:
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

    elif change_password:
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

    elif delete_user:
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


def hero() -> None:
    """ "Екран з гравцем (героєм)"""

    st.title(TITLE)
    st.header(f"{Emoji.HERO.value} Герой")

    if 'hero' in st.session_state:
        if not st.session_state.hero:

            display_sex = st.radio(
                "Оберіть стать",
                key="sex_radio",
                options=[Sex.M.value, Sex.F.value],
            )

            if display_sex == Sex.F.value:
                name_text = "КАРАТЄЛЬКА"
                sex = Sex.F
            else:
                name_text = "КАРАТЄЛЬ"
                sex = Sex.M

            name = st.text_input("Ім'я", icon=Emoji.HERO.value, value=name_text)

            professions_plus_none = {
                None: Profession(
                    name="Оберіть професію",
                    name_fem="Оберіть професію",
                    description="",
                    description_fem="",
                    main_bonuses=("",),
                    secondary_bonuses=("",),
                    penalties=("",),
                ),
                **PROFESSIONS,  # Об'єднуємо зі словником наявних професій
            }

            def _format_profession_name(profession_key: str | None) -> str:
                """Повертає назву професії для відображення за ключем."""
                if display_sex == Sex.F.value:
                    return professions_plus_none[profession_key].name_fem
                else:
                    return professions_plus_none[profession_key].name

            profession = st.selectbox(
                "Професія",
                options=list(professions_plus_none.keys()),
                format_func=_format_profession_name,
            )
            level = st.slider("Рівень", MIN_LEVEL, MAX_LEVEL, MIN_LEVEL)

            with st.expander("Професії", expanded=True):
                show_professions(
                    output=st.session_state.gsm.output, professions=profession, sex=sex
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
                        sex=sex,
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
