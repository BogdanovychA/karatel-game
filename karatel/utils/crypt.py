import bcrypt


def hash_pass(password: str) -> bytes:
    """Хешування паролю. З сіллю"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_pass(password: str, password_hash: bytes) -> bool:
    """Перевірка паролю по хешу"""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash)
