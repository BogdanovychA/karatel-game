# map_renderer.py
def render_simple_map(game_map) -> str:
    """Проста HTML карта з emoji"""
    html = """
    <style>
    .game-map {
        display: grid;
        grid-template-columns: repeat(10, 50px);
        gap: 2px;
        background: #1a1a1a;
        padding: 15px;
        border-radius: 10px;
        width: fit-content;
        margin: 20px auto;
    }
    .cell {
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 32px;
        border-radius: 5px;
        background: #2d2d2d;
        transition: all 0.3s ease;
    }
    .cell:hover {
        transform: scale(1.1);
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.3);
    }
    </style>

    <div class="game-map">
    """

    # Генеруємо клітинки
    for y in range(10):
        for x in range(10):
            # Визначаємо що відображати (заглушка)
            if x == 0 and y == 0:
                emoji = "🧙"  # Герой
            elif x == 9 and y == 9:
                emoji = "🚪"  # Вихід
            elif (x + y) % 5 == 0:
                emoji = "👹"  # Ворог
            elif (x * y) % 7 == 0:
                emoji = "💎"  # Скарб
            else:
                emoji = "⬜"  # Пусто

            html += f'<div class="cell">{emoji}</div>'

    html += "</div>"
    return html


# Використання в Streamlit
import streamlit as st

st.markdown(render_simple_map(None), unsafe_allow_html=True)
