from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from src.opsboard.schemas.users import UserCreate, UserUpdate
from src.opsboard.models.users import User
from src.opsboard.helpers.hasher import hash_pass


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession):
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    hashed_pass = hash_pass(password=user.password)
    db_user = User(email=user.email, username=user.username, password_hash=hashed_pass)
    db.add(db_user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(db_user)
    return db_user


async def update_user(user_id: int, user: UserUpdate, db: AsyncSession):
    db_user = await get_user(user_id=user_id, db=db)

    if db_user is None:
        return None

    update_data = user.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_user, field, value)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(db_user)
    return db_user


async def delete_user(user_id: int, db: AsyncSession):

    db_user = await get_user(user_id=user_id, db=db)
    if not db_user:
        return None

    await db.delete(db_user)
    await db.commit()
    return {"message": "User deleted"}


async def deactivate(user_id: int, db: AsyncSession):
    db_user = await get_user(db, user_id)
    if not db_user:
        return None

    db_user.is_active = False
    await db.commit()
    await db.refresh(db_user)
    return db_user
