from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.models.tasks import Task
from src.opsboard.schemas.tasks import TaskCreate, TaskUpdate


async def get_task(
    db: AsyncSession,
    task_id: int,
):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalar_one_or_none()


async def list_tasks(db: AsyncSession):
    result = await db.execute(select(Task).order_by(Task.id))
    return result.scalars().all()


async def create_task(
    db: AsyncSession,
    task: TaskCreate,
    creator_id: int,
):
    db_task = Task(
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        assignee_id=task.assignee_id,
        creator_id=creator_id,
        due_date=task.due_date,
    )

    db.add(db_task)

    await db.commit()
    await db.refresh(db_task)

    return db_task


async def update_task(
    db: AsyncSession,
    db_task: Task,
    task: TaskUpdate,
):
    update_data = task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    await db.commit()
    await db.refresh(db_task)

    return db_task


async def delete_task(
    db: AsyncSession,
    db_task: Task,
):
    await db.delete(db_task)
    await db.commit()
