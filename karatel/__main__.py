# -*- coding: utf-8 -*-
from karatel.ui import web_gui as gui
from karatel.ui.web_styles import apply_styles

apply_styles()
gui.init_session_state()
gui.check_game_state()
