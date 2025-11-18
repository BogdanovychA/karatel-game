import re

import bcrypt


def hash_pass(password: str) -> bytes:
    """Хешування паролю. З сіллю"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_pass(password: str, password_hash: bytes) -> bool:
    """Перевірка паролю по хешу"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)


def validate_username(username: str) -> bool:
    """Перевіряє, чи ім'я користувача складається лише з латинських літер та цифр
    і має довжину від 3 до 40 символів."""
    pattern = r"^[a-zA-Z0-9\_]{3,40}$"
    return bool(re.fullmatch(pattern, username))


def is_password_valid(password: str) -> bool:
    """Перевіряє пароль на відповідність вимогам безпеки."""
    special_chars = r'!@#$%^&*()_+'
    pattern = r"""
                ^                      # Початок рядка
                (?=.*[A-Z])            # 1. Lookahead: має бути хоча б одна велика літера
                (?=.*[a-z])            # 2. Lookahead: має бути хоча б одна мала літера
                (?=.*\d)               # 3. Lookahead: має бути хоча б одна цифра
                (?=.*[{0}])            # 4. Lookahead: має бути хоча б один спец. символ
                [a-zA-Z0-9{0}]{{8,}}   # Дозволені символи (всі попередні + спец.) і мінімум 8 разів
                $                      # Кінець рядка
            """.format(
        re.escape(special_chars)
    )
    return bool(re.fullmatch(pattern, password, re.VERBOSE))
