# -*- coding: utf-8 -*-
import gui
import streamlit as st

gui.init_session_state()

match st.session_state.game_state:
    case None:
        gui.hello()
    case "menu":
        gui.menu()
    case "hero":
        gui.hero()
    case "fast":
        gui.fast()
    case _:
        st.title("Відсутній пункт меню")
