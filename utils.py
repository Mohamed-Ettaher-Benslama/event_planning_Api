from passlib.hash import pbkdf2_sha256


def hash_password(password: str):
    return pbkdf2_sha256.hash(password)


def verify_hash(password: str, hashes: str):
    return pbkdf2_sha256.verify(password, hashes)

