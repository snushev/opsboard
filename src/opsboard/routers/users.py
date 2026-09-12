from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.opsboard.core.database import get_session
from src.opsboard.schemas.users import UserCreate, UserRead, UserUpdate
from src.opsboard.models.users import User
from src.opsboard.helpers.hasher import hash_pass
from src.opsboard.core.config import SALT

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    hashed_pass = hash_pass(password=user.password, salt=SALT)
    db_user = User(email=user.email, username=user.username, password_hash=hashed_pass)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/users", response_model=UserRead)
async def update_user(db: AsyncSession = Depends(get_session)):
    pass
