# -*- coding: utf-8 -*-

import streamlit as st

import karatel.logic.tic_tac_toe_4x4 as ttt
from karatel.core.game_state_manager import GameStateManager
from karatel.storage.abstract import FirebaseSaver  # SQLiteSaver
from karatel.ui.abstract import BufferedOutput
from karatel.utils.settings import LOG


def init_session_state():
    """Ініціалізує всі змінні сесії"""

    defaults = {
        'hero': None,
        'game_state': None,
        'game_map': None,
        'gsm': None,
        'ai': None,
        'ttt_board': None,
        'first_start': True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.first_start:
        st.session_state.gsm = GameStateManager(
            output=BufferedOutput(), saver=FirebaseSaver(), can_generate_map=False
        )
        st.session_state.ttt_board = ttt.START_BOARD.copy()
        st.session_state.first_start = False


def check_username_and_password(username: str, password: str) -> bool:
    uname = st.session_state.gsm.saver.check_username(
        output=st.session_state.gsm.output,
        username=username,
        log=LOG,
    )
    pwd = st.session_state.gsm.saver.check_password(
        output=st.session_state.gsm.output,
        password=password,
        log=LOG,
    )
    if not uname or not pwd:
        st.rerun()
    return uname and pwd


def user_params_update(
    local_id: str, email: str, id_token: str, refresh_token: str
) -> None:
    st.session_state.gsm.local_id = local_id
    st.session_state.gsm.email = email
    st.session_state.gsm.id_token = id_token
    st.session_state.gsm.refresh_token = refresh_token
