from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.opsboard.core.database import get_session
from src.opsboard.schemas.projects import (
    ProjectCreate,
    ProjectRead,
    ProjectUpdate,
)
from src.opsboard.services import projects as service_projects


router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.post("", response_model=ProjectRead)
async def create_project(
    project: ProjectCreate,
    db: AsyncSession = Depends(get_session),
):
    # Temporary owner until /auth/me is connected.
    owner_id = 1

    return await service_projects.create_project(
        db=db,
        project=project,
        owner_id=owner_id,
    )


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    db: AsyncSession = Depends(get_session),
):
    return await service_projects.list_projects(db=db)


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
):
    project = await service_projects.get_project(
        db=db,
        project_id=project_id,
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project: ProjectUpdate,
    db: AsyncSession = Depends(get_session),
):
    db_project = await service_projects.update_project(
        db=db,
        project_id=project_id,
        project=project,
    )

    if not db_project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return db_project


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: AsyncSession = Depends(get_session),
):
    deleted = await service_projects.delete_project(
        db=db,
        project_id=project_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return {"message": "Project deleted"}
