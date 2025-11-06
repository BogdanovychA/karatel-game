import streamlit as st

from karatel.core.hero import HeroFactory
from karatel.core.items import Shield, Weapon
from karatel.core.map_model import Emoji, generate_map, render_map
from karatel.core.professions import PROFESSIONS
from karatel.logic.combat import fight
from karatel.logic.map_logic import move_hero
from karatel.ui.abstract import ui
from karatel.utils.settings import DEBUG, MAX_LEVEL, MIN_LEVEL

TITLE = "КАРАТЄЛЬ"


def check_game_state() -> None:
    match st.session_state.game_state:
        case None:
            hello()
        case "menu":
            menu()
        case "hero":
            hero()
        case "enemy":
            enemy()
        case "on_map":
            on_map()
        case "fast":
            fast()
        case _:
            st.title("Відсутній пункт меню")


def read_buffer() -> str:
    text = "\n".join(str(a) for a in ui.buffer)
    ui.clear()
    return text


def init_session_state():
    """Ініціалізує всі змінні сесії"""
    defaults = {'hero': None, 'enemy': None, 'game_state': None, 'game_map': None}

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


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


def back() -> None:
    if st.button("Назад", type="secondary", width=130):
        st.session_state.game_state = "menu"
        st.rerun()


def show_log() -> None:
    with st.expander("Лог:"):
        st.text(read_buffer())


def show_hero() -> None:
    st.text(st.session_state.hero)
    if st.session_state.hero.alive:
        st.write(st.session_state.hero.display.hp())
        st.write(st.session_state.hero.display.level())
        st.write(st.session_state.hero.display.stats())
        st.write(st.session_state.hero.display.ac())
        st.write(st.session_state.hero.display.modifiers())
        st.write(st.session_state.hero.display.skills())
        st.write(st.session_state.hero.display.inventory())


def hello() -> None:
    # st.title(TITLE)
    st.image("./karatel/images/logo.png")
    st.header(
        "КАРАТЄЛЬ — рольова гра, де ти створюєш персонажа, "
        + "обираєш професію і намагаєшся вижити у тактичних боях. "
    )
    st.subheader(
        "Гра використовує спрощену систему D&D 5e з унікальними українськими "
        + "професіями."
    )
    st.subheader("Гітхаб: https://github.com/BogdanovychA/karatel-game")
    st.subheader("Автор: https://www.bogdanovych.org/")
    if st.button("СТАРТ", type="primary", width=130):
        st.session_state.game_state = "menu"
        st.rerun()


def menu() -> None:
    st.title(TITLE)
    st.header("Головне меню")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("Персонаж", type="primary", width=130):
            st.session_state.game_state = "hero"
            st.rerun()
        if st.button("Підземелля", type="primary", width=130):
            st.session_state.game_state = "on_map"
            st.rerun()
        if DEBUG:
            if st.button("Ворог", type="secondary", width=130):
                st.session_state.game_state = "enemy"
                st.rerun()
            if st.button("Швидкий бій", type="secondary", width=130):
                st.session_state.game_state = "fast"
                st.rerun()
        if st.button("Назад", type="secondary", width=130):
            st.session_state.game_state = None
            st.rerun()
    with col2:
        st.subheader(
            "Створіть собі героя та вирушайте в захопливі пригоди у підземелля. "
            + "Вбивайте ворогів, знаходьте зброю та засоби захисту. "
            + "Знайдіть вихід -- дійдіть до дверей."
        )


def on_map():
    st.title(TITLE)
    st.header("Підземелля")

    if st.session_state.hero is None:
        st.subheader("Створіть персонажа, щоб почати гру")

    if 'hero' in st.session_state and st.session_state.hero:
        with st.expander("Ваш Герой:", expanded=False):
            show_hero()
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
                                move_hero(-1, -1, st.session_state.game_map)
                                st.rerun()
                        with col2:
                            if st.button("⬆️"):
                                move_hero(-1, 0, st.session_state.game_map)
                                st.rerun()
                        with col3:
                            if st.button("↗️"):
                                move_hero(-1, 1, st.session_state.game_map)
                                st.rerun()
                        with col4:
                            st.subheader("Легенда:")

                        # Середній ряд (3 кнопки)
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
                        with col1:
                            if st.button("⬅️"):
                                move_hero(0, -1, st.session_state.game_map)
                                st.rerun()
                        with col2:
                            st.text(" ")
                        with col3:
                            if st.button("➡️"):
                                move_hero(0, 1, st.session_state.game_map)
                                st.rerun()
                        with col4:
                            st.write(
                                f"{Emoji.HERO.value} -- ви | {Emoji.ENEMY.value} -- вороги | "
                                + f"{Emoji.ITEM.value} -- скарби"
                            )

                        # Нижній ряд (3 кнопки)
                        col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
                        with col1:
                            if st.button("↙️"):
                                move_hero(1, -1, st.session_state.game_map)
                                st.rerun()
                        with col2:
                            if st.button("⬇️"):
                                move_hero(1, 0, st.session_state.game_map)
                                st.rerun()
                        with col3:
                            if st.button("↘️"):
                                move_hero(1, 1, st.session_state.game_map)
                                st.rerun()
                        with col4:
                            st.write(
                                f"{Emoji.BOOK.value} -- досвід | {Emoji.EMPTY.value} -- нічого | "
                                + f"{Emoji.EXIT.value} -- вихід"
                            )
                    else:
                        st.write(f"{Emoji.TOMB.value} {st.session_state.hero}")
    back()


def hero() -> None:
    st.title(TITLE)
    st.header("Персонаж")

    if 'hero' in st.session_state:
        if not st.session_state.hero:
            name = st.text_input("Ім'я", value="Іван")
            profession = st.selectbox(
                "Професія",
                options=list(PROFESSIONS.keys()),
                format_func=lambda x: PROFESSIONS[x].name,
            )
            level = st.slider("Рівень", MIN_LEVEL, MAX_LEVEL, MIN_LEVEL)

            if st.button("Створити героя", type="secondary", width=150):
                st.session_state.hero = HeroFactory.generate(
                    level=level, profession=profession, name=name
                )
                st.rerun()

        else:
            show_hero()

            if st.session_state.hero.alive:
                col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
                with col1:
                    if st.button("Екіпірувати зброю", type="secondary", width=150):
                        st.session_state.hero.equipment.equip_weapon(
                            st.session_state.hero.equipment.select_item(Weapon)
                        )
                        st.rerun()
                with col2:
                    if st.button("Екіпірувати щит", type="secondary", width=150):
                        st.session_state.hero.equipment.equip_shield(
                            st.session_state.hero.equipment.select_item(Shield)
                        )
                        st.rerun()
                with col3:
                    if st.button("Зняти зброю", type="secondary", width=150):
                        st.session_state.hero.equipment.equip_weapon()
                        st.rerun()
                with col4:
                    if st.button("Зняти щит", type="secondary", width=150):
                        st.session_state.hero.equipment.equip_shield()
                        st.rerun()

            show_log()

            if st.button("Видалити героя", type="primary", width=150):
                st.session_state.hero = None
                if 'game_map' in st.session_state and st.session_state.game_map:
                    st.session_state.game_map = None
                ui.clear()
                st.rerun()
    back()


def enemy() -> None:
    st.title(TITLE)
    st.header("Ворог")

    if 'enemy' in st.session_state:
        if not st.session_state.enemy:
            profession = st.selectbox(
                "Професія",
                options=list(PROFESSIONS.keys()),
                format_func=lambda x: PROFESSIONS[x].name,
            )
            level = st.slider(
                "Рівень",
                MIN_LEVEL,
                MAX_LEVEL,
                MIN_LEVEL if not st.session_state.hero else st.session_state.hero.level,
            )

            if st.button("Створити ворога", type="secondary", width=150):
                st.session_state.enemy = HeroFactory.generate(
                    level=level, profession=profession, name=HeroFactory.select_name()
                )
                st.success(f"Ворога {st.session_state.enemy.name} створено!")
                st.rerun()

        else:
            st.success("Ворога створено")
            st.text(st.session_state.enemy.display.show())

            if st.button("Видалити ворога", type="primary", width=150):
                st.session_state.enemy = None
                ui.clear()
                st.rerun()
            show_log()
    back()


def fast() -> None:
    st.title(TITLE)
    if not st.session_state.hero:
        st.subheader("Створіть персонажа, щоб почати бійку")

    if 'hero' in st.session_state and st.session_state.hero:
        with st.expander("Ваш Герой:", expanded=True):
            st.text(st.session_state.hero.display.show())

        if 'enemy' in st.session_state and (
            not st.session_state.enemy or not st.session_state.enemy.alive
        ):
            st.session_state.enemy = HeroFactory.generate(
                level=st.session_state.hero.level
            )

        if 'enemy' in st.session_state and st.session_state.enemy:
            with st.expander("Ваш ворог:", expanded=True):
                st.text(st.session_state.enemy.display.show())
            if st.button("Почати бій", type="primary", width=130):
                fight(st.session_state.hero, st.session_state.enemy)
                show_log()

    back()
