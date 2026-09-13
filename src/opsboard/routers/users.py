from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.opsboard.core.database import get_session
from src.opsboard.schemas.users import UserCreate, UserRead, UserUpdate
from src.opsboard.repositories import users as repo_users

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/users", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_session)):
    try:
        db_user = await repo_users.create_user(db, user)
    except IntegrityError:
        raise HTTPException(409, "Email or username alredy exists")
    return db_user


@router.get("/users", response_model=list[UserRead])
async def list_users(db: AsyncSession = Depends(get_session)):
    return await repo_users.list_users(db=db)


@router.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, db: AsyncSession = Depends(get_session)):
    user = await repo_users.get_user(user_id=user_id, db=db)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_session)
):
    try:
        db_user = await repo_users.update_user(user_id=user_id, user=user, db=db)
        if not db_user:
            raise HTTPException(404, "User not found")
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Email or username already exists")
    return db_user


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    db_user = await repo_users.delete_user(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(404, "User not found")

    return db_user


@router.patch("/users/{user_id}/close", response_model=UserRead)
async def deactivate_user(user_id: int, db: AsyncSession = Depends(get_session)):
    db_user = await repo_users.deactivate(user_id=user_id, db=db)

    if not db_user:
        raise HTTPException(404, "User not found")

    return db_user
