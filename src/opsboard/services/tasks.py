from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.repositories import tasks as repo_tasks
from src.opsboard.schemas.tasks import TaskCreate, TaskUpdate


async def get_task(
    db: AsyncSession,
    task_id: int,
):
    return await repo_tasks.get_task(
        db=db,
        task_id=task_id,
    )


async def list_tasks(db: AsyncSession):
    return await repo_tasks.list_tasks(db=db)


async def create_task(
    db: AsyncSession,
    task: TaskCreate,
    creator_id: int,
):
    return await repo_tasks.create_task(
        db=db,
        task=task,
        creator_id=creator_id,
    )


async def update_task(
    db: AsyncSession,
    task_id: int,
    task: TaskUpdate,
):
    db_task = await repo_tasks.get_task(
        db=db,
        task_id=task_id,
    )

    if not db_task:
        return None

    return await repo_tasks.update_task(
        db=db,
        db_task=db_task,
        task=task,
    )


async def delete_task(
    db: AsyncSession,
    task_id: int,
):
    db_task = await repo_tasks.get_task(
        db=db,
        task_id=task_id,
    )

    if not db_task:
        return None

    await repo_tasks.delete_task(
        db=db,
        db_task=db_task,
    )

    return True
