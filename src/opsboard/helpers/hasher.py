import hashlib


def hash_pass(password: str, salt: str) -> str:

    pwd_salt = password + salt
    hashed = hashlib.sha256(pwd_salt.encode())
    return hashed.hexdigest()
