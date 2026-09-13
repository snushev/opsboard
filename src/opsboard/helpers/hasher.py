from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_pass(password: str) -> str:
    return password_hash.hash(password)


def check_pass(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)
