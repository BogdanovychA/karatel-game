# -*- coding: utf-8 -*-

import requests

from karatel.auth.config import API_KEY

BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"


def firebase_signup(email: str, password: str) -> dict:
    url = f"{BASE_URL}:signUp?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def firebase_login(email: str, password: str) -> dict:
    url = f"{BASE_URL}:signInWithPassword?key={API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def change_password(id_token: str, new_password: str) -> dict:

    url = f"{BASE_URL}:update?key={API_KEY}"
    payload = {"idToken": id_token, "password": new_password, "returnSecureToken": True}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
