# -*- coding: utf-8 -*-

import streamlit as st

from karatel.ai.abstract import Google, OpenAI
from karatel.core.game_state_manager import GameStateManager
from karatel.storage.abstract import SQLiteSaver
from karatel.ui.abstract import BufferedOutput
from karatel.utils.crypt import is_password_valid, is_username_valid


def init_session_state():
    """Ініціалізує всі змінні сесії"""

    defaults = {
        'hero': None,
        'enemy': None,
        'game_state': None,
        'game_map': None,
        'gsm': None,
        'ai': None,
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
        )
        st.session_state.ai = OpenAI()
        # st.session_state.ai = Google()

        st.session_state.first_start = False


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
