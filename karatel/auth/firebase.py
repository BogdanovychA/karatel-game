# -*- coding: utf-8 -*-

import requests

from karatel.auth.config import API_KEY

BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"


def sing(email: str, password: str, command: str) -> dict:
    url = f"{BASE_URL}:{command}?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def firebase_signup(email: str, password: str) -> dict:
    """Реєстрація користувача у Firebase Authentication."""
    return sing(email, password, "signUp")


def firebase_signin(email: str, password: str) -> dict:
    """Логін користувача у Firebase Authentication."""
    return sing(email, password, "signInWithPassword")


def firebase_change_password(id_token: str, new_password: str) -> dict:
    """Зміна пароля користувача у Firebase Authentication."""
    command = "update"
    url = f"{BASE_URL}:{command}?key={API_KEY}"
    payload = {"idToken": id_token, "password": new_password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def firebase_delete_user(id_token: str) -> dict:
    """Видалення користувача з Firebase Authentication."""
    command = "delete"
    url = f"{BASE_URL}:{command}?key={API_KEY}"
    payload = {"idToken": id_token}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
