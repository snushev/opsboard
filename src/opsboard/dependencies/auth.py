from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.core.config import JWT_SECRET_KEY, ALGORITHM
from src.opsboard.core.database import get_session
from src.opsboard.repositories.users import get_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_session)
):
    credential_exception = HTTPException(401, "Could not validate credentials")
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:
        raise credential_exception

    user_id = payload.get("sub")

    if not user_id:
        raise credential_exception

    user = await get_user(db, int(user_id))

    if not user:
        raise credential_exception

    return user
