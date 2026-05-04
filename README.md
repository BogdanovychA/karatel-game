# 🎲 Karatel Game

![Made in Ukraine](https://img.shields.io/badge/Made%20in-Ukraine-blue?logo=data%3Aimage%2Fsvg%2Bxml%3Bbase64%2CPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjgwMCI%2BCjxyZWN0IHdpZHRoPSIxMjAwIiBoZWlnaHQ9IjgwMCIgZmlsbD0iIzAwNTdCNyIvPgo8cmVjdCB3aWR0aD0iMTIwMCIgaGVpZ2h0PSI0MDAiIHk9IjQwMCIgZmlsbD0iI0ZGRDcwMCIvPgo8L3N2Zz4%3D) 

Текстова RPG гра на базі правил D&D 5e з українською тематикою.

⚠️ **Увага:** Гра наразі **в розробці**. Це моя особиста арена для тренування Python — тут я практикуюся кидати кубики та ламати код. 😎

## 📖 Опис

КАРАТЄЛЬ — рольова гра, де ти створюєш персонажа, обираєш професію і намагаєшся вижити у тактичних боях.
Гра використовує спрощену систему D&D 5e з унікальними українськими професіями, а головне — дає мені привід тренувати свої власні скіли у Python. 😎

Грати: https://karatel.ua/

API: https://karatel.ua/api/docs

## ✨ Особливості

- 🎭 **унікальні професії** — від спецпризначенця до інфлюенсера
- ⚔️ **Система бою** з критичними успіхами та провалами (так, інколи я вчуся на власних помилках)
- 🛡️ **Екіпірування**: зброя (одноручна/дворучна) та щити
- 📊 **Система прогресії**: 20 рівнів, бо Python — це марафон, а не спринт
- 🎯 **Механіка D&D**: кидки кубиків, ініціатива, клас броні
- 🇺🇦 **Українська локалізація** — бо патріотизм теж важливий

## 🚀 Встановлення

### Вимоги
- Python 3.10 або новіше

### Запуск
```bash
git clone https://github.com/BogdanovychA/karatel-game
cd karatel-game
uv sync
uv run pre-commit install
uv run pre-commit run --all-files   # опційно
uv run python3 -m streamlit run ./karatel/__main__.py
uv run python3 -m uvicorn karatel.api.fastapi:app --reload   # для роботи API
