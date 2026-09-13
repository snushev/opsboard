from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.core.database import get_session
from src.opsboard.schemas.auth import Token
from src.opsboard.services.auth import authenticate_user, create_access_token
from src.opsboard.dependencies.auth import get_current_user
from src.opsboard.schemas.users import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(
        db=db, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(401, "Incorrect username or password")

    access_token = create_access_token(data={"sub": str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user=Depends(get_current_user)):
    return current_user
