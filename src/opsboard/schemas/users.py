from datetime import datetime
from pydantic import BaseModel, ConfigDict

from src.opsboard.core.roles import UserRole


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    role: UserRole
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: str | None = None
    username: str | None = None
