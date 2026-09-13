from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

import jwt

from src.opsboard.helpers.hasher import check_pass
from src.opsboard.repositories.users import get_user_by_username
from src.opsboard.core.config import (
    JWT_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)


async def authenticate_user(db: AsyncSession, username: str, password: str):
    user = await get_user_by_username(db=db, username=username)

    if not user:
        return None

    if not check_pass(password, user.password_hash):
        return None

    return user
