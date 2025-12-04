# -*- coding: utf-8 -*-

import pytest

from karatel.storage.abstract import FirebaseSaver
from karatel.ui.abstract import NoneOutput
from karatel.utils.utils import generate_random_prefix

output = NoneOutput()
saver = FirebaseSaver()


@pytest.fixture
def registered_user_data():
    """Фікстура, яка реєструє користувача перед тестом та видаляє його після."""

    email = f"test-{generate_random_prefix()}@karatel.ua"
    password = "TestPassword123!"

    # Реєстрація користувача
    is_registered, uid, email, id_token, refresh_token = saver.register_user(
        output, email, password, False
    )

    if not is_registered:
        pytest.fail(f"Не вдалося зареєструвати користувача {email}")

    user_data = {
        "email": email,
        "password": password,
        "uid": uid,
        "id_token": id_token,
        "refresh_token": refresh_token,
    }

    yield user_data

    # Видалення користувача після тесту, якщо test_delete_user() завершився з помилкою
    if user_data.get("id_token"):
        saver.delete_user(output, user_data["uid"], user_data["id_token"], False)


def test_user_login(registered_user_data):
    """Тест логіну користувача."""

    is_logged_in, uid_login, email_login, id_token_login, refresh_token_login = (
        saver.validate_user(
            output,
            registered_user_data["email"],
            registered_user_data["password"],
            False,
        )
    )

    assert is_logged_in
    assert uid_login == registered_user_data["uid"]
    assert email_login == registered_user_data["email"]
    assert id_token_login is not None
    assert refresh_token_login is not None

    if id_token_login is not None:
        registered_user_data["id_token"] = id_token_login


def test_change_password(registered_user_data):
    """Тест зміни пароля користувача."""

    new_password = "NewTestPassword123!"

    (
        is_pass_changed,
        uid_changed,
        email_changed,
        id_token_changed,
        refresh_token_changed,
    ) = saver.update_password(
        output, registered_user_data["id_token"], new_password, False
    )

    assert is_pass_changed
    assert uid_changed == registered_user_data["uid"]
    assert email_changed == registered_user_data["email"]
    assert id_token_changed is not None
    assert refresh_token_changed is not None

    if id_token_changed is not None:
        registered_user_data["id_token"] = id_token_changed


def test_delete_user(registered_user_data):
    """Тест видалення користувача."""

    is_deleted = saver.delete_user(
        output, registered_user_data["uid"], registered_user_data["id_token"], False
    )
    assert is_deleted
    registered_user_data["id_token"] = None
