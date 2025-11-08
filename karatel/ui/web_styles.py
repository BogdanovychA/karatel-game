import streamlit as st


def apply_styles():
    st.set_page_config(
        page_title="КАРАТЄЛЬ",
        page_icon="./karatel/images/favicon.png",  # або emoji типу "⚔️"
        # layout="wide"
    )
    st.markdown(
        """
        <style>

        /* Прибрати верхню сіру панель */
        div[data-testid="stToolbar"] {
            visibility: hidden;
            height: 0;
        }

        /* Мінімальний відступ зверху */
        div.block-container {
            padding-top: 3rem !important;
        }

        /* Прибрати порожній простір під заголовком */
        h1 {
            margin-top: 0rem !important;
            margin-bottom: 0.0rem !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
