# python -m pytest karatel/tests/test_api.py
#
# python -m pytest karatel/tests/test_api.py --cov=karatel.api --cov-report=html


import pytest
from fastapi.testclient import TestClient

from karatel.api.fastapi import app  # Імпортуйте ваш FastAPI додаток


@pytest.fixture
def client():
    """Фікстура для створення тестового клієнта."""
    return TestClient(app)


def test_get_weapons_all(client):
    """Тест отримання всієї зброї."""
    response = client.get("/weapons?t=all")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_weapons_strength(client):
    """Тест отримання зброї strength"""
    response = client.get("/weapons?t=strength")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_weapons_invalid_type(client):
    """Тест з неправильним типом зброї."""
    response = client.get("/weapons?t=INVALID")
    assert response.status_code == 422


def test_get_professions(client):
    """Тест отримання професій."""
    response = client.get("/professions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0


def test_get_shields(client):
    """Тест отримання щитів."""
    response = client.get("/shields")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_generate_hero(client):
    """Тест генерації героя."""
    response = client.get("/generate_hero")
    assert response.status_code == 200
    hero = response.json()
    assert isinstance(hero, dict)
    assert "name" in hero or "profession" in hero


def test_root(client):
    """Тест кореневого ендпоінту."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "available_routes" in data
    assert isinstance(data["available_routes"], list)
