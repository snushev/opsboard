from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.repositories import projects as repo_projects
from src.opsboard.schemas.projects import ProjectCreate, ProjectUpdate


async def get_project(
    db: AsyncSession,
    project_id: int,
):
    return await repo_projects.get_project(
        db=db,
        project_id=project_id,
    )


async def list_projects(db: AsyncSession):
    return await repo_projects.list_projects(db=db)


async def create_project(
    db: AsyncSession,
    project: ProjectCreate,
    owner_id: int,
):
    return await repo_projects.create_project(
        db=db,
        project=project,
        owner_id=owner_id,
    )


async def update_project(
    db: AsyncSession,
    project_id: int,
    project: ProjectUpdate,
):
    db_project = await repo_projects.get_project(
        db=db,
        project_id=project_id,
    )

    if not db_project:
        return None

    return await repo_projects.update_project(
        db=db,
        db_project=db_project,
        project=project,
    )


async def delete_project(
    db: AsyncSession,
    project_id: int,
):
    db_project = await repo_projects.get_project(
        db=db,
        project_id=project_id,
    )

    if not db_project:
        return None

    await repo_projects.delete_project(
        db=db,
        db_project=db_project,
    )

    return True
