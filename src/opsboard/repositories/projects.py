from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.models.projects import Project
from src.opsboard.schemas.projects import ProjectCreate, ProjectUpdate


async def get_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    return result.scalar_one_or_none()


async def list_projects(db: AsyncSession):
    result = await db.execute(select(Project).order_by(Project.id))
    return result.scalars().all()


async def create_project(
    db: AsyncSession,
    project: ProjectCreate,
    owner_id: int,
):
    db_project = Project(
        name=project.name,
        description=project.description,
        owner_id=owner_id,
    )

    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)

    return db_project


async def update_project(
    db: AsyncSession,
    db_project: Project,
    project: ProjectUpdate,
):
    update_data = project.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_project, field, value)

    await db.commit()
    await db.refresh(db_project)

    return db_project


async def delete_project(
    db: AsyncSession,
    db_project: Project,
):
    await db.delete(db_project)
    await db.commit()
