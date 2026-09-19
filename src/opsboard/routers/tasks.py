from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.core.database import get_session
from src.opsboard.schemas.tasks import (
    TaskCreate,
    TaskRead,
    TaskUpdate,
)
from src.opsboard.services import tasks as service_tasks


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.post("", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_session),
):
    # Temporary creator until /auth/me is connected.
    creator_id = 1

    return await service_tasks.create_task(
        db=db,
        task=task,
        creator_id=creator_id,
    )


@router.get("", response_model=list[TaskRead])
async def list_tasks(
    db: AsyncSession = Depends(get_session),
):
    return await service_tasks.list_tasks(db=db)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_session),
):
    task = await service_tasks.get_task(
        db=db,
        task_id=task_id,
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task: TaskUpdate,
    db: AsyncSession = Depends(get_session),
):
    db_task = await service_tasks.update_task(
        db=db,
        task_id=task_id,
        task=task,
    )

    if not db_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return db_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_session),
):
    deleted = await service_tasks.delete_task(
        db=db,
        task_id=task_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return {"message": "Task deleted"}
