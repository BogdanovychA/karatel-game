import re

import bcrypt


def hash_pass(password: str) -> bytes:
    """Хешування паролю. З сіллю"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def validate_password(password: str, password_hash: bytes) -> bool:
    """Перевірка пароля по хешу"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)


def is_username_valid(username: str) -> bool:
    """Перевіряє, чи ім'я користувача є валідним"""

    pattern = r"""
        ^                    # Початок рядка
        [a-zA-Z0-9\_]{2,40}  # Дозволені символи: великі та малі латинські літери (a-z, A-Z),
                             # цифри (0-9) та символ підкреслення (_).
                             # Кількість символів: від 2 до 40.
        $                    # Кінець рядка
    """

    return bool(
        re.fullmatch(pattern, username, re.VERBOSE)
    )  # re.VERBOSE ігнорує пробіли та коментарі в патерні


def is_email_valid(email: str) -> bool:
    """Перевіряє, чи є емейл є валідним"""
    pattern = r"""
        ^                  # Початок рядка
        [a-zA-Z0-9._%+-]+  # 1. Локальна частина: одна або більше літер, цифр, крапок, підкреслень, %, +, -
        @                  # 2. Символ '@' обов'язковий
        [a-zA-Z0-9.-]+     # 3. Домен: одна або більше літер, цифр, крапок або дефісів
        \.                 # 4. Крапка перед доменом верхнього рівня
        [a-zA-Z]{2,}       # 5. Домен верхнього рівня: мінімум 2 літери (наприклад .com, .ua)
        $                  # Кінець рядка
    """
    return bool(
        re.fullmatch(pattern, email, re.VERBOSE)
    )  # re.VERBOSE ігнорує пробіли та коментарі в патерні


def is_password_valid(password: str) -> bool:
    """Перевіряє пароль є валідним"""
    special_chars = r'!@#$%^&*()_+'
    pattern = r"""
                ^                     # Початок рядка
                (?=.*[A-Z])           # 1. Lookahead: має бути хоча б одна велика літера
                (?=.*[a-z])           # 2. Lookahead: має бути хоча б одна мала літера
                (?=.*\d)              # 3. Lookahead: має бути хоча б одна цифра
                (?=.*[{0}])           # 4. Lookahead: має бути хоча б один спец. символ
                [a-zA-Z0-9{0}]{{8,}}  # Дозволені символи (всі попередні + спец.) і мінімум 8 разів
                $                     # Кінець рядка
            """.format(
        re.escape(special_chars)
    )
    return bool(
        re.fullmatch(pattern, password, re.VERBOSE)
    )  # re.VERBOSE ігнорує пробіли та коментарі в патерні
